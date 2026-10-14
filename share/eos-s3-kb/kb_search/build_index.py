#!/usr/bin/env python3
"""Build a SQLite FTS5 full-text index over the EOS S3 knowledge base.

Usage:
    python3 build_index.py [--root W:/2026/EOS] [--db kb.sqlite] [--verbose]

Indexes:
    <root>/knowledge_base/**.md          area = docs   (split by heading, page numbers kept)
    <root>/source_code_knowledge/**      area = code   (C/H by function, Verilog by module,
                                                        markdown/rst by heading, rest by line windows)

The database is rebuilt from scratch each run (a few seconds) into a temp file and then
swapped in, so a search running at the same time never sees a half-built index.
Standard library only (Python 3.8+, SQLite with FTS5).
"""
import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
import time

SCHEMA_VERSION = 1

# ---------------------------------------------------------------- configuration
TARGET = 2500          # preferred chunk size (chars)
MAX = 4000             # hard ceiling before a chunk is split
MIN = 300              # chunks smaller than this are merged with the next one
WINDOW_LINES = 80      # line window for files without structure
OVERLAP_LINES = 8

MAX_CODE_BYTES = 300_000           # skip bigger source files (generated models, bitstreams)
SKIP_DIRS = {".git", ".vscode", "build", "sim", "rtlsim", "timingSim", "timing_sim", "__pycache__"}
CODE_EXT = {
    ".c": "c", ".h": "c", ".cpp": "c", ".s": "asm", ".S": "asm",
    ".v": "verilog", ".vh": "verilog", ".sv": "verilog",
    ".md": "markdown", ".rst": "rst", ".txt": "text",
    ".py": "script", ".sh": "script", ".tcl": "script", ".pl": "script",
    ".mk": "build", ".ld": "build", ".pcf": "constraints", ".sdc": "constraints",
    ".qdc": "constraints", ".cfg": "config",
}
BUILD_NAMES = re.compile(r"^(GNU)?[Mm]akefile.*$|.*gdbinit$")

# lines that are page furniture in the PDF conversions
NOISE_LINE = re.compile(
    r"^\s*(?:"
    r"©\s*\d{4}\s+QuickLogic Corporation\s*"
    r"|EOS S3 TRM \(r[\d.]+a?\)\s*"
    r"|Confidential\s*"
    r"|\**_?www\.quicklogic\.com_?\**\s*\d*\s*"
    r"|<u>www\.quicklogic\.com</u>.*"
    r"|\**\d+\**\s*<u>www\.quicklogic\.com</u>.*"
    r"|\*\*<mark>PRELIMINARY</mark>\*\*\s*"
    r"|\*\*_QuickLogic EOS S3 Ultra Low Power multicore MCU datasheet[^*]*_\*\*\s*"
    r")$"
)
PAGE_LINE = re.compile(r"^\s*(?:\*\*_)?Page\s+(\d+)(?:_\*\*)?\s*$")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
PIC_START, PIC_END = "<!-- Start of picture text -->", "<!-- End of picture text -->"


# ---------------------------------------------------------------- helpers
def clean_heading(h):
    h = re.sub(r"<[^>]+>", "", h)
    h = h.replace("**", "").replace("__", "").replace("~~", "")
    h = re.sub(r"(?<!\w)_|_(?!\w)", "", h)
    return re.sub(r"\s+", " ", h).strip(" *_#")


def junk_heading(h):
    alnum = re.sub(r"[^A-Za-z0-9]", "", h)
    if len(alnum) < 3:
        return True
    if "quicklogic" in alnum.lower() and len(alnum) < 25:
        return True
    return False


def front_matter(text):
    """Return (metadata dict, body, number of lines removed)."""
    if not text.startswith("---\n"):
        return {}, text, 0
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text, 0
    meta = {}
    for line in text[4:end].splitlines():
        m = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
        if m:
            v = m.group(2).strip()
            try:
                v = json.loads(v) if v[:1] in '"[{' else v
            except ValueError:
                v = v.strip('"')
            meta[m.group(1)] = v
    body = text[end + 5:]
    return meta, body, text[:end + 5].count("\n")


IDENT = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")
HEX = re.compile(r"\b0[xX]([0-9A-Fa-f_]+)\b")


def extra_terms(text):
    """Extra tokens so 'ACK' finds WBs_ACK, 'clk' finds Sys_Clk0, '0x40020000' finds 0x4002_0000."""
    out = set()
    for ident in set(IDENT.findall(text)):
        if "_" in ident or re.search(r"[a-z][A-Z]", ident):
            parts = re.split(r"_+|(?<=[a-z0-9])(?=[A-Z])", ident)
            out.update(p.lower() for p in parts if len(p) > 1)
    for h in set(HEX.findall(text)):
        digits = h.replace("_", "").lower().lstrip("0") or "0"
        out.add("0x" + digits)
        out.add("0x" + h.replace("_", "").lower())
    return " ".join(sorted(out))


def split_big(lines, start_line, limit=MAX):
    """Split a list of lines into pieces of <= limit chars, preferring blank-line boundaries."""
    pieces, cur, cur_len, cur_start = [], [], 0, start_line
    for i, line in enumerate(lines):
        ln = len(line) + 1
        if cur and cur_len + ln > limit:
            # back up to the last blank line in the current piece if it is not too early
            cut = None
            for j in range(len(cur) - 1, len(cur) // 2, -1):
                if not cur[j].strip():
                    cut = j + 1
                    break
            if cut:
                pieces.append((cur_start, cur[:cut]))
                cur_start += cut
                cur = cur[cut:]
                cur_len = sum(len(x) + 1 for x in cur)
            else:
                pieces.append((cur_start, cur))
                cur_start += len(cur)
                cur, cur_len = [], 0
        cur.append(line)
        cur_len += ln
    if cur:
        pieces.append((cur_start, cur))
    return pieces


def windows(lines, start=1):
    out, i = [], 0
    while i < len(lines):
        j = min(len(lines), i + WINDOW_LINES)
        out.append((start + i, lines[i:j]))
        if j == len(lines):
            break
        i = j - OVERLAP_LINES
    return out


# ---------------------------------------------------------------- chunkers
def chunk_markdown(text, line_offset=0, rst=False):
    """Split by headings. Returns list of dicts: heading, start_line, end_line, page, text."""
    lines = text.splitlines()

    # page numbers: a 'Page N' line closes page N, so every line before it belongs to page N
    page_of = [None] * len(lines)
    nxt = None
    for i in range(len(lines) - 1, -1, -1):
        m = PAGE_LINE.match(lines[i])
        if m:
            nxt = int(m.group(1))
        page_of[i] = nxt

    if rst:
        # turn RST underlined titles into markdown headings
        levels, conv = {}, list(lines)
        for i in range(1, len(lines)):
            u = lines[i]
            if re.fullmatch(r"([=\-~^*+#\"'`:.])\1{2,}\s*", u) and lines[i - 1].strip() and len(u.strip()) >= len(lines[i - 1].strip()) - 1:
                ch = u.strip()[0]
                levels.setdefault(ch, min(len(levels) + 1, 6))
                conv[i - 1] = "#" * levels[ch] + " " + lines[i - 1].strip()
                conv[i] = ""
        lines = conv

    sections = []          # (heading_path, start_idx, [lines])
    path = []              # [(level, title)]
    cur_lines, cur_start, in_pic, in_fence = [], 0, False, False
    for i, raw in enumerate(lines):
        line = raw
        if line.strip().startswith("```"):
            in_fence = not in_fence
        if not in_fence:
            if PIC_START in line:
                in_pic = True
            if in_pic:
                if PIC_END in line:
                    in_pic = False
                line = line.replace(PIC_START, "").replace(PIC_END, "").replace("<br>", " ")
                cur_lines.append(("[figure text] " + line.strip()) if line.strip() else "")
                continue
            if NOISE_LINE.match(line) or PAGE_LINE.match(line):
                continue
            m = HEADING.match(line)
            if m:
                title = clean_heading(m.group(2))
                if junk_heading(title):
                    continue
                if any(x.strip() for x in cur_lines):
                    sections.append((" > ".join(t for _, t in path), cur_start, cur_lines))
                level = len(m.group(1))
                # PDF conversions often put every heading at level 6; fall back to numbering depth
                num = re.match(r"^(?:Chapter\s+)?(\d+(?:\.\d+)*)\b", title)
                if num and level >= 5:
                    level = min(1 + num.group(1).count("."), 6) if not title.startswith("Chapter") else 1
                while path and path[-1][0] >= level:
                    path.pop()
                path.append((level, title))
                cur_lines, cur_start = [], i
                continue
        cur_lines.append(line)
    if any(x.strip() for x in cur_lines):
        sections.append((" > ".join(t for _, t in path), cur_start, cur_lines))

    # collapse blank runs, merge tiny sections, split big ones
    chunks = []
    pending = None
    for heading, start, body in sections:
        body = re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip("\n").split("\n")
        size = sum(len(x) + 1 for x in body)
        if pending:
            ph, pstart, pbody = pending
            if size + sum(len(x) + 1 for x in pbody) <= TARGET:
                pbody = pbody + ["", "## " + heading.split(" > ")[-1] if heading else ""] + body
                pending = (ph, pstart, pbody)
                continue
            chunks.append(pending)
            pending = None
        if size < MIN:
            pending = (heading, start, body)
            continue
        chunks.append((heading, start, body))
    if pending:
        chunks.append(pending)

    out = []
    for heading, start, body in chunks:
        for pstart, piece in split_big(body, start):
            txt = "\n".join(piece).strip()
            if not txt:
                continue
            first = start + 1 + line_offset
            page = next((page_of[k] for k in range(min(start, len(page_of) - 1), len(page_of)) if page_of[k]), None) if page_of else None
            out.append(dict(heading=heading, symbol="", start_line=first,
                            end_line=first + len(piece), page=page, text=txt))
    return out


C_FUNC = re.compile(r"([A-Za-z_]\w*)\s*\([^;{}]*\)\s*$")
C_TYPE = re.compile(r"\b(struct|union|enum)\s+([A-Za-z_]\w*)")


def strip_c_noise(line, state):
    """Remove comments and string/char literals for brace counting. state = in block comment."""
    out, i, n = [], 0, len(line)
    while i < n:
        if state:
            j = line.find("*/", i)
            if j < 0:
                return "".join(out), True
            i, state = j + 2, False
            continue
        c = line[i]
        if line.startswith("//", i):
            break
        if line.startswith("/*", i):
            state, i = True, i + 2
            continue
        if c in "\"'":
            j = i + 1
            while j < n and line[j] != c:
                j += 2 if line[j] == "\\" else 1
            i = j + 1
            continue
        out.append(c)
        i += 1
    return "".join(out), state


def chunk_c(text):
    lines = text.splitlines()
    blocks, depth, in_comment, start, sig = [], 0, False, 0, []
    for i, line in enumerate(lines):
        code, in_comment = strip_c_noise(line, in_comment)
        if depth == 0 and code.strip():
            sig.append(code)
        opens, closes = code.count("{"), code.count("}")
        was = depth
        depth = max(0, depth + opens - closes)
        if was > 0 and depth == 0 or (was == 0 and depth == 0 and code.rstrip().endswith(";")):
            blocks.append((start, i, " ".join(sig)))
            start, sig = i + 1, []
    if start < len(lines):
        blocks.append((start, len(lines) - 1, " ".join(sig)))

    def name_of(signature):
        head = signature.split("{")[0]
        m = C_FUNC.search(head.strip())
        if m and m.group(1) not in ("if", "while", "for", "switch", "sizeof", "return"):
            return m.group(1)
        m = C_TYPE.search(head)
        if m:
            return m.group(2)
        m = re.search(r"\}\s*([A-Za-z_]\w*)\s*;", signature)
        return m.group(1) if m else ""

    # group consecutive small blocks
    groups, cur = [], []
    for b in blocks:
        size = sum(len(lines[k]) + 1 for k in range(b[0], b[1] + 1))
        cur_size = sum(len(lines[k]) + 1 for g in cur for k in range(g[0], g[1] + 1))
        if cur and cur_size + size > TARGET:
            groups.append(cur)
            cur = []
        cur.append(b)
    if cur:
        groups.append(cur)

    out = []
    for g in groups:
        s, e = g[0][0], g[-1][1]
        names = [n for n in (name_of(b[2]) for b in g) if n]
        for pstart, piece in split_big(lines[s:e + 1], s):
            txt = "\n".join(piece).strip()
            if txt:
                out.append(dict(heading="", symbol=" ".join(dict.fromkeys(names))[:300],
                                start_line=pstart + 1, end_line=pstart + len(piece), page=None, text=txt))
    return out


V_MOD = re.compile(r"^\s*(?:macro)?module\s+([A-Za-z_]\w*)")


def chunk_verilog(text):
    lines = text.splitlines()
    out, i, n = [], 0, len(lines)
    seg_start, name = 0, ""

    def emit(s, e, nm):
        body = lines[s:e]
        pieces = windows(body, s + 1) if sum(len(x) + 1 for x in body) > MAX else [(s + 1, body)]
        for pstart, piece in pieces:
            txt = "\n".join(piece).strip()
            if txt:
                out.append(dict(heading="", symbol=nm, start_line=pstart,
                                end_line=pstart + len(piece) - 1, page=None, text=txt))

    for i, line in enumerate(lines):
        m = V_MOD.match(line)
        if m:
            if i > seg_start and any(x.strip() for x in lines[seg_start:i]) and name:
                emit(seg_start, i, name)
                seg_start = i
            name = m.group(1)
        if re.match(r"^\s*endmodule\b", line):
            emit(seg_start, i + 1, name)
            seg_start, name = i + 1, ""
    if seg_start < n and any(x.strip() for x in lines[seg_start:]):
        emit(seg_start, n, name)
    return out


def chunk_lines(text):
    lines = text.splitlines()
    if sum(len(x) + 1 for x in lines) <= MAX:
        pieces = [(1, lines)]
    else:
        pieces = windows(lines)
    return [dict(heading="", symbol="", start_line=s, end_line=s + len(p) - 1, page=None,
                 text="\n".join(p).strip()) for s, p in pieces if "\n".join(p).strip()]


# ---------------------------------------------------------------- walk
def iter_files(root):
    kb = os.path.join(root, "knowledge_base")
    sc = os.path.join(root, "source_code_knowledge")
    for base, area in ((kb, "docs"), (sc, "code")):
        if not os.path.isdir(base):
            print(f"warning: {base} not found", file=sys.stderr)
            continue
        for d, dirs, files in os.walk(base):
            dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS)
            for f in sorted(files):
                p = os.path.join(d, f)
                ext = os.path.splitext(f)[1]
                if area == "docs":
                    if ext != ".md":
                        continue
                    kind = "markdown"
                else:
                    kind = CODE_EXT.get(ext) or ("build" if BUILD_NAMES.match(f) else None)
                    if not kind:
                        continue
                yield p, area, kind


def build(root, db_path, verbose=False):
    t0 = time.time()
    tmp = db_path + ".tmp"
    if os.path.exists(tmp):
        os.remove(tmp)
    con = sqlite3.connect(tmp)
    con.executescript(f"""
        PRAGMA journal_mode=OFF;
        PRAGMA synchronous=OFF;
        CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE documents(
            id INTEGER PRIMARY KEY, path TEXT UNIQUE, area TEXT, kind TEXT,
            title TEXT, source_file TEXT, size INTEGER, mtime REAL, sha1 TEXT, chunks INTEGER);
        CREATE TABLE chunks(
            id INTEGER PRIMARY KEY, doc_id INTEGER REFERENCES documents(id), ord INTEGER,
            path TEXT, area TEXT, kind TEXT, title TEXT,
            heading TEXT, symbol TEXT, start_line INTEGER, end_line INTEGER, page INTEGER,
            text TEXT, terms TEXT, text_hash TEXT);
        CREATE INDEX chunks_doc ON chunks(doc_id, ord);
        CREATE INDEX chunks_hash ON chunks(text_hash);
        CREATE VIRTUAL TABLE chunks_fts USING fts5(
            title, heading, symbol, path, text, terms,
            content='chunks', content_rowid='id',
            tokenize="unicode61 remove_diacritics 2 tokenchars '_'",
            prefix='2 3 4');
    """)
    n_docs = n_chunks = skipped = 0
    for p, area, kind in iter_files(root):
        rel = os.path.relpath(p, root).replace(os.sep, "/")
        st = os.stat(p)
        if area == "code" and st.st_size > MAX_CODE_BYTES:
            skipped += 1
            if verbose:
                print(f"skip (size {st.st_size}): {rel}")
            continue
        raw = open(p, "rb").read()
        text = raw.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
        if "\x00" in text[:4096]:
            skipped += 1
            continue
        meta, body, off = ({}, text, 0)
        if kind in ("markdown",):
            meta, body, off = front_matter(text)
        title = meta.get("title") or os.path.basename(p)
        if kind == "markdown":
            chunks = chunk_markdown(body, off)
        elif kind == "rst":
            chunks = chunk_markdown(body, 0, rst=True)
        elif kind == "c":
            chunks = chunk_c(text)
        elif kind == "verilog":
            chunks = chunk_verilog(text)
        else:
            chunks = chunk_lines(text)
        if not chunks:
            continue
        cur = con.execute(
            "INSERT INTO documents(path, area, kind, title, source_file, size, mtime, sha1, chunks) VALUES (?,?,?,?,?,?,?,?,?)",
            (rel, area, kind, str(title), str(meta.get("source_file", "")), st.st_size, st.st_mtime,
             hashlib.sha1(raw).hexdigest(), len(chunks)))
        doc_id = cur.lastrowid
        rows = []
        for k, c in enumerate(chunks):
            rows.append((doc_id, k, rel, area, kind, str(title), c["heading"], c["symbol"],
                         c["start_line"], c["end_line"], c["page"], c["text"],
                         extra_terms(c["heading"] + " " + c["symbol"] + " " + c["text"]),
                         hashlib.sha1(re.sub(r"\s+", " ", c["text"]).encode()).hexdigest()[:16]))
        con.executemany(
            "INSERT INTO chunks(doc_id, ord, path, area, kind, title, heading, symbol, start_line, end_line, page, text, terms, text_hash) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
        n_docs += 1
        n_chunks += len(rows)
        if verbose:
            print(f"{len(rows):5d}  {rel}")
    con.execute("INSERT INTO chunks_fts(chunks_fts) VALUES('rebuild')")
    con.execute("INSERT INTO chunks_fts(chunks_fts) VALUES('optimize')")
    info = dict(schema_version=SCHEMA_VERSION, built_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                root=os.path.abspath(root), documents=n_docs, chunks=n_chunks, skipped=skipped,
                seconds=round(time.time() - t0, 1))
    con.executemany("INSERT INTO meta VALUES (?,?)", [(k, str(v)) for k, v in info.items()])
    con.commit()
    con.close()
    os.replace(tmp, db_path)
    return info


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=os.environ.get("EOS_KB_ROOT", os.path.dirname(here)),
                    help="folder containing knowledge_base/ and source_code_knowledge/ (default: parent of this script)")
    ap.add_argument("--db", default=os.environ.get("EOS_KB_DB", os.path.join(here, "kb.sqlite")))
    ap.add_argument("--verbose", "-v", action="store_true")
    a = ap.parse_args()
    info = build(a.root, a.db, a.verbose)
    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()
