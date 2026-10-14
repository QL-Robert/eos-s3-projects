---
title: "EOS S3 eFPGA Wishbone Interface \u2014 Reference Notes"
source_file: "eos-s3-wishbone-mcp/src/eos_s3_wishbone_mcp/knowledge/notes.md"
type: "notes"
topic: "FPGA Wishbone interface"
added: 2026-10-09
sha256: e93a1d9780d9c895b2f4932aa3de0ab169641000e506a61d168191c862e594d1
---

# EOS S3 eFPGA Wishbone Interface — Reference Notes

The M4 reaches FPGA logic through a single-master, single-transfer, 32-bit Wishbone slave port at 0x4002_0000–0x4003_FFFF (128 KB), clocked by a fabric-driven clock (C40 / `WB_CLK`) that the TRM limits to 10 MHz. Facts are cross-checked against the EOS S3 TRM r1.01a. The TRM says little about the bridge itself, so protocol detail comes from QuickLogic's RTL, simulation models, SDK and IP docs.

## Key facts

| Item | Value | Source |
| --- | --- | --- |
| M4 address window | 0x4002_0000, 128 KB (to 0x4003_FFFF); `FPGA_PERIPH_BASE = PERIPH_BASE + 0x20000` | TRM p.41; SDK `eoss3_dev.h` |
| Bit-band alias | `FPGA_BB_BASE = 0x4240_0000` | SDK `eoss3_dev.h` |
| Address bus | `WBs_ADR[16:0]`, byte address; designs decode word addresses from bit 2 up | cell macro, example RTL |
| Data | 32-bit `WBs_WR_DAT` / `WBs_RD_DAT`, `WBs_BYTE_STB[3:0]` | cell macro; TRM p.275 |
| Transfer sizes | 8/16/32-bit AHB accesses map to byte strobes; wider = 32-bit word | bridge model |
| Handshake | `CYC`+`STB` held until `ACK`; one Wishbone cycle per AHB transfer; no bursts, no error/retry | bridge model |
| Masters | M4-F or AP only; fabric IP cannot initiate transfers | TRM p.275 |
| Clock | `WB_CLK` is a fabric output (CRU C40) driving the bridge; typically `Sys_Clk0` (C16) via `gclkbuff` | TRM p.91–92, p.340 |
| `WB_CLK` maximum | 10 MHz (±10% at DVDD 1.1 V) | TRM p.90, p.340 |
| Clock crossing | Asynchronous; 3-flop toggle synchronisers each way (model) | TRM p.275; bridge model |
| Reset | `WB_RST` from CRU `FB_MISC_SW_RST_CTL[0]` `AHBWB_SW_RESET` (0x4000_4094, default 0) | TRM p.106 |
| Timeout | None: a missing `ACK` stalls the AHB and M4 forever; add a default-ACK timer | `AL4S3B_FPGA_QL_Reserved.v` |
| Response | `HRESP` always OKAY | bridge model |

## Checked against the TRM

| Claim | TRM r1.01a | Page | Result |
| --- | --- | --- | --- |
| FPGA window 0x4002_0000, 128 KB | "Fabric (FPGA) 0x4002_0000 128KB" | 41 | Confirmed |
| 32-bit address and data | "takes a 32-bit address and data on its AHB port and passes these values to the Wishbone bus" | 275 | Confirmed |
| Asynchronous transfers | "supports asynchronous transfers" | 275 | Confirmed (mechanism not described) |
| Fabric is slave only | Fabric IP "does not have the ability to initiate direct transfers" | 275 | Confirmed |
| `WB_CLK` driven by fabric | "C40 (Fabric to Wishbone clock) – WB_CLK"; "Clock output from FB to AHB-WB Bridge" | 92, 340 | Confirmed |
| `WB_CLK` max | "AHB2WB for FPGA clock 10 MHz C40"; "maximum frequency of this clock is 10 MHz" | 90, 340 | Confirmed. ADC example runs 18 MHz = over spec |
| C40 needs Wishbone design | "C40 requires Wishbone Slave design loaded into Fabric" | 340 | Confirmed |
| Fabric input clocks | C16 = Sys_Clk0, C21 = Sys_Clk1, C02 = Sys_Pclk; C16/C21 max 72 MHz | 90, 340 | Confirmed |
| C41 max | Table: 20 MHz; section 36.3: 10 MHz | 90, 341 | TRM inconsistent; use 10 MHz |
| Bridge reset | `FB_MISC_SW_RST_CTL` bit0 AHBWB_SW_RESET (R40), bit1 PFAFIFO1_SW_RESET (R41), default 0 | 106 | Confirmed |
| Fabric domain resets | `FB_SW_RESET` bits 0/2/4/5 = C02/C09/C16/C21, default 1 | 105 | Confirmed |
| 4 fabric interrupts | "Total of 4 outputs from FPGA fabric can be used" | 52 | Confirmed (registers not named) |
| SDMA to fabric | SDMA "can transfer data between M4SRAM, FFE memories, and Fabric" | 342 | Confirmed; no channel map |
| Bring-up order | Power FB domain, enable C09, configure, then enable C16/C21/C02 | 340–341 | Confirmed |
| Handshake, strobes, ACK rules, timeout, latency | Not covered | — | Model/RTL only |

## Architecture and memory map

The hard AHB-to-Wishbone bridge is the only path from the M4 into fabric registers. The bridge presents `HADDR[16:0]` as `WBs_ADR[16:0]`. QuickLogic examples carve the window into 4 KB blocks (`APERWIDTH = 17`, `APERSIZE = 10` words) and decode `WBs_ADR[16:12]`.

| Block (adc_ad7476_if) | Fabric offset | M4 address | Contents |
| --- | --- | --- | --- |
| FPGA registers | 0x0_0000 | 0x4002_0000 | ID 0x0ADC0001, revision, FIFO reset, sensor enable, overrun, debug |
| DMA control registers | 0x1_0000 | 0x4003_0000 | DMA enable, done status, interrupt enable |
| DMA CH0 data port | 0x1_1000 | 0x4003_1000 | Read pops one word of the 512×32 RX FIFO |
| QL reserved | 0x1_2000 | 0x4003_2000 | Customer/product ID at +0x1F8, revisions at +0x1FC |
| Anything else | — | — | Reads 0xBAD_FAB_AC; default-ACK timer completes the cycle |

The layout is a convention; S3_FPGA_2xUART puts UARTs at 0x1000/0x2000 and the reserved block at 0x3000. Separately, the TRM memory map lists RAMFIFO0–3 (FPGA) at 0x4001_8000–0x4001_BFFF (4 KB each): M4 access to fabric RAM/FIFO blocks, not via the Wishbone bridge.

## Signal reference

Ports on `qlal4s3b_cell_macro`, direction from the fabric's point of view.

| Port | Width | Dir | Behaviour |
| --- | --- | --- | --- |
| WBs_ADR | 17 | in | Byte address; registered from HADDR[16:0], stable all cycle |
| WBs_CYC | 1 | in | Cycle valid; asserted with STB, cleared on the edge where the bridge samples ACK |
| WBs_STB | 1 | in | Strobe; always with CYC |
| WBs_WE | 1 | in | 1 = write |
| WBs_RD | 1 | in | 1 = read (~WE during cycle); examples ignore it |
| WBs_BYTE_STB | 4 | in | Byte lanes from HSIZE/HADDR[1:0] |
| WBs_WR_DAT | 32 | in | Write data, wired from HWDATA; valid while CYC/STB high |
| WBs_RD_DAT | 32 | out | Read data, captured on the WB_CLK edge where ACK is high |
| WBs_ACK | 1 | out | Cycle complete; single-cycle pulse |
| WB_CLK | 1 | out (to bridge) | Bus clock (C40), max 10 MHz |
| WB_RST | 1 | in | Bridge reset from FB_MISC_SW_RST_CTL[0] |
| Sys_Clk0 / Sys_Clk0_Rst | 1/1 | in | C16 and reset |
| Sys_Clk1 / Sys_Clk1_Rst | 1/1 | in | C21 and reset |
| Sys_Pclk / Sys_Pclk_Rst | 1/1 | in | C02 and reset |
| SDMA_Req / SDMA_Sreq | 4/4 | out | DMA burst / single request per FPGA DMA channel |
| SDMA_Done / SDMA_Active | 4/4 | in | DMA done / active |
| FB_msg_out | 4 | out | Interrupts to M4 (FB_INTERRUPT_0..3) |
| FB_Int_Clr | 8 | out | Tied 0 in examples |
| Device_ID | 16 | out | Readable by software |
| Sys_PKfb_Clk, FB_PKfb* | — | mixed | Packet FIFO push (C41 domain) |

## Bus protocol and timing

From QuickLogic's behavioural bridge model (`ahb2fb_asynbrig`, `ahb2fb_asynbrig_if`, `fb2ahb_asynbrig_if` in `pp3_cells_sim.v`).

1. HCLK: transfer accepted when `HSEL & HREADY & HTRANS[1]`; address, R/W, byte strobes registered; HREADYOUT drops; strobe toggle flips.
2. WB_CLK: toggle passes a 3-flop synchroniser; edge (ff2 XOR ff3) starts the cycle.
3. WB_CLK: next edge drives CYC=1, STB=1, WE/RD, BYTE_STB; ADR and WR_DAT already stable.
4. WB_CLK: bridge holds everything until it samples ACK=1.
5. WB_CLK: on that edge it captures WBs_RD_DAT, clears CYC/STB/WE/RD/BYTE_STB on the same edge, flips the ack toggle.
6. HCLK: ack toggle synchronised (3 flops); HREADYOUT returns to 1. HRESP always OKAY.

Byte strobes (no data shifting; data in natural lane):

| HSIZE | HADDR[1:0] | BYTE_STB | Lanes |
| --- | --- | --- | --- |
| 000 byte | 00/01/10/11 | 0001/0010/0100/1000 | [7:0]/[15:8]/[23:16]/[31:24] |
| 001 halfword | 0x/1x | 0011/1100 | [15:0]/[31:16] |
| 010 word or larger | — | 1111 | [31:0] |

Rules:
- ACK exactly one WB_CLK cycle: `ACK_nxt = CYC & STB & ~ACK`.
- Gate write enables with `~ACK` so each access writes once.
- WBs_RD_DAT valid on the ACK edge; a combinational mux on WBs_ADR works.
- Never leave a cycle unacknowledged (no bridge timeout).
- Read side effects (FIFO pop, clear-on-read) on or after the ACK edge. UART IP decodes reads with `& WBs_ACK_o` and delays the pop one more clock.

Latency estimate (model, not datasheet): ~1 HCLK + 2–3 WB_CLK sync + 1 WB_CLK to raise CYC + 1 WB_CLK slave + 3–4 HCLK back ≈ 4–5 WB_CLK + 4–5 HCLK per access.

## Clocks and resets

| Clock | Direction/name | Max (TRM) | Registers (CRU base 0x4000_4000) |
| --- | --- | --- | --- |
| C16 | into fabric, Sys_Clk0 | 72 MHz | CLK_Control_F_0 0x020 / F_1 0x024; C16_CLK_GATE 0x064 bit0; CLK_DIVIDER_CLK_GATING 0x124 bit5. SDK S3X_FB_16_CLK |
| C21 | into fabric, Sys_Clk1 | 72 MHz | CLK_Control_I_0 0x034 / 0x038; C21_CLK_GATE 0x070 bit0; master gate bit8. SDK S3X_FB_21_CLK |
| C02 | into fabric, Sys_Pclk | 40 MHz | CLK_Control_B_0 0x008 / 0x00C; C02_CLK_GATE 0x044 bit1; master gate bit1 |
| C09 | configuration APB | 10 MHz | C09_CLK_DIV 0x114; C09_CLK_GATE = 0x6 before loading bitstream |
| C40 | out of fabric, WB_CLK to bridge | 10 MHz | exists only when design drives it; not routable to pads |
| C41 | out of fabric, Sys_PKfb_Clk | 20 MHz (p.90) / 10 MHz (p.341) | turn off before powering down packet FIFO domain |

Resets:

| Register | Address | Bits |
| --- | --- | --- |
| FB_SW_RESET | 0x4000_4088 | [0] C02, [2] C09, [4] C16, [5] C21 domain resets, default 1; [1],[3] general purpose. Write 1 asserts immediately, 0 releases synchronously |
| FB_MISC_SW_RST_CTL | 0x4000_4094 | [0] AHBWB_SW_RESET (R40, bridge/WB_RST), [1] PFAFIFO1_SW_RESET (R41), default 0 |
| PMU FB_ISOLATION | PMU+0x3F4 | Isolation during config; loaders clear after bitstream (SDK) |

Power the fabric domain before enabling its clocks (TRM p.340). SDK loader: enable clocks, write bitstream via CFG_CTL (0x4001_4000 / data 0x4001_4FFC), exit config, wait, clear FB_ISOLATION, clear FB_SW_RESET and FB_MISC_SW_RST_CTL.

The ADC example runs C16 = 18 MHz as WB_CLK, 1.8× the TRM C40 limit. Keep WB_CLK ≤ 10 MHz in new designs.

## Walkthrough: adc_ad7476_if

Commit 2f8fed632d5bf1196485c5b57de46be4f8341485. Three layers: top wires the macro; IP decodes 4 KB blocks; leaf blocks generate ACK.

- `AL4S3B_FPGA_Top.v`: `WB_CLK = gclkbuff(Sys_Clk0)`, `WB_RST_FPGA = gclkbuff(Sys_Clk0_Rst | WB_RST)`; SDMA ch0 and FB_msg_out[0] to IP.
- `AL4S3B_FPGA_IP.v`: block select `WBs_ADR[16:12] == BASE[16:12] & WBs_CYC`; `WBs_ACK = ACK_FPGA_Reg | ACK_QL_Reserved`; read mux by block, default 0xBAD_FAB_AC.
- `AL4S3B_FPGA_Registers.v`: write decode `(adr == REG[ADDRWIDTH-1:2]) & CYC & STB & WE & ~ACK`, qualified by BYTE_STB[0]; `ACK_nxt = (CYC|CYC_DMA_REG|CYC_DMA_DAT) & STB & ~ACK`; undefined reads 0xFAB_DEF_AC; FIFO_rst self-clearing.
- DMA data port: `WBs_DMA_DAT = CYC_DMA_DAT & STB & ~r1`, registered twice; pop = r1 & ~r2 during the ACK cycle; FIFO (FIFO_16K_BLK, unregistered read) so captured word is pre-pop.
- `AL4S3B_FPGA_QL_Reserved.v`: default-ACK FSM, 3-bit counter from 7, acks if no real ACK by count 1 (~7 WB_CLK). Registers {16'h0, cust_id, prod_id} at 0x1F8, {major, minor} at 0x1FC; else 0xDEF_FAB_AC.
- SDMA: DMA0_Start = (rx_fifo_cnt > 255) & DMA0_EN; Dma_Ctrl raises SDMA_Req[0], cleared async by SDMA_Active or Done; Done clears DMA0_EN and sets DMA0_Done_IRQ; FB_msg_out[0] = IRQ & IRQ_EN.

Register map (IP doc rev 1.0 + RTL):

| Address | Register | Access | Reset |
| --- | --- | --- | --- |
| 0x4002_0000 | IP Device ID | RO | 0x0ADC0001 |
| 0x4002_0004 | Revision | RO | 0x00000100 |
| 0x4002_0008 | FIFO reset bit0 self-clear | W | 0 |
| 0x4002_000C | Sensor enable bit0 | R/W | 0 |
| 0x4002_0010 | Overrun: [31:16] count, [0] sticky (RTL only) | RO | 0 |
| 0x4002_0030/34 | Debug 1/2 (RTL only) | RO | — |
| 0x4003_0000 | DMA CH0 enable bit0, HW clears on done | R/W | 0 |
| 0x4003_0004 | DMA done IRQ status bit0, write 0 to clear | R/W | 0 |
| 0x4003_0008 | DMA done IRQ enable bit0 | R/W | 0 |
| 0x4003_1000 | DMA CH0 data port (RX FIFO) | RO | — |

Data: two 16-bit samples per word, sample 0 in [15:0]. One SPI read = 18 Sys_Clk0 clocks (18 MHz → 1 MSPS).

## Firmware side (qorc-sdk)

```c
#define PERIPH_BASE       (0x40000000)
#define FPGA_PERIPH_BASE  (PERIPH_BASE + 0x00020000)
#define FB_FSDMA_BASE            (FPGA_PERIPH_BASE + 0x10000)  // 0x4003_0000
#define FSDMA_CH0_DATA_REGISTER  (FB_FSDMA_BASE + 0x1000)      // CH1..3 at +0x2000..0x4000
typedef struct { __IO uint32_t FSDMA_ENR, FSDMA_SR, FSDMA_INTEN; } FSDMA_TypeDef;
```

AD7476 driver bring-up: set C16 18 MHz, C21 4 MHz, SDMA clock 72 MHz; configure SDMA channel 12 (FPGA ch0 + 12) from FSDMA_CH0_DATA_REGISTER, no source increment, word transfers; enable NVIC FbMsg_IRQn, FSDMA_INTEN and FSDMA_ENR bit0; FIFO_RESET=1 then SEN_ENR=1; on done clear FSDMA_SR bit0 and re-arm.

Interrupt registers (SDK, INTR_CTRL 0x4000_4800 + 0x80..0x94): FB_INTR, FB_INTR_RAW, FB_INTR_TYPE, FB_INTR_POL, FB_INTR_EN_AP, FB_INTR_EN_M4. `HAL/src/eoss3_hal_wb.c` is the FFE sensor Wishbone master (I2C/SPI0), not the FPGA bridge.

## Other examples

- qorc-sdk qf_advancedfpga: minimal register block, 7-bit word address, per-byte-lane writes.
- s3-gateware ip_modules/UART_16550: read side effects gated with ACK, pop delayed one clock.
- s3-gateware projects/S3_FPGA_2xUART: multiple slaves, ACK OR of four; RTL and timing-sim testbenches.
- s3-gateware ip_modules/GPIO, FLL_I2S: more Wishbone slaves with register-map PDFs.
- EOS-S3-QTplus hw/template: WB_CLK = Sys_Clk1 at 1 MHz; `ack <= cyc & stb` (two-cycle ACK, can double-write; prefer `& ~ack`).
- Simulation: `pp3_cells_sim.v` has qlal4s3b_cell_macro_bfm, bridge model, ahb_gen_bfm tasks `ahb_write_word_al4s3b_fabric` / `ahb_read_word_al4s3b_fabric`.

## Design checklist

- WB_CLK from a fabric clock via gclkbuff, ≤ 10 MHz; fabric domain powered and CRU clock enabled before first access.
- Every address in the window gets an ACK (ack-all slaves or default-ACK timer).
- ACK one-clock pulse; write enables include ~ACK.
- Only one slave ACKs per access.
- Writes honour WBs_BYTE_STB; data in natural lane.
- Read data valid on ACK edge; side effects on/after it.
- Reset from WB_RST (optionally | Sys_Clk0_Rst) through gclkbuff.
- Synchronise other clock domains into WB_CLK yourself.
- Use SDMA or packet FIFO for bulk data.
- Tie off unused macro inputs; FBIO pins via .pcf.
- Custom FPGA image replaces QuickFeather USB-serial gateware; use hardware UART for console.

## Gaps

- TRM does not specify the bus protocol (27.2.4 is one paragraph; 27.4 points to IOMUX; 27.3.1 "[discussion to be added]").
- ADC example exceeds WB_CLK limit (18 MHz vs 10 MHz).
- C41 maximum inconsistent in TRM.
- No SDMA channel map in TRM; FPGA ch0 = SDMA ch12 from driver; 13–15 inferred.
- No FPGA interrupt register detail in TRM.
- WBs_RD unused in all examples.
- ADC PDF omits registers at 0x10, 0x30, 0x34 that exist in RTL.
