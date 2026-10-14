# kb_search — full-text search over the EOS S3 knowledge base

SQLite FTS5 index of `knowledge_base/` and `source_code_knowledge/`. Standard-library Python only (3.8+); no packages to install. This is the search engine the knowledge-base MCP server will use.

| File | What it is |
|---|---|
| `build_index.py` | Chunks every file and (re)builds `kb.sqlite` |
| `kb_search.py` | Command-line search, and the `KB` class for the MCP server |
| `kb.sqlite` | The index (~50 MB): 2,736 files → 8,446 chunks (first build, 2026-10-09) |

## Use

Run from this folder (on Windows use `py` instead of `python3`):

```bash
python3 kb_search.py "WB_CLK maximum frequency"
python3 kb_search.py "appfpga flash address" --area docs -n 5
python3 kb_search.py load_fpga --area code
python3 kb_search.py "RAM_8K_BLK INIT_FILE" --kind verilog
python3 kb_search.py 'NEAR("default" ACK timer, 5)'   # raw FTS5 syntax
python3 kb_search.py --get 1059 --context 1           # full text of a hit (+1 chunk either side)
python3 kb_search.py --stats
```

Each hit shows chunk id, file, line range, PDF page (for converted manuals), the heading path or C/Verilog symbol, and a snippet with `[matches]`. Identical chunks found in several files (shared SDK sources, copies of the Wishbone notes) are shown once with "+ identical in N other files".

### Query rules

- Plain words: every word must match; if nothing matches, it retries with any word (and says so). Filler words ("how", "do", "the", …) are ignored.
- `"exact phrase"`, `prefix*`, `AND` / `OR` / `NOT`, `NEAR(a b, 5)` are passed straight to FTS5.
- Identifiers match whole (`WBs_ACK`) **and** by part (`ACK`, `wbs`); camelCase splits too.
- Hex addresses match in any form: `0x4002_1000`, `0x40021000`, `0x0040021000`.
- Filters: `--area docs|code`, `--kind markdown|c|verilog|build|script|rst|text|constraints|config|asm`, `--path <substring>`.

## Rebuild after adding files

```bash
python3 build_index.py            # about 30 s; default root = parent of this folder
python3 build_index.py --root W:/2026/EOS --db kb.sqlite -v
```

The index is rebuilt from scratch into `kb.sqlite.tmp` and swapped in at the end. Environment overrides: `EOS_KB_ROOT`, `EOS_KB_DB`.

## How files are chunked

| Files | Split | Kept per chunk |
|---|---|---|
| `knowledge_base/**/*.md` | By heading (heading path kept, e.g. `Chapter 27 > 27.2.4 S3 Platform Interface`). Sections < 300 chars merged with the next; > 4,000 chars split at blank lines | Title + source PDF from front matter, PDF page number, line range |
| `.md` / `.rst` in the source tree | Same, RST titles converted to headings | |
| `.c` / `.h` | Top-level functions, structs, enums (brace matching ignoring comments/strings); small neighbours grouped to ~2,500 chars | Function/type names |
| `.v` / `.vh` | One chunk per `module`; big modules in 80-line windows with 8-line overlap | Module name |
| Makefiles, linker scripts, PCF/SDC/QDC, scripts, configs, text | Whole file if ≤ 4,000 chars, else 80-line windows | |

Cleaned before indexing: PDF page furniture (`Confidential`, `EOS S3 TRM (r1.01a)`, `© QuickLogic`, `www.quicklogic.com`, `Page N`, datasheet running headers, junk OCR headings). OCR'd figure text is kept, tagged `[figure text]`.

Skipped: `.vscode`, `build`, `sim`, `rtlsim`, `timingSim`, `timing_sim` folders; source files over 300 KB (vendor simulation models); JSON, SVG, batch files.

## Database layout (for the MCP server)

```
documents(id, path, area, kind, title, source_file, size, mtime, sha1, chunks)
chunks(id, doc_id, ord, path, area, kind, title, heading, symbol,
       start_line, end_line, page, text, terms, text_hash)
chunks_fts  FTS5 over (title, heading, symbol, path, text, terms), external content = chunks
            tokenizer unicode61, '_' kept inside tokens, prefix indexes 2/3/4
meta(key, value)   build time, counts, schema_version
```

`terms` holds the extra search tokens (identifier parts, normalised hex). Ranking is BM25 with weights symbol 8, heading 6, title 3, path 1.5, text 1, terms 0.4.

```python
from kb_search import KB
kb = KB("kb.sqlite")
kb.search("appfpga flash address", area="docs", limit=5)   # list of dicts
kb.get_chunk(1059, context=1)
kb.outline("knowledge_base/QL-S3-Technical-Reference-Manual.md")
kb.list_documents(area="docs")
```
