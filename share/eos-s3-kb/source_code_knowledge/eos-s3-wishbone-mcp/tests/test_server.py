"""End-to-end test: start the server over stdio and call every tool through an MCP client."""
import asyncio
import json
import os
import shutil
import subprocess
import sys
import tempfile

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def text(res):
    return "\n".join(c.text for c in res.content if hasattr(c, "text"))


async def main():
    params = StdioServerParameters(command=sys.executable, args=["-m", "eos_s3_wishbone_mcp.server"],
                                   env={**os.environ})
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            tools = {t.name for t in (await s.list_tools()).tools}
            expected = {"list_sections", "get_section", "search_notes", "lookup_register", "lookup_signal",
                        "fabric_address", "byte_strobe", "check_clocks", "list_example_rtl", "get_example_rtl",
                        "generate_wishbone_slave", "trm_search", "trm_page"}
            assert expected <= tools, expected - tools
            res = {x.uri.unicode_string() if hasattr(x.uri, "unicode_string") else str(x.uri)
                   for x in (await s.list_resources()).resources}
            assert "eos-s3://notes" in res, res

            assert "Clocks" in text(await s.call_tool("list_sections", {}))
            assert "10 MHz" in text(await s.call_tool("get_section", {"title": "clocks"}))
            assert "C40" in text(await s.call_tool("search_notes", {"query": "C40"}))
            t = text(await s.call_tool("lookup_register", {"query": "0x40004094"}))
            assert "AHBWB_SW_RESET" in t, t
            assert "FSDMA_CH0" in text(await s.call_tool("lookup_register", {"query": "0x4003_1000"}))
            assert "single-cycle" in text(await s.call_tool("lookup_signal", {"name": "WBs_ACK"}))
            fa = json.loads(text(await s.call_tool("fabric_address", {"address": "0x40031000"})))
            assert fa["WBs_ADR"] == "17'h11000" and fa["block_4k_WBs_ADR_16_12"] == 17, fa
            bs = json.loads(text(await s.call_tool("byte_strobe", {"size_bytes": 1, "address": "0x4002000A"})))
            assert bs["WBs_BYTE_STB"] == "4'b0100", bs
            ck = json.loads(text(await s.call_tool("check_clocks", {"wb_clk_hz": 18e6})))
            assert ck["C40"]["ok"] is False and "advice" in ck, ck
            ck = json.loads(text(await s.call_tool("check_clocks", {"wb_clk_hz": 10e6, "sys_clk0_hz": 48e6})))
            assert ck["C40"]["ok"] and ck["C16"]["ok"], ck

            v = text(await s.call_tool("generate_wishbone_slave", {
                "module_name": "my_regs",
                "registers": [{"name": "ctrl", "offset": "0x4", "access": "rw", "reset": "0x1"},
                              {"name": "status", "offset": "0x8", "access": "ro"},
                              {"name": "fifo_rst", "offset": "0xC", "access": "w1p"}]}))
            assert "module my_regs" in v and "ctrl_o" in v and "status_i" in v
            if shutil.which("iverilog"):
                with tempfile.NamedTemporaryFile("w", suffix=".v", delete=False) as f:
                    f.write(v)
                tb = os.path.join(os.path.dirname(__file__), "tb_generated_slave.v")
                simbin = f.name + ".vvp"
                subprocess.run(["iverilog", "-g2005", "-o", simbin, f.name, tb], check=True)
                out = subprocess.run(["vvp", simbin], capture_output=True, text=True, timeout=60).stdout
                assert "FAIL" not in out and "acks=8 OK" in out and "pulses=1" in out, out
                print("iverilog: generated slave passes bus simulation")

            print(text(await s.call_tool("list_example_rtl", {}))[:80])
            rtl = text(await s.call_tool("get_example_rtl", {"file": "Dma_Ctrl.v", "max_lines": 5}))
            print("get_example_rtl:", rtl.splitlines()[0])

            tr = text(await s.call_tool("trm_search", {"query": "C40"}))
            print("trm_search:", tr[:160].replace("\n", " "))
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    asyncio.run(main())
