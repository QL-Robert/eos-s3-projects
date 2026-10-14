# EOS S3 knowledge base

Reference material, source code and a search index for the **QuickLogic EOS S3** (Cortex-M4F + eFPGA SoC), mainly on the **QuickFeather** board (QFN package `PU64`). Most questions here are about the eFPGA: Verilog designs, the AHB-to-Wishbone bridge, the FPGA toolchain, and M4 firmware that talks to the fabric.

## Folder map

| Path | What |
|---|---|
| `knowledge_base/` | Markdown: 39 converted PDFs (TRM, datasheets, app notes, IP register maps, schematics) + curated notes. Index: `knowledge_base/README.md` |
| `knowledge_base/EOS_S3_FPGA_Design_Flow.md` | **Start here for any FPGA build/load question** |
| `knowledge_base/boards/` | QuickFeather and SparkFun QuickThing Plus board references; EOS S3 IO → QFN pin / BGA ball map |
| `knowledge_base/wishbone/` | AHB-to-Wishbone bridge reference, registers, signals, clock limits |
| `knowledge_base/designs/` | Summaries of eFPGA designs (S3_FPGA_2xUART_GPIO, qorc-onion-apps) |
| `source_code_knowledge/` | Filtered copy of QuickLogic's qorc-sdk (HAL, BSP, libraries, apps, s3-gateware RTL) + `designs/` (third-party and user designs) + `eos-s3-wishbone-mcp/` |
| `kb_search/` | SQLite full-text index over the two folders above (`kb.sqlite`), `kb_search.py`, `build_index.py` |

`source_code_knowledge/` is a **read-only reference copy** for search and examples — it is not a buildable SDK. To build firmware or FPGA images, use a full clone of https://github.com/QuickLogic-Corp/qorc-sdk.

## How to answer questions

1. **Search before answering** — never rely on memory for registers, addresses, pins, timings or tool flags. Run from this folder (use `py` instead of `python` if needed):
   ```bash
   python kb_search/kb_search.py "WB_CLK maximum frequency"
   python kb_search/kb_search.py "appfpga flash" --area docs -n 5
   python kb_search/kb_search.py load_fpga --area code
   python kb_search/kb_search.py "RAM_8K_BLK" --kind verilog
   python kb_search/kb_search.py --get <chunk_id> --context 1         # full text around a hit
   ```
   Plain words = all must match (auto-falls back to any). Also supports `"phrase"`, `prefix*`, `AND/OR/NOT`, `NEAR(a b, 5)`, `--path <substring>`. Identifiers match whole or by part (`ACK` finds `WBs_ACK`); hex matches in any form (`0x4002_1000` = `0x40021000`). If `kb_search/kb.sqlite` is missing, run `python kb_search/build_index.py` first (~30 s).
2. **Then read the cited lines** with the Read tool (`path`, `L<start>-<end>`) before quoting. Don't read whole large files: the TRM markdown is ~650 KB — search or use offsets.
3. **Cite sources**: file path + section, and the PDF page for converted manuals (shown as `p.N` in search results), e.g. "TRM p.340".
4. **Source priority**: TRM r1.01a / datasheet for hardware facts → QuickLogic SDK/s3-gateware code for actual behaviour → curated notes → third-party designs. Say when sources disagree (e.g. C41 max 20 MHz on TRM p.90 vs 10 MHz on p.341).
5. Label anything not confirmed by a source as an inference. The TRM is marked **Confidential** — don't reproduce large parts of it outside this folder.

## Key facts (verified — see the cited files)

- **Wishbone window**: M4 address `0x4002_0000`–`0x4003_FFFF` (128 KB). `WBs_ADR[16:0]` is a byte address; designs decode 4 KB blocks on `WBs_ADR[16:12]`. Fabric is slave-only; 32-bit data with `WBs_BYTE_STB[3:0]`.
- **WB_CLK (C40) max 10 MHz** (TRM p.90/p.340). Fabric clocks: C16 = `Sys_Clk0`, C21 = `Sys_Clk1` (max 72 MHz), C02 = `Sys_Pclk`.
- **ACK rules**: one-cycle pulse (`ACK_nxt = CYC & STB & ~ACK`), gate writes with `~ACK`, **every address must ACK** (bridge has no timeout → M4 hangs). Keep the QL_Reserved default-ACK block.
- **Resets**: `FB_SW_RESET` 0x4000_4088, `FB_MISC_SW_RST_CTL` 0x4000_4094 (bit0 = WB bridge). Interrupts to M4: `FB_msg_out[3:0]` → FB_INTERRUPT_0..3.
- **Fabric**: 891 logic cells ("2,400 effective"), 8 × 8 Kbit RAM, 8 FIFO controllers, 2 × 32×32 multipliers. SRAM-configured → must be loaded every boot.
- **Toolchain**: `ql_symbiflow` (QuickLogic Symbiflow v1.3.1 via qorc-sdk `envsetup.sh`; Linux/WSL only). Verilog only. Typical:
  `ql_symbiflow -compile -src $PWD -d ql-eos-s3 -P PU64 -t top -v *.v -p quickfeather.pcf [-s top.sdc] -dump header binary jlink openocd`
  Use `-P` for the package (some SDK makefiles use `-k`; undocumented).
- **Loading**: C header + `load_fpga()` from the M4; `.bin` in flash via bootloader (`qfprog --appfpga x.bin --mode fpga|fpga-m4`; appfpga partition at flash `0x40000`); `.jlink`; `.openocd` (`monitor load_bitstream`).
- **QuickFeather pins**: LEDs blue IO_18, green IO_21, red IO_22; user button IO_6; UART TX IO_44 / RX IO_45; SWD IO_14/IO_15 (never assign in a PCF); I2C0 IO_0/IO_1; boot SPI flash IO_34/35/36/38/39.
- **Boards**: QuickFeather = QFN64 (`-P PU64`); SparkFun QuickThing Plus = BGA64 (`-P PD64`). Both use the same IO numbers for LEDs, button, UART, SWD, I2C0 and PDM mic. In a PCF prefer `IO_x` aliases: a bare number is a **QFN pin**, not an IO (red LED = `IO_22` = QFN `34` = BGA `G7`). Full map and per-board header tables: `knowledge_base/boards/`.
- Loading a custom FPGA image **replaces the USB-serial gateware** — the USB port stops being a serial port; use the hardware UART for logs.

## Working on FPGA designs

- Follow the QuickLogic structure: `AL4S3B_FPGA_Top.v` (cell macro `qlal4s3b_cell_macro`, `gclkbuff` on clock/reset) → `AL4S3B_FPGA_IP.v` (decode, ACK OR, read mux) → register/IP blocks → `AL4S3B_FPGA_QL_Reserved.v`.
- Reference designs: `source_code_knowledge/s3-gateware/` (UART 16550, GPIO, FLL_I2S, ADC AD7476), `source_code_knowledge/designs/` and their summaries in `knowledge_base/designs/`.
- Before calling a design done: every top port has a `set_io`, no PCF lines for missing ports, WB_CLK ≤ 10 MHz, add an SDC and check `build/top.log` / `report_timing.setup.rpt`.
- Quick syntax check without the toolchain: `iverilog -Wall` with stubs for `qlal4s3b_cell_macro`, `gclkbuff` and any IP not on hand.

## Maintaining the knowledge base

- **New PDF**: convert with `pymupdf4llm.to_markdown(doc, ignore_images=True)`; add front matter (`title`, `source_file`, `pages`, `sha256`) like the existing files; save in `knowledge_base/`.
- **New note/design**: Markdown with front matter (`title`, `type`, `topic`, `added`); summaries in `knowledge_base/designs/`, code in `source_code_knowledge/designs/<name>/`.
- **Always** add a row to `knowledge_base/README.md`, then rebuild the index: `python kb_search/build_index.py` (~30 s).
- Skip generated bitstream arrays (`*_bit.h`, `firmware_raw_image.h`), binaries, SpDE `.chp` dumps and vendor sim models — they pollute search.

## Don'ts

- Never print, copy or commit API keys or tokens; use environment variables.
- Don't edit files in `source_code_knowledge/` — it mirrors upstream code.
