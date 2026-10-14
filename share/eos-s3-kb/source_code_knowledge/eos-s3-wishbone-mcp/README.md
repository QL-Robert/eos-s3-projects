# eos-s3-wishbone-mcp

MCP server for the QuickLogic EOS S3 eFPGA AHB-to-Wishbone interface. It serves the reference notes from this research (cross-checked against TRM r1.01a), register and signal lookups, clock checks, QuickLogic example RTL, a Verilog slave generator and search over your own copy of the TRM.

## Install

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/) (or pip).

```bash
cd eos-s3-wishbone-mcp
uv sync            # or: pip install -e .   (add ".[pdf]" if you have no pdftotext)
```

## Use with Claude Code

`.mcp.json` in this folder registers the server as `eos-s3-wishbone`. Either open Claude Code in this folder, or copy `.mcp.json` into your FPGA project root and set:

```bash
export EOS_S3_MCP_DIR=/path/to/eos-s3-wishbone-mcp
export EOS_S3_TRM_PDF=/path/to/QL-S3-Technical-Reference-Manual.pdf   # optional, enables trm_search / trm_page
```

Claude Code asks you to approve project-scoped servers the first time. Check with `claude mcp list` or `/mcp`.

Claude Desktop or other MCP clients: same entry under `mcpServers`, with absolute paths instead of the `${...}` variables.

## Tools

| Tool | What it does |
| --- | --- |
| `list_sections`, `get_section`, `search_notes` | Read and search the reference notes |
| `lookup_register` | CRU/PMU/CFG_CTL/interrupt registers and the adc_ad7476_if map, by name or address |
| `lookup_signal` | `qlal4s3b_cell_macro` Wishbone, clock, SDMA and interrupt ports |
| `fabric_address` | M4 address to `WBs_ADR`, 4 KB block and word index |
| `byte_strobe` | `WBs_BYTE_STB` and data lanes for an 8/16/32-bit access |
| `check_clocks` | Checks WB_CLK (C40), C16, C21, C41 against TRM limits |
| `list_example_rtl`, `get_example_rtl` | Fetch QuickLogic s3-gateware files at commit 2f8fed6 (cached in `~/.cache/eos-s3-wishbone-mcp`) |
| `generate_wishbone_slave` | Verilog register block in QuickLogic's pattern (one-cycle ACK, `~ACK`-gated byte-lane writes) |
| `trm_search`, `trm_page` | Search / read your local TRM PDF. Page numbers are PDF page indexes, which match the printed page numbers in r1.01a |

Resources: `eos-s3://notes`, `eos-s3://registers`, `eos-s3://signals`.

## What is and isn't bundled

- Bundled: notes and structured data written during this research.
- Not bundled: QuickLogic RTL (s3-gateware has no license file, so it is fetched from GitHub on demand) and the TRM (marked Confidential; you point the server at your own copy).

## Test

```bash
EOS_S3_TRM_PDF=/path/to/trm.pdf python tests/test_server.py
```

Starts the server over stdio, calls every tool through an MCP client, and, if Icarus Verilog is installed, simulates a generated slave against a bridge-like master (ACK count, byte-lane write, read-only input, write pulse, out-of-block read).

## Caveats

- Protocol timing comes from QuickLogic's behavioural bridge model, not a silicon spec.
- TRM limit for WB_CLK is 10 MHz; QuickLogic's own ADC example runs 18 MHz.
- `generate_wishbone_slave` output has passed simulation only; it has not been synthesised with the QuickLogic toolchain or run on hardware.
