#!/usr/bin/env python3
"""Search the EOS S3 knowledge-base index (kb.sqlite, built by build_index.py).

Command line:
    python3 kb_search.py "WB_CLK maximum frequency"
    python3 kb_search.py "load_fpga" --area code -n 5
    python3 kb_search.py --get 1234              # print a whole chunk
    python3 kb_search.py --stats

Query syntax:
    plain words        all words must match (falls back to any word if nothing matches)
    "exact phrase"     phrase match
    FB_MISC*           prefix match
    AND / OR / NOT / NEAR(a b, 5)   passed through as SQLite FTS5 syntax

As a library (for the MCP server):
    from kb_search import KB
    kb = KB("kb.sqlite"); kb.search("appfpga flash address", area="docs", limit=5)
"""
import argparse
import os
import re
import sqlite3
import sys

# column weights for bm25: title, heading, symbol, path, text, terms
WEIGHTS = (3.0, 6.0, 8.0, 1.5, 1.0, 0.4)
FTS_SYNTAX = re.compile(r'"|\*|\bAND\b|\bOR\b|\bNOT\b|\bNEAR\(|[:^()]')
TOKEN = re.compile(r"[A-Za-z0-9_]+")


def _norm_token(t):
    m = re.fullmatch(r"0[xX]([0-9A-Fa-f_]+)", t)
    if m:  # 0x4002_0000 / 0x40020000 -> the normalised form stored in 'terms'
        return "0x" + (m.group(1).replace("_", "").lower().lstrip("0") or "0")
    return t


STOPWORDS = set("""a an the and or of to in on for with by from at is are was were be been being do does did
how what where when which who why can could should would will shall may might must i we you it its this that these
those there here my our your me us get set use using used show find tell about into over under than then so if
not no yes any all some each per via vs""".split())


def build_query(q, mode="all"):
    """Turn free text into an FTS5 query. Raw FTS syntax is passed through unchanged."""
    if FTS_SYNTAX.search(q):
        return q
    toks = [_norm_token(t) for t in TOKEN.findall(q)]
    kept = [t for t in toks if t and t.lower() not in STOPWORDS]
    toks = kept or [t for t in toks if t]
    if not toks:
        return None
    quoted = ['"%s"' % t.replace('"', '""') for t in toks]
    return (" OR " if mode == "any" else " AND ").join(quoted)


class KB:
    def __init__(self, db_path):
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"{db_path} not found - run build_index.py first")
        self.con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, check_same_thread=False)
        self.con.row_factory = sqlite3.Row

    def stats(self):
        meta = dict(self.con.execute("SELECT key, value FROM meta").fetchall())
        meta["by_area_kind"] = [dict(r) for r in self.con.execute(
            "SELECT area, kind, COUNT(*) AS documents, SUM(chunks) AS chunks FROM documents GROUP BY area, kind ORDER BY area, chunks DESC")]
        return meta

    def search(self, query, area=None, kind=None, path=None, limit=10, dedupe=True):
        """Ranked chunks. area: 'docs'|'code'; kind: 'markdown','c','verilog',...; path: substring filter.
        Identical chunks in several files are collapsed into one result with 'duplicates' listing the others."""
        results = []
        for mode in ("all", "any"):
            fts = build_query(query, mode)
            if not fts:
                return []
            where, args = ["chunks_fts MATCH ?"], [fts]
            if area:
                where.append("c.area = ?"); args.append(area)
            if kind:
                where.append("c.kind = ?"); args.append(kind)
            if path:
                where.append("c.path LIKE ?"); args.append(f"%{path}%")
            sql = f"""
                SELECT c.id, c.path, c.area, c.kind, c.title, c.heading, c.symbol,
                       c.start_line, c.end_line, c.page, c.text_hash,
                       snippet(chunks_fts, 4, '[', ']', ' … ', 24) AS snippet,
                       bm25(chunks_fts, {', '.join(map(str, WEIGHTS))}) AS score
                FROM chunks_fts JOIN chunks c ON c.id = chunks_fts.rowid
                WHERE {' AND '.join(where)}
                ORDER BY score LIMIT ?"""
            try:
                rows = self.con.execute(sql, args + [limit * 6 if dedupe else limit]).fetchall()
            except sqlite3.OperationalError as e:
                raise ValueError(f"bad query {fts!r}: {e}")
            results, seen = [], {}
            for r in rows:
                d = dict(r, match=mode, duplicates=[])
                key = d["text_hash"]
                if dedupe and key in seen:
                    seen[key]["duplicates"].append(d["path"])
                    continue
                seen[key] = d
                if len(results) < limit:
                    results.append(d)
            for d in results:
                d.pop("text_hash", None)
            if results or FTS_SYNTAX.search(query):
                break
        return results

    def get_chunk(self, chunk_id, context=0):
        """A chunk by id, optionally with N neighbouring chunks from the same file on each side."""
        r = self.con.execute("SELECT * FROM chunks WHERE id = ?", (chunk_id,)).fetchone()
        if not r:
            return None
        if not context:
            return dict(r)
        rows = self.con.execute(
            "SELECT * FROM chunks WHERE doc_id = ? AND ord BETWEEN ? AND ? ORDER BY ord",
            (r["doc_id"], r["ord"] - context, r["ord"] + context)).fetchall()
        out = dict(r)
        out["text"] = "\n\n".join(x["text"] for x in rows)
        out["start_line"], out["end_line"] = rows[0]["start_line"], rows[-1]["end_line"]
        return out

    def get_document(self, path):
        """Whole document text (re-assembled from chunks) and its outline."""
        rows = self.con.execute("SELECT * FROM chunks WHERE path = ? ORDER BY ord", (path,)).fetchall()
        if not rows:
            rows = self.con.execute("SELECT * FROM chunks WHERE path LIKE ? ORDER BY path, ord", (f"%{path}%",)).fetchall()
        return [dict(r) for r in rows]

    def outline(self, path):
        return [dict(r) for r in self.con.execute(
            "SELECT id, heading, symbol, start_line, end_line, page FROM chunks WHERE path = ? ORDER BY ord", (path,))]

    def list_documents(self, area=None):
        sql, args = "SELECT path, area, kind, title, chunks, size FROM documents", []
        if area:
            sql += " WHERE area = ?"; args.append(area)
        return [dict(r) for r in self.con.execute(sql + " ORDER BY area, path", args)]


def _fmt(r):
    loc = f"L{r['start_line']}-{r['end_line']}"
    if r.get("page"):
        loc += f", p.{r['page']}"
    where = r["heading"] or r["symbol"] or ""
    snip = re.sub(r"\s+", " ", r["snippet"])[:300]
    dup = f"\n        (+ identical in {len(r['duplicates'])} other file(s), e.g. {r['duplicates'][0]})" if r.get("duplicates") else ""
    return (f"#{r['id']:<6} {r['path']}  ({loc})\n"
            f"        {where[:120]}\n"
            f"        {snip}{dup}")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", nargs="*")
    ap.add_argument("--db", default=os.environ.get("EOS_KB_DB", os.path.join(here, "kb.sqlite")))
    ap.add_argument("--area", choices=["docs", "code"])
    ap.add_argument("--kind")
    ap.add_argument("--path", help="only files whose path contains this text")
    ap.add_argument("-n", "--limit", type=int, default=10)
    ap.add_argument("--get", type=int, metavar="CHUNK_ID", help="print a whole chunk")
    ap.add_argument("--context", type=int, default=0, help="with --get: neighbouring chunks to include")
    ap.add_argument("--stats", action="store_true")
    a = ap.parse_args()
    kb = KB(a.db)
    if a.stats:
        import json
        print(json.dumps(kb.stats(), indent=2))
        return
    if a.get:
        r = kb.get_chunk(a.get, a.context)
        if not r:
            sys.exit(f"no chunk {a.get}")
        print(f"{r['path']}  L{r['start_line']}-{r['end_line']}" + (f"  p.{r['page']}" if r['page'] else ""))
        print(r["heading"] or r["symbol"])
        print("-" * 80)
        print(r["text"])
        return
    if not a.query:
        ap.error("give a query, --get or --stats")
    res = kb.search(" ".join(a.query), a.area, a.kind, a.path, a.limit)
    if not res:
        print("no results")
        return
    if res[0]["match"] == "any":
        print("(no chunk had every word - showing chunks with any of them)\n")
    for r in res:
        print(_fmt(r))
        print()


if __name__ == "__main__":
    main()
