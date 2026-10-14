# EOS S3 knowledge base

A searchable, offline knowledge base for the **QuickLogic EOS S3** (Arm
Cortex-M4F with an embedded FPGA), built for use with
[Claude Code](https://code.claude.com/docs/en/overview) or any other tool that
can read files and run a script.

It holds QuickLogic's documentation converted to Markdown, a curated copy of
QuickLogic's own source code, engineering notes written while working with the
part, and a full-text index over all of it. Nothing to install beyond Python:
no server, no API key, no embeddings, no network access.

The point is that a question like *"what is the maximum WB_CLK frequency and
where is that specified?"* gets answered from the documents, with a file name
and a page number, rather than from a model's memory.

## What is in it

| | |
|---|---|
| Converted documents | 980 pages of QuickLogic PDFs as Markdown: the Technical Reference Manual, two datasheet revisions, 19 application notes, IP register maps, board schematics |
| Engineering notes | The eFPGA design flow, the AHB-to-Wishbone interface, the QuickFeather and SparkFun QuickThing Plus boards, an IO-to-package pin map, example design write-ups |
| Source code | 2,889 files of QuickLogic's qorc-sdk (HAL, BSP, libraries, apps, `s3-gateware` RTL) plus third-party designs, as a reference copy |
| Search index | SQLite FTS5 over all of the above: 2,739 files in 8,467 chunks |

## Directory structure

```
eos-s3-kb/
├── README.md                    This file
├── CLAUDE.md                    Instructions for Claude Code: folder map, how
│                                to search and cite, verified facts, design rules
├── GETTING_STARTED.md           Condensed quick start, kept for the zip release
│
├── knowledge_base/              53 Markdown documents, 1.9 MB
│   ├── README.md                Index of every document, with page counts and
│   │                            the source PDF each came from  ← start here
│   ├── QL-S3-Technical-Reference-Manual.md
│   ├── QL-EOS-S3-...-Datasheet-v3_3d.md
│   ├── QL_Application_Note_*.md          19 application notes in all, some
│   │                                     named ..._App_Note or ..._AN_131
│   ├── *_register_map.md                 UART 16550, GPIO, FLL_I2S, USB-serial
│   ├── ADC_IF_IP_Rev100.md               AD7476 ADC interface IP
│   ├── chandalar_rev1_0.md               Reference board schematic
│   ├── SparkFun_..._R8_Schematic.md      QuickThing Plus schematic
│   ├── EOS_S3_FPGA_Design_Flow.md        Toolchains, PCF/SDC, build, loading
│   ├── EOS_S3_Open_Toolchain_Flow_and_MCP_Notes.md
│   ├── boards/
│   │   ├── QuickFeather.md               Pins, boot, flash map, BSP
│   │   ├── QuickThing_Plus.md            Pins, headers, boot straps, recovery
│   │   └── EOS_S3_IO_Package_Map.md      All 46 IOs: QFN pin, BGA ball, board use
│   ├── wishbone/
│   │   ├── EOS_S3_Wishbone_Reference_Notes.md
│   │   ├── EOS_S3_Wishbone_Registers_Signals_Clocks.md
│   │   └── EOS_S3_Wishbone_MCP_Server.md
│   └── designs/
│       ├── S3_FPGA_2xUART_GPIO.md
│       └── qorc-onion-apps.md
│
├── source_code_knowledge/       29 MB, reference copy, not a buildable SDK
│   ├── HAL/  BSP/  Libraries/  Tasks/  Tools/
│   ├── s3-gateware/             QuickLogic eFPGA RTL: UART, GPIO, I2S, ADC,
│   │                            USB-serial, and the AHB-to-Wishbone bridge model
│   ├── qf_apps/  qt_apps/  qomu_apps/  qf_vr_apps/  qorc_apps_au/
│   ├── designs/                 Third-party and user designs
│   ├── eos-s3-wishbone-mcp/     Source of an MCP server for the Wishbone interface
│   └── docs/  freertos_gateware/
│
└── kb_search/
    ├── README.md                Query syntax, chunking rules, database layout
    ├── build_index.py           Chunks everything and builds the index
    ├── kb_search.py             Command-line search, and a `KB` class to import
    └── kb.sqlite                The index (50 MiB, rebuildable in about a minute)
```

## Requirements

- **Python 3.8 or newer.** Standard library only — nothing to `pip install`.
- **Claude Code**, if you want the conversational route. Optional; the search
  script works on its own.

## Quick start

```bash
git clone <this repository>
cd eos-s3-kb
python kb_search/build_index.py          # about a minute, see "Limitations"
```

Then either ask questions:

```bash
claude                                   # from this directory
```

`CLAUDE.md` is picked up automatically and tells Claude Code to search before
answering and to cite the file and page. Questions that work well:

- What is the maximum WB_CLK frequency, and where is it specified?
- How do I load an FPGA bitstream from the M4? Show the register sequence.
- Write a Wishbone register block for four control registers at 0x4002_6000.
- Which QuickFeather pins are free for FPGA IO without breaking SWD or the boot flash?

Or search it directly:

```bash
python kb_search/kb_search.py "FB_MISC_SW_RST_CTL"
python kb_search/kb_search.py "appfpga flash address" --area docs -n 5
python kb_search/kb_search.py load_fpga --area code
python kb_search/kb_search.py "RAM_8K_BLK" --kind verilog
python kb_search/kb_search.py --get 1234 --context 1      # full text around a hit
python kb_search/kb_search.py --stats
```

Plain words mean every word must match, falling back to any word if that finds
nothing. `"exact phrase"`, `prefix*`, `AND`/`OR`/`NOT` and `NEAR(a b, 5)` are
passed through to FTS5. Identifiers match whole or by part, so `ACK` finds
`WBs_ACK`, and hex matches in any spelling, so `0x4002_1000` finds
`0x40021000`. Filter with `--area docs|code`, `--kind`, `--path`.

Full syntax and the database layout are in `kb_search/README.md`.

## Adding material

1. Put Markdown in `knowledge_base/` (or code in
   `source_code_knowledge/designs/<name>/`).
2. Give notes YAML front matter: `title`, `type`, `topic`, `added`. Converted
   PDFs also carry `source_file`, `pages` and `sha256`.
3. Add a row to `knowledge_base/README.md`, which is the index people read.
4. Rebuild: `python kb_search/build_index.py`.

To convert a new PDF, the existing files were made with
`pymupdf4llm.to_markdown(doc, ignore_images=True)`, with Tesseract OCR for
image-only pages.

Claude Code will follow these conventions if asked; they are written down in
`CLAUDE.md`.

## Limitations

Worth reading before trusting an answer.

**The index is not in version control.** `kb.sqlite` is 50.2 MiB, which is over
GitHub's 50 MiB warning threshold, and it is a binary that changes completely on
every rebuild. Run `python kb_search/build_index.py` after cloning; it takes
about a minute. If you do commit it, use Git LFS.

**Search is keyword, not semantic.** FTS5 with BM25 ranking. It is good at
register names, addresses, signal names and tool flags, and weak at loosely
worded questions. If a search comes back empty, try the vendor's own
terminology. There is no embedding model and no vector search.

**Conversion is lossy.** Text extraction keeps prose, tables and register maps
reasonably well, and loses figures. Diagram and schematic text was recovered by
OCR where possible and is tagged `[figure text]`, but it is unreliable: in the
QuickThing Plus schematic, OCR interleaves BGA ball labels with net names, so
ball locations in that file cannot be trusted. Use the datasheet pinout table
instead. **For anything that matters, check the original PDF.** Every converted
file records its source and page count in its front matter.

**Page numbers are PDF page indexes.** They line up with the printed numbers in
the TRM r1.01a, but do not assume that for every document.

**The source tree is for reading, not building.** `source_code_knowledge/` is a
filtered copy with generated bitstream headers, binaries and vendor simulation
models removed. To build firmware or FPGA images, clone
[qorc-sdk](https://github.com/QuickLogic-Corp/qorc-sdk) and run
`source envsetup.sh`, on Linux or WSL.

**The index covers two folders only**: `knowledge_base/` and
`source_code_knowledge/`. Anything added elsewhere is invisible to search.

**No MCP server for the knowledge base.** `CLAUDE.md` plus the search script is
the whole mechanism, which is why there is nothing to install. There is a
separate MCP server for the Wishbone interface specifically; its source is in
`source_code_knowledge/eos-s3-wishbone-mcp/`, it is not wired up here, and it
needs Python 3.10 with `uv` and a local copy of the TRM PDF.

**Known gaps.** The TRM's own figures are absent, so register bit diagrams read
as tables of text at best. Some vendor simulation models were skipped as too
large, so a search for a cell-level primitive may miss. The document counts in
the header of `knowledge_base/README.md` are approximate.

**Sources disagree sometimes, and the notes say so.** For example the TRM gives
C41 as 20 MHz on page 90 and 10 MHz on page 341, and QuickLogic's own ADC
example runs WB_CLK at 18 MHz against a documented 10 MHz limit. Where a note
records a conflict, believe the note's reasoning rather than either number
alone.

**Nothing here is a substitute for QuickLogic's documents.** It is an index over
them.

## Provenance and licensing

- **QuickLogic documents**: the Markdown in `knowledge_base/` is a machine
  conversion of QuickLogic PDFs. Copyright remains QuickLogic Corporation's, and
  the original PDFs are not redistributed here. Check your redistribution rights
  before making a copy of this repository public — in particular for the
  Technical Reference Manual, whose original is marked for restricted
  distribution. To drop it:
  `rm knowledge_base/QL-S3-Technical-Reference-Manual.md`, remove its row from
  `knowledge_base/README.md`, and rebuild the index. Other notes quote short TRM
  facts with page references.
- **qorc-sdk code**: © QuickLogic Corporation, Apache-2.0 per
  `source_code_knowledge/LICENSE`.
- **s3-gateware RTL**: © QuickLogic Corporation. The upstream repository carries
  no licence file, so treat it as all rights reserved.
- **qorc-onion-apps**: Unlicense (public domain),
  <https://github.com/coolbreeze413/qorc-onion-apps>.
- **The notes, the search scripts and `CLAUDE.md`** were written for this
  knowledge base.

If you are publishing this, also check that no credentials travelled with it.
The working folder this was assembled in contains unrelated scripts with a
hard-coded API key; they are not part of this tree, and should not be added to
it.

## Related

The eFPGA designs built against this knowledge base live separately, each with
its own README, build script and testbenches — including a Wishbone SPI host
verified at RTL and on a post-synthesis netlist.
