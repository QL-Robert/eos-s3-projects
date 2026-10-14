---
title: "S3_FPGA_2xUART_GPIO — eFPGA design (2× UART 16550 + 32-bit GPIO)"
source_folder: "C:/Users/Rob/Downloads/S3_FPGA_2xUART_GPIO"
source_code: "source_code_knowledge/designs/S3_FPGA_2xUART_GPIO/"
type: "design-summary"
topic: "FPGA Wishbone interface"
board: "QuickFeather (PU64)"
added: 2026-10-09
---

# S3_FPGA_2xUART_GPIO — eFPGA design

EOS S3 eFPGA design for QuickFeather with **two 16550 UARTs and a GPIO controller** on the M4's AHB-to-Wishbone bus. It combines QuickLogic's `s3-gateware` examples **S3_FPGA_2xUART** (two UARTs) and **S3_FPGA_UART_GPIO** (one UART + GPIO).

Source: `source_code_knowledge/designs/S3_FPGA_2xUART_GPIO/` (`rtl/` + makefiles). Related: [Wishbone reference notes](<../wishbone/EOS_S3_Wishbone_Reference_Notes.md>), [UART 16550 register map](<../UART_16550_register_map.md>), [GPIO register map](<../GPIO_register_map.md>), [FPGA_UART_2x doc](<../FPGA_UART_2x.md>).

## Files

| File | Role |
|---|---|
| `rtl/AL4S3B_FPGA_Top.v` | Top level `top`: pads, `qlal4s3b_cell_macro`, clock/reset buffers, interrupts |
| `rtl/AL4S3B_FPGA_IP.v` | Wishbone address decode, read mux, ACK OR; instantiates the blocks below |
| `rtl/AL4S3B_FPGA_Registers.v` | ID / revision registers (block 0) |
| `rtl/AL4S3B_FPGA_QL_Reserved.v` | QuickLogic reserved block + default-ACK timer (identical to QuickLogic's) |
| `rtl/quickfeather.pcf` | Pin constraints |
| `rtl/makefile`, `makefile`, `rtl/compile.txt` | Build with `ql_symbiflow` (`-d ql-eos-s3 -P pu64`) → `top_bit.h` |
| `docs/FPGA_UART_2x.pdf/.docx` | Not copied: byte-identical to QuickLogic's S3_FPGA_2xUART doc (already in the knowledge base); does not cover GPIO |

IP pulled in from `s3-gateware/ip_modules/`: **UART_16550** and **GPIO** (`GPIO_controller.v`).

## Architecture

```
M4 ── AHB ──► AHB-to-Wishbone bridge (qlal4s3b_cell_macro)
                  │  WB_CLK = gclkbuff(Sys_Clk0)   WB_RST_FPGA = gclkbuff(Sys_Clk0_Rst | WB_RST)
                  ▼
           AL4S3B_FPGA_IP  (decode WBs_ADR[16:12], OR of ACKs, read mux)
             ├─ 0x0000  AL4S3B_FPGA_Registers   ID / revision
             ├─ 0x1000  UART_16550 #0  ── UART0_SIN_i / UART0_SOUT_o, INTR → FB_msg_out[2]
             ├─ 0x2000  UART_16550 #1  ── UART1_SIN_i / UART1_SOUT_o, INTR → FB_msg_out[3]
             ├─ 0x4000  GPIO_controller ── GPIO_io[31:0] (only [3:0] reach pads)
             └─ 0x5000  AL4S3B_FPGA_QL_Reserved  + default-ACK for unclaimed addresses
```

`CLK_IP`/`RST_IP` (= `Sys_Clk1`/`Sys_Clk1_Rst`) are passed into the IP but not used by any block; the UARTs and GPIO run on `WB_CLK` (Sys_Clk0). Keep Sys_Clk0 ≤ 10 MHz (TRM limit for WB_CLK). The UART baud rate is derived from this clock.

## Memory map (M4 addresses)

| M4 address | Fabric offset | Block | Notes |
|---|---|---|---|
| 0x4002_0000 | 0x0_0000 | FPGA registers | +0x000 Device ID = **0xABCD0004** (RO); +0x004 Revision = 0x00000100 (RO); other addresses read 0xFAB_DEF_AC |
| 0x4002_1000 | 0x0_1000 | UART0 (16550) | 8-bit registers on word addresses (`WBs_ADR[5:2]`), data in [7:0]; reads return {16'h0, 16-bit} |
| 0x4002_2000 | 0x0_2000 | UART1 (16550) | Same as UART0 |
| 0x4002_3000 | 0x0_3000 | *(unused)* | Reads 0xBAD_FAB_AC; ACKed by the default-ACK timer (~7 WB_CLK) |
| 0x4002_4000 | 0x0_4000 | GPIO | +0x00 GPIO_IN (RO), +0x04 GPIO_OUT (RW), +0x08 GPIO_OE (RW, 1 = drive); 32 bits, only bits [3:0] wired to pads |
| 0x4002_5000 | 0x0_5000 | QL reserved | +0x1F8 {16'h0, cust 0x01, prod 0x00}; +0x1FC {major 0x0001, minor 0x0000} |
| other | — | — | 0xBAD_FAB_AC + default ACK |

Differences from QuickLogic's S3_FPGA_2xUART: GPIO block added at 0x4000, QL reserved block moved from 0x3000 to **0x5000**, Device ID changed 0xABCD0002 → **0xABCD0004**, `gnd_o` and `dbg_reset_o` removed. Firmware written for the original 2xUART image that reads the reserved block at 0x4002_3000 must be updated.

## Interrupts

| FB_msg_out bit | Source | M4 interrupt |
|---|---|---|
| 0, 1 | tied 0 | — |
| 2 | UART0 INTR | FB_INTERRUPT_2 |
| 3 | UART1 INTR | FB_INTERRUPT_3 |

GPIO has no interrupt. SDMA, packet FIFO and SPI-master APB ports are tied off.

## Pins (`quickfeather.pcf`)

| Signal | Pad |
|---|---|
| UART0_SIN_i | IO_2 |
| UART0_SOUT_o | IO_3 |
| UART1_SIN_i | IO_4 |
| UART1_SOUT_o | IO_5 |
| gnd_o | IO_10 *(no such port in this design — see issues)* |
| GPIO_io[3:0] | **not constrained** |

For reference, QuickLogic's S3_FPGA_UART_GPIO puts GPIO_io(0..3) on IO_18, IO_21, IO_22 (QuickFeather blue/green/red LEDs) and IO_7.

## Wishbone implementation notes

- Block select: `WBs_ADR[16:12] == BASE[16:12]` (4 KB blocks, `APERWIDTH = 17`, `APERSIZE = 10`).
- UART cycles are qualified as `CYC & WE & BYTE_STB[0]` for writes and **`CYC & WBs_RD`** for reads, so byte writes must target lane 0, and this design does use `WBs_RD` (unlike most QuickLogic examples).
- The GPIO controller gets the raw `WBs_CYC` and full `WBs_ADR[16:0]` and decodes itself with `MODULE_OFFSET = 0x4000` (`WBs_ADR[16:8]`), so only 0x4000–0x40FF ACKs; 0x4100–0x4FFF fall to the default-ACK timer.
- ACK is the OR of all blocks; each block makes a one-cycle ACK (`CYC & STB & ~ACK`).
- `assign GPIO_io = GPIO[3:0];` in the top level is the same pattern as QuickLogic's S3_FPGA_UART_GPIO; tristates are inside `GPIO_controller` (`GPIO_OE[i] ? GPIO_out[i] : 1'bz`).

## Issues found (checked 2026-10-09)

Checked by elaborating with Icarus Verilog against the real `GPIO_controller.v` and stubs for `UART_16550`, `qlal4s3b_cell_macro` and `gclkbuff`. Not synthesised or placed/routed.

1. **Syntax error — missing comma in the `top` port list** after `UART1_SOUT_o` (line 13 of `AL4S3B_FPGA_Top.v`, before `// GPIO`). The design does not compile as delivered. With the comma added it elaborates with only benign warnings.
2. **`gnd_o` in the PCF has no matching port.** It was removed from `top` (it exists in QuickLogic's 2xUART). Remove the `set_io gnd_o IO_10` line or restore the port, otherwise the PCF step may fail.
3. **GPIO_io[3:0] has no pin constraints.** Add `set_io GPIO_io(n) IO_x` lines; otherwise the tools pick pads (or fail). Avoid IO_2–IO_5 (UARTs).
4. **Build paths assume the s3-gateware tree.** `rtl/makefile` pulls IP from `../../../ip_modules/{UART_16550,GPIO}/rtl/`; place the project under `s3-gateware/projects/` (or edit `MODULEDIRS`) before running `make`.
5. Minor: `AL4S3B_FPGA_Registers` still has unused `fsm_top_st_i` / `spi_fsm_st_i` inputs and an implicit `WBs_ACK_o_nxt` wire (inherited from QuickLogic's template); the Device ID parameter `AL4S3B_DEVICE_ID` is ignored (ID is hard-coded 0xABCD0004).
6. Docs folder is the unchanged 2xUART document; no GPIO documentation or updated memory map.

## Firmware sketch

```c
#define FPGA_BASE      0x40020000UL
#define FPGA_ID        (*(volatile uint32_t *)(FPGA_BASE + 0x0000))  // 0xABCD0004
#define UART0_BASE     (FPGA_BASE + 0x1000)
#define UART1_BASE     (FPGA_BASE + 0x2000)
#define GPIO_IN        (*(volatile uint32_t *)(FPGA_BASE + 0x4000))
#define GPIO_OUT       (*(volatile uint32_t *)(FPGA_BASE + 0x4004))
#define GPIO_OE        (*(volatile uint32_t *)(FPGA_BASE + 0x4008))
// UART 16550 registers are 8-bit, one per 32-bit word: reg n at UARTx_BASE + 4*n
```
