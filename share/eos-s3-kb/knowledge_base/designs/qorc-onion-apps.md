---
title: "qorc-onion-apps — EOS S3 eFPGA + M4 example designs (overview)"
source: "https://github.com/coolbreeze413/qorc-onion-apps"
source_commit: a960ca3f450fafde9da07547b35efe8e1caa2574 (2022-04-21)
license: "Unlicense (public domain)"
type: "design-summary"
topic: "FPGA Wishbone interface / eFPGA designs"
board: "QuickFeather (PU64); some apps also target OptimusLogic Pygmy boards"
added: 2026-10-09
---

# qorc-onion-apps — overview

"Experimental stuff that can be run with the QORC SDK" by coolbreeze413: 17 apps for the EOS S3 covering bootloaders, project templates, standalone FPGA designs, M4-controlled FPGA peripherals over Wishbone (GPIO, PWM, breathe, timer with interrupt), a composite design combining them, and dynamic FPGA reloading. Each app has makefile targets for clean/build/flash/load (J-Link/OpenOCD) and VS Code configs.

Files: [`source_code_knowledge/designs/qorc-onion-apps/`](<../../source_code_knowledge/designs/qorc-onion-apps/README.md>) (repo README and every app README converted to Markdown; RTL, C, PCF, makefiles, scripts, VS Code and OpenOCD configs kept as-is).

Related: [Wishbone reference notes](<../wishbone/EOS_S3_Wishbone_Reference_Notes.md>), [S3_FPGA_2xUART_GPIO](<S3_FPGA_2xUART_GPIO.md>), [GPIO register map (QuickLogic)](<../GPIO_register_map.md>).

## Apps

| App | Kind | FPGA | M4 | What it shows |
|---|---|:-:|:-:|---|
| [qorc_loadflash_dual](<../../source_code_knowledge/designs/qorc-onion-apps/qorc_loadflash_dual/README.md>) | Flashloader | usb2serial | ✓ | Preps a new board: flashes bootloader, boot FPGA, app FPGA, M4 app over USB-serial **or** UART IO_44/IO_45 |
| [qorc_bootloader_dual](<../../source_code_knowledge/designs/qorc-onion-apps/qorc_bootloader_dual/README.md>) | Bootloader | usb2serial | ✓ | Flash/load M4 + FPGA images from SPI flash; listens on USB-serial and UART |
| [qorc_bootloader_cli](<../../source_code_knowledge/designs/qorc-onion-apps/qorc_bootloader_cli/README.md>) | Bootloader | usb2serial | ✓ | Menu-driven bootloader CLI on USB-serial (**marked unstable**) |
| [qorc_helloworldm4](<../../source_code_knowledge/designs/qorc-onion-apps/qorc_helloworldm4/README.md>) | Template | — | ✓ | M4 only |
| [qorc_helloworldfpga](<../../source_code_knowledge/designs/qorc-onion-apps/qorc_helloworldfpga/README.md>) | Template | ✓ | — | FPGA only (LED blink, standalone FPGA binary) |
| [qorc_helloworldm4fpga](<../../source_code_knowledge/designs/qorc-onion-apps/qorc_helloworldm4fpga/README.md>) | Template | ✓ | ✓ | M4 + FPGA, separate binaries, no M4↔FPGA communication |
| [qorc_helloworldm4fpgaheader](<../../source_code_knowledge/designs/qorc-onion-apps/qorc_helloworldm4fpgaheader/README.md>) | Template | ✓ | ✓ | Same, FPGA bitstream compiled into the M4 binary as a C header (legacy) |
| [qorc_fpga_pwm](<../../source_code_knowledge/designs/qorc-onion-apps/qorc_fpga_pwm/README.md>) | FPGA standalone | ✓ | — | 8-bit PWM on the RGB LED |
| [qorc_fpga_breathe](<../../source_code_knowledge/designs/qorc-onion-apps/qorc_fpga_breathe/README.md>) | FPGA standalone | ✓ | — | LED "breathing" (PWM ramp up/down), cycles colours |
| [qorc_fpga_gpioctrl](<../../source_code_knowledge/designs/qorc-onion-apps/qorc_fpga_gpioctrl/README.md>) | FPGA + M4 | ✓ | ✓ | Control all IO pads from the M4 through an FPGA GPIO block |
| [qorc_fpga_pwmctrl](<../../source_code_knowledge/designs/qorc-onion-apps/qorc_fpga_pwmctrl/README.md>) | FPGA + M4 | ✓ | ✓ | PWM block configured from the M4 |
| [qorc_fpga_breathectrl](<../../source_code_knowledge/designs/qorc-onion-apps/qorc_fpga_breathectrl/README.md>) | FPGA + M4 | ✓ | ✓ | Breathe block configured from the M4 |
| [qorc_fpga_timerctrl](<../../source_code_knowledge/designs/qorc-onion-apps/qorc_fpga_timerctrl/README.md>) | FPGA + M4 | ✓ | ✓ | One-shot timer → **FPGA interrupt to M4** (FB_INTERRUPT_0) |
| [qorc_fpga_compositeGPBTctrl](<../../source_code_knowledge/designs/qorc-onion-apps/qorc_fpga_compositeGPBTctrl/README.md>) | FPGA + M4 | ✓ | ✓ | All four blocks in one design, sharing the IO pads |
| [qorc_fpgareload_flash](<../../source_code_knowledge/designs/qorc-onion-apps/qorc_fpgareload_flash/README.md>) | Experimental | ✓ | ✓ | Load different FPGA bitstreams from SPI flash at run time (**unstable**) |
| [qorc_fpgareload_header](<../../source_code_knowledge/designs/qorc-onion-apps/qorc_fpgareload_header/README.md>) | Experimental | ✓ | ✓ | Same, bitstreams built into the M4 binary (**unstable**) |
| [qorc_pygmy_test](<../../source_code_knowledge/designs/qorc-onion-apps/qorc_pygmy_test/README.md>) | Test | — | ✓ | Peripheral tests for OptimusLogic Pygmy-based boards (BMA400 etc.) |

## Wishbone controller designs (gpioctrl / pwmctrl / breathectrl / timerctrl / composite)

All five use the same layout, so addresses are the same whether a block is used alone or in the composite design.

### Memory map (M4 addresses, `FPGA_PERIPH_BASE` = 0x4002_0000)

| M4 address | Block | Registers (offset: name) |
|---|---|---|
| 0x4002_1000 | GPIO controller | +0x0 GPIO_IN (RO, pad values) · +0x4 GPIO_OUT · +0x8 GPIO_OE (1 = drive) — bit *n* = IO_*n* |
| 0x4002_2000 | PWM controller | +0x0 PWM_0_CONFIG (red, IO_22) · +0x4 PWM_1_CONFIG (green, IO_21) · +0x8 PWM_2_CONFIG (blue, IO_18) |
| 0x4002_3000 | Breathe controller | +0x0 BREATHE_0_CONFIG (IO_22) · +0x4 BREATHE_1_CONFIG (IO_21) · +0x8 BREATHE_2_CONFIG (IO_18) |
| 0x4002_4000 | Timer controller | +0x0 TIMER_0_CONFIG |
| 0x4002_5000 | QL reserved | +0x1F8 customer/product ID, +0x1FC revisions; default-ACK timer for unclaimed addresses |
| other | — | reads 0xBAD_FAB_AC |

Undefined offsets inside a block read 0xDEF_FAB_AC. Blocks are decoded on `WBs_ADR[16:10]`, so each occupies 1 KB at its base (e.g. 0x1000–0x13FF); the rest of each 4 KB slot falls to the default-ACK timer.

### Config register formats (from RTL)

| Register | Bit 31 | Low bits | Reset value |
|---|---|---|---|
| PWM_n_CONFIG | 1 = run, 0 = held in reset (output Z) | [7:0] duty cycle (0–255, output high while counter ≤ duty) | 0 |
| BREATHE_n_CONFIG | 1 = run, 0 = reset (output Z) | [23:0] clock cycles per brightness step | 0xAAAA (bit 31 = 0, so off) |
| TIMER_0_CONFIG | 1 = run, 0 = reset/clear | [30:0] period in clock cycles; one-shot, output (= interrupt) goes high at expiry and stays high until bit 31 is cleared | 0 |
| GPIO_OUT / GPIO_OE | — | 32 bits, one per IO pad | 0 |

### Device IDs

Each design sets the 16-bit `Device_ID` on the cell macro, read by firmware at `MISC_CTRL_BASE + 0x3FC` (`hal_fpga_onion_get_device_id()`):

| Design | Device ID |
|---|---|
| gpioctrl | 0xC001 |
| pwmctrl | 0xC002 |
| breathectrl | 0xC004 |
| timerctrl | 0xC008 |
| compositeGPBTctrl | 0xC00F (bit-OR of the four) |

### Clocks, reset, interrupts, pins

- `WB_CLK = gclkbuff(Sys_Clk0)`; the PWM/breathe/timer logic also runs on `Sys_Clk0` (C16). Reset = `Sys_Clk0_Rst | WB_RST`.
- Firmware (`src/s3x_pwrcfg.c`) sets **C16 = 12 MHz** and C21 = 48 MHz. 12 MHz is above the TRM's 10 MHz WB_CLK limit (see the Wishbone notes); it works on the author's boards.
- Interrupt: timerctrl and composite drive `FB_msg_out[0]` from the timer → `FB_INTERRUPT_0`. Firmware: `FB_RegisterISR(FB_INTERRUPT_0, …)`, `NVIC_EnableIRQ(FbMsg_IRQn)`; the ISR clears the timer by writing bit 31 = 0. Other designs tie `FB_msg_out` to 0.
- Pins: the controller designs expose `io_pad[31:0]` mapped 1:1 to IO_0–IO_31 in `quickfeather.pcf`, **except IO_14/IO_15** (commented out — SWD). The standalone designs use only `red_led` IO_22, `green_led` IO_21, `blue_led` IO_18.
- Composite pad sharing: `io_pad = GPIO | PWM | BREATHE` (bitwise OR). PWM and breathe drive only bits 22/21/18, and are Z while their bit 31 is 0; use only one block per LED pad at a time.

### Wishbone pattern (same as QuickLogic's examples)

- Writes: `addr match & CYC & STB & WE & ~ACK`, byte-lane writes per `WBs_BYTE_STB`.
- ACK: `CYC & STB & ~ACK` (one-cycle pulse), ACKs ORed in the IP; read data from a combinational mux on `WBs_ADR`.
- Only the GPIO block resets its ACK flop on `WB_RST`; PWM/breathe/timer leave `WBs_ACK_o` out of the reset branch (harmless in practice, ACK self-clears after one cycle).

## Firmware HAL (per app, `fpga/inc` + `fpga/src`)

`hal_fpga_onion.c/.h` (device ID, Wishbone test) plus one file per block: `hal_fpga_onion_gpioctrl` (`set_output(pad, val)`, `set_input(pad)`, `get_value(pad)`), `hal_fpga_onion_pwmctrl` (`enable(pad, duty)`, `disable`, `getval`), `hal_fpga_onion_breathectrl` (`enable(pad, period)`, …), `hal_fpga_onion_timerctrl` (`enable(id, period)`, ISR setup). The apps expose these through CLI sub-menus `gpioctrl`, `pwmctrl`, `breathectrl`, `timerctrl`.

## What was copied

- 1,069 files (≈7 MB) from commit `a960ca3`, in `source_code_knowledge/designs/qorc-onion-apps/`.
- All 18 `README.rst` files converted to `README.md` (with front matter; links between apps point to the converted READMEs).
- **Left out (64 files):** compiled binaries (`.bin`, `.elf`, `.map`), SpDE `.chp` project dumps, build logs/temp files, `.gitignore`, and 13 generated bitstream arrays (`*_bit.h`, `firmware_raw_image.h`, `usb2serial_bitstream.c`). Rebuild them from the RTL, or get them from the GitHub repo.
- Not checked: none of the designs were rebuilt or simulated here.
