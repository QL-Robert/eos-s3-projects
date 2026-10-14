# EOS S3 knowledge base — getting started

A searchable knowledge base for the **QuickLogic EOS S3** and its embedded FPGA, set up for **Claude Code**. No MCP server, no packages to install.

## What you need

- **Claude Code**, installed and signed in: https://code.claude.com/docs/en/overview
- **Python 3.8 or newer** (`python --version`; on Windows `py --version` also works). Only the standard library is used.

## Start

1. Unzip this folder anywhere, e.g. `C:\work\eos-s3-kb` or `~/eos-s3-kb`.
2. Open a terminal **in that folder** and run `claude`. Claude Code reads `CLAUDE.md` automatically.
3. Ask questions, for example:
   - "What is the maximum WB_CLK frequency and where is it specified?"
   - "How do I load an FPGA bitstream from the M4? Show the register sequence."
   - "Write a Wishbone register block for 4 control registers at 0x4002_6000."
   - "What is the QFN pin and BGA ball for the red LED, and which header pins does the QuickThing Plus expose for I2S?"
   - "Which QuickFeather pins can I use for FPGA IO without breaking SWD or the boot flash?"

Claude searches the index, reads the matching sections, and cites file and PDF page.

## Search it yourself

```bash
python kb_search/kb_search.py "FB_MISC_SW_RST_CTL"
python kb_search/kb_search.py "appfpga flash address" --area docs
python kb_search/kb_search.py load_fpga --area code -n 5
python kb_search/kb_search.py --get 1234 --context 1
python kb_search/kb_search.py --stats
```

See `kb_search/README.md` for query syntax and how files are chunked.

## Contents

| Folder | Size | What |
|---|---|---|
| `CLAUDE.md` | | Instructions for Claude Code: folder map, how to search and cite, key facts, design rules |
| `knowledge_base/` | 2 MB | Markdown versions of 39 QuickLogic PDFs (TRM r1.01a, datasheets, app notes, IP register maps, schematics) + curated notes on the FPGA design flow, the Wishbone interface, example designs and the QuickFeather / QuickThing Plus boards (`knowledge_base/boards/`). Index: `knowledge_base/README.md` |
| `source_code_knowledge/` | 34 MB | QuickLogic's own code from qorc-sdk (HAL, BSP, libraries, apps, s3-gateware RTL), qorc-onion-apps (public domain) and other designs — a reference copy, not a buildable SDK |
| `kb_search/` | ~50 MB | Full-text index (`kb.sqlite`) and the search/build scripts |

## Adding material

Put new Markdown in `knowledge_base/` (or code in `source_code_knowledge/designs/`), add a row to `knowledge_base/README.md`, then rebuild:

```bash
python kb_search/build_index.py
```

Or ask Claude Code to do it — `CLAUDE.md` describes the conventions.

## Building firmware or FPGA images

Not needed for asking questions. For actual builds you need Linux or WSL, a full clone of https://github.com/QuickLogic-Corp/qorc-sdk with `source envsetup.sh` (installs the ARM compiler, the QuickLogic FPGA toolchain and the `qfprog` flasher), and a QuickFeather board. See `knowledge_base/EOS_S3_FPGA_Design_Flow.md`.

## Confidential material

`knowledge_base/QL-S3-Technical-Reference-Manual.md` is converted from QuickLogic's **EOS S3 TRM r1.01a, marked Confidential**. Only pass this package on to people entitled to that document. To make a version without it:

```bash
rm knowledge_base/QL-S3-Technical-Reference-Manual.md     # (Windows: del knowledge_base\QL-S3-Technical-Reference-Manual.md)
python kb_search/build_index.py
```

and remove its row from `knowledge_base/README.md`. Other notes quote short TRM facts with page references.

## Sources and licences

- QuickLogic documents and qorc-sdk code: © QuickLogic Corporation, under their respective terms (qorc-sdk: Apache-2.0 per `source_code_knowledge/LICENSE`).
- qorc-onion-apps: Unlicense (public domain), https://github.com/coolbreeze413/qorc-onion-apps
- Curated notes and the search scripts were written for this knowledge base.

Built 2026-10-10; board references (QuickFeather, QuickThing Plus, IO pin map) added 2026-10-11.
