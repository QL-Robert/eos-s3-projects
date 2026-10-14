"""MCP server: QuickLogic EOS S3 eFPGA Wishbone interface reference.

Run with:  eos-s3-wishbone-mcp            (stdio transport)
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import urllib.request
from functools import lru_cache
from importlib import resources
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .knowledge.data import (
    CLOCK_LIMITS,
    EXAMPLE_FILES,
    FPGA_BASE,
    FPGA_SIZE,
    REGISTERS,
    S3_GATEWARE_COMMIT,
    SIGNALS,
)

mcp = FastMCP(
    "eos-s3-wishbone",
    instructions=(
        "Reference for the QuickLogic EOS S3 AHB-to-Wishbone bridge into the eFPGA: memory map, "
        "signals, protocol rules, clocks/resets (cross-checked against TRM r1.01a), the "
        "adc_ad7476_if example, a Verilog slave generator, and optional search of a local TRM PDF. "
        "Key rules: WB_CLK (C40) max 10 MHz; ACK must be a one-cycle pulse; the bridge has no timeout."
    ),
)

CACHE_DIR = Path(os.environ.get("EOS_S3_MCP_CACHE", Path.home() / ".cache" / "eos-s3-wishbone-mcp"))


# ---------------------------------------------------------------- notes
@lru_cache(maxsize=1)
def _notes() -> str:
    return resources.files("eos_s3_wishbone_mcp.knowledge").joinpath("notes.md").read_text(encoding="utf-8")


@lru_cache(maxsize=1)
def _sections() -> dict[str, str]:
    out: dict[str, str] = {}
    title, buf = "Overview", []
    for line in _notes().splitlines():
        if line.startswith("## "):
            out[title] = "\n".join(buf).strip()
            title, buf = line[3:].strip(), [line]
        else:
            buf.append(line)
    out[title] = "\n".join(buf).strip()
    return out


def _fmt_addr(a: int | None) -> str:
    return "n/a" if a is None else f"0x{a >> 16:04X}_{a & 0xFFFF:04X}"


@mcp.resource("eos-s3://notes", mime_type="text/markdown")
def notes_resource() -> str:
    """Full reference notes (markdown)."""
    return _notes()


@mcp.resource("eos-s3://registers", mime_type="application/json")
def registers_resource() -> str:
    """All known registers as JSON."""
    return json.dumps(REGISTERS, indent=2)


@mcp.resource("eos-s3://signals", mime_type="application/json")
def signals_resource() -> str:
    """qlal4s3b_cell_macro Wishbone-related ports as JSON."""
    return json.dumps([dict(zip(("name", "width", "dir_fabric", "description"), s)) for s in SIGNALS], indent=2)


@mcp.tool()
def list_sections() -> list[str]:
    """List the section titles of the reference notes."""
    return list(_sections().keys())


@mcp.tool()
def get_section(title: str) -> str:
    """Return one section of the notes by (case-insensitive, partial) title, e.g. 'clocks', 'protocol', 'TRM'."""
    t = title.lower()
    for name, body in _sections().items():
        if t in name.lower():
            return body
    return f"No section matching '{title}'. Sections: {', '.join(_sections())}"


@mcp.tool()
def search_notes(query: str, max_results: int = 5) -> list[dict]:
    """Keyword search across the notes. Returns matching lines with their section, best matches first."""
    terms = [w for w in re.split(r"\W+", query.lower()) if w]
    hits = []
    for sec, body in _sections().items():
        for line in body.splitlines():
            low = line.lower()
            score = sum(low.count(w) for w in terms)
            if score and all(w in low for w in terms[:1]):
                hits.append({"section": sec, "line": line.strip(), "score": score})
    hits.sort(key=lambda h: -h["score"])
    return hits[:max_results] or [{"section": "", "line": f"No match for '{query}'.", "score": 0}]


# ---------------------------------------------------------------- lookups
@mcp.tool()
def lookup_register(query: str) -> list[dict]:
    """Find registers by name fragment (e.g. 'FB_MISC', 'C16', 'DMA') or address (e.g. '0x40004094', '0x4003_1000')."""
    q = query.strip().lower().replace("_", "")
    addr = None
    if re.fullmatch(r"(0x)?[0-9a-f]+", q):
        try:
            addr = int(q, 16)
        except ValueError:
            addr = None
    res = []
    for r in REGISTERS:
        if (addr is not None and r["address"] == addr) or q in r["name"].lower().replace("_", "") \
                or q in r["block"].lower().replace("_", ""):
            d = dict(r)
            d["address"] = _fmt_addr(r["address"])
            d["reset"] = None if r["reset"] is None else hex(r["reset"])
            res.append(d)
    if not res and addr is not None and FPGA_BASE <= addr < FPGA_BASE + FPGA_SIZE:
        off = addr - FPGA_BASE
        res.append({"name": "(inside FPGA Wishbone window)", "address": _fmt_addr(addr),
                    "notes": f"Fabric offset 0x{off:05X}: WBs_ADR = 0x{off:05X}, 4 KB block index "
                             f"WBs_ADR[16:12] = {off >> 12}, word index WBs_ADR[11:2] = {(off >> 2) & 0x3FF}. "
                             "Meaning depends on the loaded design."})
    return res or [{"name": f"No register matching '{query}'."}]


@mcp.tool()
def lookup_signal(name: str) -> list[dict]:
    """Describe qlal4s3b_cell_macro Wishbone/clock/DMA/interrupt ports (name fragment, e.g. 'ACK', 'SDMA')."""
    n = name.lower()
    res = [dict(zip(("name", "width", "dir_fabric", "description"), s)) for s in SIGNALS if n in s[0].lower()]
    return res or [{"name": f"No signal matching '{name}'."}]


@mcp.tool()
def fabric_address(address: str) -> dict:
    """Convert an M4 address (0x4002_0000..0x4003_FFFF) or a fabric offset to WBs_ADR, block and word index."""
    a = int(address.replace("_", ""), 16)
    off = a - FPGA_BASE if a >= FPGA_BASE else a
    if not 0 <= off < FPGA_SIZE:
        return {"error": f"{address} is outside the 128 KB FPGA window (0x4002_0000-0x4003_FFFF)."}
    return {"m4_address": _fmt_addr(FPGA_BASE + off), "WBs_ADR": f"17'h{off:05X}",
            "block_4k_WBs_ADR_16_12": off >> 12, "word_index_WBs_ADR_11_2": (off >> 2) & 0x3FF,
            "byte_lane_HADDR_1_0": off & 3}


@mcp.tool()
def byte_strobe(size_bytes: int, address: str) -> dict:
    """Byte strobes and data lanes the bridge produces for an M4 access of size_bytes (1, 2 or 4) at address."""
    a = int(address.replace("_", ""), 16)
    lane = a & 3
    if size_bytes == 1:
        stb = 1 << lane
    elif size_bytes == 2:
        stb = 0b0011 if not (a & 2) else 0b1100
    else:
        stb = 0b1111
    lanes = [f"[{8 * i + 7}:{8 * i}]" for i in range(4) if stb >> i & 1]
    return {"WBs_BYTE_STB": f"4'b{stb:04b}", "data_lanes": lanes,
            "note": "Data is not shifted: it sits in its natural lane of WBs_WR_DAT / WBs_RD_DAT. "
                    "Accesses wider than 32 bits are treated as a word."}


@mcp.tool()
def check_clocks(wb_clk_hz: float, sys_clk0_hz: float | None = None, sys_clk1_hz: float | None = None,
                 pkfb_clk_hz: float | None = None) -> dict:
    """Check fabric clock frequencies against TRM r1.01a limits (C40 = WB_CLK, C16, C21, C41)."""
    checks = [("C40", wb_clk_hz), ("C16", sys_clk0_hz), ("C21", sys_clk1_hz), ("C41", pkfb_clk_hz)]
    out = {}
    for clk, f in checks:
        if f is None:
            continue
        lim = CLOCK_LIMITS[clk]
        out[clk] = {"signal": lim["name"], "requested_hz": f, "max_hz": lim["max_hz"],
                    "ok": f <= lim["max_hz"], "source": lim["source"]}
    if wb_clk_hz > CLOCK_LIMITS["C40"]["max_hz"]:
        out["advice"] = ("WB_CLK exceeds the TRM 10 MHz limit (QuickLogic's adc_ad7476_if runs 18 MHz, but that "
                         "is out of spec). Drive WB_CLK from a slower clock and cross into your IP clock domain.")
    # rough access time estimate from the bridge model: ~4.5 WB_CLK + ~4.5 HCLK
    out["estimated_access_ns_excluding_HCLK"] = round(4.5e9 / wb_clk_hz, 1)
    return out


# ---------------------------------------------------------------- example RTL
@mcp.tool()
def list_example_rtl() -> dict:
    """List QuickLogic example files available through get_example_rtl (s3-gateware, pinned commit)."""
    return {"commit": S3_GATEWARE_COMMIT, "files": sorted(EXAMPLE_FILES)}


@mcp.tool()
def get_example_rtl(file: str, start_line: int = 1, max_lines: int = 400) -> str:
    """Fetch an example file from QuickLogic s3-gateware at the pinned commit (cached locally).
    Use start_line/max_lines to page through long files such as pp3_cells_sim.v."""
    if file not in EXAMPLE_FILES:
        return f"Unknown file. Choose from: {', '.join(sorted(EXAMPLE_FILES))}"
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cached = CACHE_DIR / f"{S3_GATEWARE_COMMIT[:8]}_{file}"
    if not cached.exists():
        url = f"https://raw.githubusercontent.com/QuickLogic-Corp/s3-gateware/{S3_GATEWARE_COMMIT}/{EXAMPLE_FILES[file]}"
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                cached.write_bytes(r.read())
        except Exception as e:  # noqa: BLE001
            return f"Could not fetch {url}: {e}"
    lines = cached.read_text(encoding="utf-8", errors="replace").splitlines()
    s = max(start_line, 1) - 1
    chunk = lines[s:s + max_lines]
    header = f"// {file} lines {s + 1}-{s + len(chunk)} of {len(lines)} (s3-gateware @ {S3_GATEWARE_COMMIT[:8]})\n"
    return header + "\n".join(chunk)


# ---------------------------------------------------------------- generator
@mcp.tool()
def generate_wishbone_slave(module_name: str, registers: list[dict], block_base: str = "0x00000",
                            id_value: str = "0xC0DE0001", ack_all_addresses: bool = True) -> str:
    """Generate a Verilog Wishbone slave for the EOS S3 bridge following QuickLogic's pattern.

    registers: list of {"name": str, "offset": "0x4", "access": "rw"|"ro"|"wo"|"w1p", "reset": "0x0"}.
      offset is a byte offset inside the 4 KB block (multiple of 4, not 0 which holds the ID register).
      "ro" registers become input ports; "w1p" is a self-clearing write pulse (e.g. FIFO reset).
    block_base: fabric byte offset of the 4 KB block (e.g. 0x00000 for 0x4002_0000).
    ack_all_addresses: True (default) = ACK every access in the 128 KB window, so it can be the only slave
      with no default-ACK timer (other blocks read 0xBADFABAC). Set False when several slaves share the bus;
      then OR the ACKs and keep a default-ACK timer, or unmapped accesses hang the M4.
    """
    base = int(block_base, 16)
    if base % 0x1000:
        raise ValueError("block_base must be 4 KB aligned")
    regs = []
    for r in registers:
        off = int(str(r["offset"]), 16)
        if off % 4 or not 0 < off < 0x1000:
            raise ValueError(f"offset {r['offset']} must be a non-zero multiple of 4 below 0x1000")
        name = re.sub(r"\W", "_", r["name"])
        regs.append({"name": name, "idx": off >> 2, "access": r.get("access", "rw").lower(),
                     "reset": int(str(r.get("reset", "0")), 16)})
    ports, decls, rst, wr, rd = [], [], [], [], []
    for r in regs:
        n, i = r["name"], r["idx"]
        if r["access"] == "ro":
            ports.append(f"  input      [31:0] {n}_i,")
            rd.append(f"      10'd{i}: WBs_RD_DAT = {n}_i;")
        elif r["access"] == "w1p":
            ports.append(f"  output reg        {n}_pulse_o,")
            rst.append(f"      {n}_pulse_o <= 1'b0;")
            wr.append(f"      {n}_pulse_o <= wr && (wa == 10'd{i}) && WBs_BYTE_STB[0] && WBs_WR_DAT[0];")
            rd.append(f"      10'd{i}: WBs_RD_DAT = 32'h0;")
        else:
            ports.append(f"  output reg [31:0] {n}_o,")
            rst.append(f"      {n}_o <= 32'h{r['reset']:08X};")
            wr.append(f"      if (wr && wa == 10'd{i})\n        for (i = 0; i < 4; i = i + 1)\n"
                      f"          if (WBs_BYTE_STB[i]) {n}_o[8*i +: 8] <= WBs_WR_DAT[8*i +: 8];")
            if r["access"] != "wo":
                rd.append(f"      10'd{i}: WBs_RD_DAT = {n}_o;")
    idv = int(id_value, 16)
    return f"""// Generated by eos-s3-wishbone-mcp. Block at fabric offset 0x{base:05X} (M4 {_fmt_addr(FPGA_BASE + base)}).
// Keep WB_CLK <= 10 MHz (TRM r1.01a p.340). ACK is a one-cycle pulse; writes are gated with ~ACK.
module {module_name} (
  input             WB_CLK,
  input             WB_RST,
  input      [16:0] WBs_ADR,
  input             WBs_CYC,
  input             WBs_STB,
  input             WBs_WE,
  input      [3:0]  WBs_BYTE_STB,
  input      [31:0] WBs_WR_DAT,
{chr(10).join(ports)}
  output reg [31:0] WBs_RD_DAT,
  output reg        WBs_ACK
);
  wire       blk = (WBs_ADR[16:12] == 5'd{base >> 12});
  wire       hit = WBs_CYC & WBs_STB & ~WBs_ACK;   // high for exactly one clock per access
  wire       sel = {"hit" if ack_all_addresses else "hit & blk"};{"  // ACK every address in the window" if ack_all_addresses else "  // ACK own block only: another slave or a default-ACK timer must cover the rest"}
  wire       wr  = hit & blk & WBs_WE;
  wire [9:0] wa  = WBs_ADR[11:2];
  integer i;

  always @(posedge WB_CLK or posedge WB_RST)
    if (WB_RST) begin
      WBs_ACK <= 1'b0;
{chr(10).join(rst)}
    end else begin
      WBs_ACK <= sel;
{chr(10).join(wr)}
    end

  always @(*)
    if (!blk) WBs_RD_DAT = 32'hBAD_FAB_AC;
    else case (wa)
      10'd0: WBs_RD_DAT = 32'h{idv:08X};
{chr(10).join(rd)}
      default: WBs_RD_DAT = 32'hBAD_FAB_AC;
    endcase
endmodule
"""


# ---------------------------------------------------------------- TRM search
@lru_cache(maxsize=1)
def _trm_pages() -> list[str]:
    pdf = os.environ.get("EOS_S3_TRM_PDF")
    if not pdf or not Path(pdf).is_file():
        raise FileNotFoundError("Set EOS_S3_TRM_PDF to the path of your local EOS S3 TRM PDF.")
    if shutil.which("pdftotext"):
        txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout
        return txt.split("\f")
    from pypdf import PdfReader  # optional dependency
    return [p.extract_text() or "" for p in PdfReader(pdf).pages]


@mcp.tool()
def trm_search(query: str, max_results: int = 8, context_lines: int = 2) -> list[dict]:
    """Search your local copy of the EOS S3 TRM (path in env EOS_S3_TRM_PDF). Returns PDF page numbers and snippets.
    Useful queries: 'C40', 'FB_MISC_SW_RST_CTL', 'AHB-To-Wishbone', 'Setup Fabric clocks'."""
    try:
        pages = _trm_pages()
    except Exception as e:  # noqa: BLE001
        return [{"error": str(e)}]
    q = query.lower()
    out = []
    for pno, text in enumerate(pages, start=1):
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if q in line.lower():
                snip = "\n".join(l.rstrip() for l in lines[max(0, i - context_lines): i + context_lines + 1])
                out.append({"pdf_page": pno, "snippet": snip})
                if len(out) >= max_results:
                    return out
    return out or [{"pdf_page": None, "snippet": f"No match for '{query}'."}]


@mcp.tool()
def trm_page(page: int) -> str:
    """Return the text of one page of your local TRM PDF (env EOS_S3_TRM_PDF)."""
    try:
        pages = _trm_pages()
    except Exception as e:  # noqa: BLE001
        return str(e)
    if not 1 <= page <= len(pages):
        return f"Page out of range 1-{len(pages)}."
    return pages[page - 1]


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
