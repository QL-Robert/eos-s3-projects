---
title: "EOS S3 Wishbone \u2014 Registers, Signals and Clock Limits"
source_file: "eos-s3-wishbone-mcp/src/eos_s3_wishbone_mcp/knowledge/data.py"
type: "notes"
topic: "FPGA Wishbone interface"
added: 2026-10-09
sha256: ef89b0e0b871cf130759e33db32f87f9cf7796b43e65fd50d349db6605b85442
---

# EOS S3 Wishbone — Registers, Signals and Clock Limits

Generated from the structured data in the eos-s3-wishbone-mcp server (`knowledge/data.py`). Page numbers refer to EOS S3 TRM r1.01a. Narrative explanation: [EOS_S3_Wishbone_Reference_Notes.md](<EOS_S3_Wishbone_Reference_Notes.md>).

- FPGA Wishbone window: **0x40020000**, size 0x00020000 (128 KB)
- CRU base: 0x40004000

## Clock limits

| Clock | Name | Max | Source |
|---|---|---:|---|
| C16 | Sys_Clk0 | 72 MHz | TRM p.90 |
| C21 | Sys_Clk1 | 72 MHz | TRM p.90 |
| C02 | Sys_Pclk | 40 MHz | TRM p.89 (C02 domain) |
| C09 | CFG_CTL APB (configuration) | 10 MHz | TRM p.89 |
| C40 | WB_CLK (fabric -> AHB-to-Wishbone bridge) | 10 MHz | TRM p.90, p.340 |
| C41 | Sys_PKfb_Clk (fabric -> packet FIFO 1) | 10 MHz | TRM p.341 says 10 MHz; clock table p.90 says 20 MHz (inconsistent, 10 MHz used) |

## Registers

### FB_SW_RESET

- **Block:** CRU
- **Address:** 0x40004088
- **Access:** RW
- **Reset:** 0x3F
- **Source:** TRM p.105 Table 11-30
- **Notes:** Write 1 asserts reset immediately; write 0 releases synchronously even with the clock gated.

| Bits | Meaning |
|---|---|
| 0 | FB_C02_DOMAIN_SW_RESET (default 1) |
| 1 | general purpose (default 1) |
| 2 | FB_C09_DOMAIN_SW_RESET (default 1) |
| 3 | general purpose (default 1) |
| 4 | FB_C16_DOMAIN_SW_RESET (default 1) |
| 5 | FB_C21_DOMAIN_SW_RESET (default 1) |

### FB_MISC_SW_RST_CTL

- **Block:** CRU
- **Address:** 0x40004094
- **Access:** RW
- **Reset:** 0x0
- **Source:** TRM p.106 Table 11-33
- **Notes:** Firmware must clear the bit manually after setting it.

| Bits | Meaning |
|---|---|
| 0 | AHBWB_SW_RESET - reset path R40, the AHB-to-Wishbone bridge (WB_RST) |
| 1 | PFAFIFO1_SW_RESET - reset path R41, packet FIFO 1 (Sys_PKfb_Rst) |

### CLK_Control_F_0

- **Block:** CRU
- **Address:** 0x40004020
- **Access:** RW
- **Reset:** —
- **Source:** TRM p.341
- **Notes:** C16 (Sys_Clk0) divider.

### CLK_Control_F_1

- **Block:** CRU
- **Address:** 0x40004024
- **Access:** RW
- **Reset:** —
- **Source:** TRM p.341
- **Notes:** C16 (Sys_Clk0) source select.

### CLK_Control_I_0

- **Block:** CRU
- **Address:** 0x40004034
- **Access:** RW
- **Reset:** —
- **Source:** TRM p.341
- **Notes:** C21 (Sys_Clk1) divider.

### CLK_Control_I_1

- **Block:** CRU
- **Address:** 0x40004038
- **Access:** RW
- **Reset:** —
- **Source:** TRM p.341
- **Notes:** C21 (Sys_Clk1) source select (TRM text misprints it as CLK_Control_F_1).

### C16_CLK_GATE

- **Block:** CRU
- **Address:** 0x40004064
- **Access:** RW
- **Reset:** —
- **Source:** TRM p.104, p.341

| Bits | Meaning |
|---|---|
| 0 | 1 = enable Sys_Clk0 |

### C21_CLK_GATE

- **Block:** CRU
- **Address:** 0x40004070
- **Access:** RW
- **Reset:** —
- **Source:** TRM p.104, p.341

| Bits | Meaning |
|---|---|
| 0 | 1 = enable Sys_Clk1 |

### C02_CLK_GATE

- **Block:** CRU
- **Address:** 0x40004044
- **Access:** RW
- **Reset:** —
- **Source:** TRM p.341

| Bits | Meaning |
|---|---|
| 1 | 1 = enable Sys_Pclk |

### C09_CLK_DIV

- **Block:** CRU
- **Address:** 0x40004114
- **Access:** RW
- **Reset:** —
- **Source:** TRM p.341
- **Notes:** Divider and root gate for C09 (configuration clock).

### C09_CLK_GATE

- **Block:** CRU
- **Address:** 0x40004118
- **Access:** RW
- **Reset:** —
- **Source:** TRM p.341
- **Notes:** Write 0x6 before loading a bitstream.

### CLK_DIVIDER_CLK_GATING

- **Block:** CRU
- **Address:** 0x40004124
- **Access:** RW
- **Reset:** —
- **Source:** TRM p.341
- **Notes:** Must be 1 for the fabric input clocks.

| Bits | Meaning |
|---|---|
| 1 | C02 divider master gate |
| 5 | C16 divider master gate |
| 8 | C21 divider master gate |

### CFG_CTL

- **Block:** CFG_CTL_TOP (PIF)
- **Address:** 0x40014000
- **Access:** RW
- **Reset:** —
- **Source:** TRM p.41 memory map; qorc-sdk fpga_loader.c
- **Notes:** 0xBDFF enters configuration mode; 0 exits. Bitstream words go to 0x4001_4FFC.

### FB_ISOLATION

- **Block:** PMU
- **Address:** —
- **Access:** RW
- **Reset:** 0x1
- **Source:** qorc-sdk eoss3_dev.h, fpga_loader.c
- **Notes:** PMU offset 0x3F4. Cleared by loaders after configuration.

| Bits | Meaning |
|---|---|
| 0 | 1 = fabric isolated |

### FB_INTR / FB_INTR_RAW / FB_INTR_TYPE / FB_INTR_POL / FB_INTR_EN_AP / FB_INTR_EN_M4

- **Block:** INTR_CTRL
- **Address:** 0x40004880
- **Access:** RW
- **Reset:** —
- **Source:** qorc-sdk eoss3_dev.h (not in TRM text)
- **Notes:** Offsets 0x80-0x94 from INTR_CTRL (0x4000_4800). FB_INTERRUPT_0..3 = FB_msg_out[3:0]; NVIC line FbMsg_IRQn.

### ADC IP Device ID

- **Block:** adc_ad7476_if
- **Address:** 0x40020000
- **Access:** RO
- **Reset:** 0x0ADC0001
- **Source:** ADC IP doc rev 1.0; AL4S3B_FPGA_Registers.v

### ADC Revision

- **Block:** adc_ad7476_if
- **Address:** 0x40020004
- **Access:** RO
- **Reset:** 0x100
- **Source:** ADC IP doc

### ADC FIFO reset

- **Block:** adc_ad7476_if
- **Address:** 0x40020008
- **Access:** W
- **Reset:** 0x0
- **Source:** ADC IP doc

| Bits | Meaning |
|---|---|
| 0 | 1 = flush RX FIFO (self-clearing) |

### ADC Sensor enable

- **Block:** adc_ad7476_if
- **Address:** 0x4002000C
- **Access:** RW
- **Reset:** 0x0
- **Source:** ADC IP doc

| Bits | Meaning |
|---|---|
| 0 | 1 = start reading the ADC |

### ADC FIFO overrun

- **Block:** adc_ad7476_if
- **Address:** 0x40020010
- **Access:** RO
- **Reset:** 0x0
- **Source:** AL4S3B_FPGA_Registers.v
- **Notes:** RTL only, not in the PDF.

| Bits | Meaning |
|---|---|
| 31:16 | overrun count |
| 0 | sticky overrun flag |

### ADC Debug 1

- **Block:** adc_ad7476_if
- **Address:** 0x40020030
- **Access:** RO
- **Reset:** —
- **Source:** AL4S3B_FPGA_Registers.v
- **Notes:** {6'h0, rx_fifo_cnt, pop_flag, 2'b00, full, empty}. RTL only.

### ADC Debug 2

- **Block:** adc_ad7476_if
- **Address:** 0x40020034
- **Access:** RO
- **Reset:** —
- **Source:** AL4S3B_FPGA_Registers.v
- **Notes:** FSM states and DMA handshake bits. RTL only.

### FSDMA_ENR (DMA enable)

- **Block:** adc_ad7476_if
- **Address:** 0x40030000
- **Access:** RW
- **Reset:** 0x0
- **Source:** ADC IP doc; eoss3_hal_fpga_sdma_reg.h

| Bits | Meaning |
|---|---|
| 0 | DMA CH0 enable; hardware clears on done |

### FSDMA_SR (DMA status)

- **Block:** adc_ad7476_if
- **Address:** 0x40030004
- **Access:** RW
- **Reset:** 0x0
- **Source:** ADC IP doc

| Bits | Meaning |
|---|---|
| 0 | DMA done interrupt; write 0 to clear |

### FSDMA_INTEN (DMA interrupt enable)

- **Block:** adc_ad7476_if
- **Address:** 0x40030008
- **Access:** RW
- **Reset:** 0x0
- **Source:** ADC IP doc

| Bits | Meaning |
|---|---|
| 0 | DMA done interrupt enable |

### FSDMA_CH0_DATA_REGISTER

- **Block:** adc_ad7476_if
- **Address:** 0x40031000
- **Access:** RO
- **Reset:** —
- **Source:** ADC IP doc; eoss3_hal_fpga_ad7476.c
- **Notes:** Read pops one word of the 512x32 RX FIFO. SDMA channel 12 reads it with no address increment.

### QL reserved customer/product ID

- **Block:** adc_ad7476_if
- **Address:** 0x400321F8
- **Access:** RO
- **Reset:** —
- **Source:** AL4S3B_FPGA_QL_Reserved.v

| Bits | Meaning |
|---|---|
| 15:8 | customer ID |
| 7:0 | product ID |

### QL reserved revisions

- **Block:** adc_ad7476_if
- **Address:** 0x400321FC
- **Access:** RO
- **Reset:** —
- **Source:** AL4S3B_FPGA_QL_Reserved.v

| Bits | Meaning |
|---|---|
| 31:16 | major revision |
| 15:0 | minor revision |

## qlal4s3b_cell_macro signals

Direction is from the fabric's point of view.

| Port | Width | Dir | Behaviour |
|---|---:|---|---|
| `WBs_ADR` | 17 | in | Byte address in the 128 KB window; registered from HADDR[16:0], stable for the whole cycle. |
| `WBs_CYC` | 1 | in | Cycle valid. Asserted with STB and cleared on the WB_CLK edge where the bridge samples ACK=1. |
| `WBs_STB` | 1 | in | Transfer strobe; always asserted together with CYC by this bridge. |
| `WBs_WE` | 1 | in | 1 = write. |
| `WBs_RD` | 1 | in | 1 = read (~WE during a cycle). Non-standard; QuickLogic examples ignore it. |
| `WBs_BYTE_STB` | 4 | in | Byte lanes from HSIZE and HADDR[1:0]; data is not shifted. |
| `WBs_WR_DAT` | 32 | in | Write data, wired from HWDATA; valid while CYC/STB are high. |
| `WBs_RD_DAT` | 32 | out | Read data; captured on the WB_CLK edge where ACK is high. |
| `WBs_ACK` | 1 | out | Cycle complete. Must be a single-cycle pulse; no bridge timeout if it never comes. |
| `WB_CLK` | 1 | out | Bus clock (CRU C40) driven by the fabric into the bridge. Max 10 MHz (TRM p.340). |
| `WB_RST` | 1 | in | Bridge reset from CRU FB_MISC_SW_RST_CTL[0] AHBWB_SW_RESET. |
| `Sys_Clk0` | 1 | in | CRU C16 into the fabric (max 72 MHz). |
| `Sys_Clk0_Rst` | 1 | in | Reset for the C16 domain (FB_SW_RESET[4]). |
| `Sys_Clk1` | 1 | in | CRU C21 into the fabric (max 72 MHz). |
| `Sys_Clk1_Rst` | 1 | in | Reset for the C21 domain (FB_SW_RESET[5]). |
| `Sys_Pclk` | 1 | in | CRU C02 into the fabric; clocks the SPI-master APB port. |
| `SDMA_Req` | 4 | out | SDMA burst request, one bit per FPGA DMA channel (FPGA ch0 = SDMA ch12 per SDK). |
| `SDMA_Sreq` | 4 | out | SDMA single request per FPGA DMA channel. |
| `SDMA_Done` | 4 | in | SDMA channel done. |
| `SDMA_Active` | 4 | in | SDMA channel active. |
| `FB_msg_out` | 4 | out | Interrupts to the M4: FB_INTERRUPT_0..3 (TRM p.52: 4 fabric outputs). |
| `FB_Int_Clr` | 8 | out | Interrupt clear inputs; tied to 0 in all examples. |
| `Device_ID` | 16 | out | Design ID readable by software. |
| `Sys_PKfb_Clk` | 1 | out | Packet FIFO push clock (CRU C41). |
| `FB_PKfbData` | 32 | out | Packet FIFO push data. |
| `FB_PKfbPush` | 4 | out | Packet FIFO push strobes, one per FIFO. |

## Example RTL files (QuickLogic s3-gateware @ `2f8fed63`)

Local copy: `source_code_knowledge/s3-gateware/` (from your qorc-sdk; may be a different revision than the pinned commit).

| File | Path in s3-gateware | Local copy |
|---|---|---|
| AL4S3B_FPGA_IP.v | `adc_ad7476_if/rtl/AL4S3B_FPGA_IP.v` | yes |
| AL4S3B_FPGA_QL_Reserved.v | `adc_ad7476_if/rtl/AL4S3B_FPGA_QL_Reserved.v` | yes |
| AL4S3B_FPGA_Registers.v | `adc_ad7476_if/rtl/AL4S3B_FPGA_Registers.v` | yes |
| AL4S3B_FPGA_Top.v | `adc_ad7476_if/rtl/AL4S3B_FPGA_Top.v` | yes |
| Dma_Ctrl.v | `adc_ad7476_if/rtl/Dma_Ctrl.v` | yes |
| Fsm_Top.v | `adc_ad7476_if/rtl/Fsm_Top.v` | yes |
| Generic_tb_AL4S3B_FPGA_IP.v | `adc_ad7476_if/testbench/Generic_tb_AL4S3B_FPGA_IP.v` | yes |
| S3_FPGA_2xUART_IP.v | `projects/S3_FPGA_2xUART/rtl/AL4S3B_FPGA_IP.v` | yes |
| Serializer_Deserializer.v | `adc_ad7476_if/rtl/Serializer_Deserializer.v` | yes |
| UART_16550_Registers.v | `ip_modules/UART_16550/rtl/UART_16550_Registers.v` | yes |
| pp3_cells_sim.v | `adc_ad7476_if/testbench/pp3_cells_sim.v` | yes |
