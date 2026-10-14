---
title: "SparkFun QuickLogic Thing Plus - EOS S3 (QuickThing Plus) - board reference"
type: board-reference
topic: QuickThing Plus hardware, pins, connectors, boot, programming, differences from QuickFeather
added: 2026-10-11
sources: QTPLUS_R8 schematic (SparkFun_QuickLogic_ThingPlus_EOS-S3_R8_Schematic.md, OCR'd); SparkFun "QuickLogic Thing Plus (EOS S3) Hookup Guide"; QORC SDK (qt_apps, BSP, qt-initial-binaries README); datasheet v3.3d Table 31
---

# SparkFun QuickLogic Thing Plus - EOS S3 ("QuickThing Plus")

A SparkFun Thing Plus-format board (Feather-compatible footprint, 2.75" x 2.10") around the QuickLogic **EOS S3** (Cortex-M4F + eFPGA), supported by the QORC SDK as `qt_apps`. The schematic title is "QuickThing+", revision R8, dated October 2020 (design by Optimus Logic Systems). SparkFun marks the product as **retired** on its hookup guide.

**Package: 64-ball BGA** (the schematic symbol is `EOS_S3B_VBGA64`), so the `ql_symbiflow` package is `-P PD64` and PCF ball names are the BGA balls (`G7`, `H7`, ...), not QFN pin numbers. The QuickFeather is the one with the QFN (`PU64`). IO aliases (`IO_22`) work on both.

## What is on the board

| Item | Detail |
|---|---|
| MCU / FPGA | QuickLogic EOS S3, VBGA64 |
| Flash | 16 Mbit (2 MB) SPI NOR, GigaDevice GD25Q16C, on the SPI master bus (IO_34/36/38, chip select IO_39) |
| Accelerometer | ST LIS2DH12, 3-axis, 12-bit, I2C address 0x18, INT1 on IO_3 |
| Microphone | Vesper VM3011 PDM MEMS mic (left channel); data IO_28, clock IO_29, config on I2C0, INT net on IO_12. A hole through the PCB is the sound port |
| RGB LED | Blue IO_18, green IO_21, red IO_22 (driven through MOSFETs; not routed to headers) |
| Buttons | User button on IO_6 (also on J8.10); reset button on SYS_RSTn (also on the SWD header) |
| Power | USB-C (J5) 5 V, or single Li-Po (JST-PH) via MCP73831 charger (default charge current about 212 mA). 3.3 V from a TPS62821 buck converter; 3V3 enable pin broken out |
| Battery monitor | Divider into ADC0, enabled by IO_26 (`ADC0_EN`) |
| Clock | 32.768 kHz crystal |
| Qwiic | Connector J4 on I2C0 (IO_0 SCL / IO_1 SDA), shared with the accelerometer and mic configuration |
| Debug | 10-pin SWD header J7 (SWD CLK IO_14, SWD IO IO_15, SYS_RSTn, 3.3 V, GND) |
| Logic level | 3.3 V only |

Connector designators follow the schematic: J1 = battery, J4 = Qwiic, J5 = USB-C, J6 = 16-pin header, J7 = SWD, J8 = 18-pin header, J9 = 12-pin header, J2/J3 = two 2-pin boot-strap shunts.

## Headers (SparkFun hookup guide; BGA balls verified against the datasheet)

### J9 (12 pins; the guide's table header calls it "J2")

| Pin | EOS S3 IO | Function |
|---|---|---|
| 1 | - | VBAT |
| 2 | - | 3.3 V circuit enable |
| 3 | - | VBUS |
| 4 | IO_27 | GPIO; SPI master CS2 |
| 5 | IO_20 | SPI peripheral CSn input; boot-strap |
| 6 | IO_19 | SPI peripheral COPI input; boot-strap |
| 7 | IO_17 | SPI peripheral CIPO output |
| 8 | IO_16 | SPI peripheral CLK input |
| 9 | IO_43 | Interrupt output to host |
| 10 | IO_3 | Accelerometer interrupt |
| 11 | IO_0 | I2C0 SCL |
| 12 | IO_1 | I2C0 SDA |

### J6 (16 pins)

| Pin | EOS S3 IO | Function |
|---|---|---|
| 1 | - | GND |
| 2 | IO_44 | UART TX |
| 3 | IO_45 | UART RX |
| 4 | IO_36 | SPI master CIPO |
| 5 | IO_38 | SPI master COPI |
| 6 | IO_34 | SPI master CLK |
| 7 | IO_2 | GPIO |
| 8 | IO_13 | GPIO |
| 9 | IO_25 | GPIO |
| 10 | IO_30 | GPIO |
| 11 | ADC1 | ADC1 input |
| 12 | - | no connect |
| 13 | - | GND |
| 14 | - | no connect |
| 15 | - | +3.3 V |
| 16 | SYS_RSTn | Hardware reset input |

### J8 (18 pins)

| Pin | EOS S3 IO | Function |
|---|---|---|
| 1 | IO_28 | PDM mic data |
| 2 | IO_29 | PDM mic clock |
| 3 | IO_23 | I2S peripheral WCLK input |
| 4 | IO_24 | I2S peripheral data output |
| 5 | IO_31 | I2S peripheral CLK input |
| 6 | IO_11 | GPIO |
| 7 | IO_12 | GPIO |
| 8 | IO_4 | GPIO |
| 9 | IO_5 | GPIO |
| 10 | IO_6 | User button input |
| 11 | IO_7 | GPIO |
| 12 | IO_8 | GPIO |
| 13 | IO_10 | GPIO |
| 14 | IO_35 | GPIO |
| 15, 17 | - | +3.3 V |
| 16, 18 | - | GND |

### J7 (10-pin SWD)

| Pin | Signal |
|---|---|
| 1 | +3.3 V |
| 2 | SWD IO (IO_15) |
| 3, 5, 9 | GND |
| 4 | SWD CLK (IO_14) |
| 6-8 | no connect |
| 10 | SYS_RSTn |

The ball names printed in the SparkFun tables match the datasheet BGA ball column (for example IO_22 = G7, IO_44 = E1), which confirms the BGA package.

## Boot-strap shunts (J2 / J3)

IO_19 and IO_20 are boot-strap pins. SparkFun: **install both shunts to debug over SWD, remove both to boot from flash** (the flash must hold a valid boot image). Do not assign these two pads to fabric logic if you need to switch modes.

## Programming and recovery

- **Pre-loaded demo:** a UART terminal (PuTTY) with `diag` and `help` commands tests the LED and button.
- **J-Link over SWD (hookup guide):** fit the shunts, connect the 10-pin cable and run J-Link Commander with a command file (FPGA only, or FPGA + M4).
- **Factory restore (QORC SDK `qt-initial-binaries/README.md`):** the three manufacturing binaries are `qt_bootloader.bin` (bootloader), `qt_bootfpga.bin` (FPGA image used by the bootloader; it is `s3-gateware/usb2serial/usb2serial.bin`) and `qt_helloworldsw.bin` (first M4 app). To recover a "bricked" board, load and run `qt_loadflash.bin` with J-Link, then run `python3 TinyFPGA-Programmer-Application/tinyfpga-programmer-gui --port COMXXX --mfgpkg qt-initial-binaries`.
- The QuickThing Plus apps in the SDK (`qt_apps`): `qt_bootloader`, `qt_loadflash`, `qt_helloworldsw`, `qt_ssi_ai_app`. Build with `make` in each `GCC_Project`; `make qt_mfgpkg` in `qt_apps` collects the factory set.
- The local `QuickThingPlus/TinyFPGA-Programmer-Application` folder is the programmer tool (its board PDFs are in this knowledge base as `TinyFPGA-A-Programmer.md` and `TinyFPGA-B.md`).

## Differences from QuickFeather

| | QuickFeather | QuickThing Plus |
|---|---|---|
| Package / `-P` | QFN64 / `PU64` | BGA64 / `PD64` |
| Accelerometer | mCube MC3635 | ST LIS2DH12 |
| Other sensors | Infineon DPS310 pressure, IM69D130 PDM mic | Vesper VM3011 PDM mic |
| USB connector | Micro-USB | USB-C (schematic part USB4105) |
| Extras | | Qwiic, battery-voltage monitor (IO_26), SPI peripheral and I2S pins on headers |
| Debug header | J6 | J7 (10-pin) |
| LEDs, button, UART, SWD, I2C0, PDM pins | same IO numbers | same IO numbers (IO_18/21/22, IO_6, IO_44/45, IO_14/15, IO_0/1, IO_28/29) |

In the QORC SDK the two boards share the **same BSP** (`BSP/quickfeather`), the same linker script contents (`thingplus.ld` is identical to `quickfeather.ld`) and the same flash map (2 MB, see `QuickFeather.md`). The `qt_helloworldsw` and `qf_helloworldsw` sources differ only in version strings and banner text, plus a comment in `pincfg_table.c`.

## Using the eFPGA on QuickThing Plus

- Use `-P PD64`. Prefer `IO_x` aliases in the PCF (`set_io redled IO_22`, `greenled IO_21`, `blueled IO_18`) so the same file works on both boards. In BGA spelling the LEDs are red G7, green H7, blue E8.
- The QORC example PCFs are written for QuickFeather; the LED and UART IO numbers carry over, other pads do not. Check the table in `EOS_S3_IO_Package_Map.md`.
- Keep IO_14 / IO_15 (SWD) and IO_19 / IO_20 (boot-strap) out of the PCF unless you accept losing debug or boot-mode selection.
- Wishbone window `0x4002_0000`-`0x4003_FFFF` and all FPGA rules are the same as on QuickFeather (see `wishbone/`, `EOS_S3_FPGA_Design_Flow.md`).

## Source conflicts and cautions

- The hookup guide labels the 12-pin header "J9" in the heading and "J2" in the table, and calls the battery connector "J4". The schematic shows J9 = 12-pin header, J1 = battery, J4 = Qwiic. This document follows the schematic.
- The hookup guide's text mentions both "Type-C" and "micro USB" cables and refers to the SWD header as J6 in one step and J7 in another. The schematic shows a USB-C receptacle and J7 as the SWD header.
- The guide's own IO map lists IO_14 and IO_36 on J6 pin 4 and IO_15 and IO_44 on J6 pin 2, which conflicts with its J6 table (and with the SWD header J7). Trust the J6 / J7 tables above and verify on the board.
- The OCR of the R8 schematic scrambles ball labels beside net names. Use the datasheet for ball locations and the schematic only for net names and part numbers. The OCR reads the flash as `GD25Q16CWIGR`; the guide says `GD25Q16CEIGR`.
- Net names in the schematic that have no header pin identified here: `S3IO_9`, GPIO 32, 33, 37 and 40-42. The USB D+/D- nets connect to EOS S3 pads through 22 ohm resistors, but the exact pads are not legible in the OCR. Look at the schematic image before using these pads.
- I2C: 100 kHz and 400 kHz, SPI up to 10 MHz (guide). To use an external PDM mic remove R28 (100 ohm).

## Related files

- `EOS_S3_IO_Package_Map.md`
- `../SparkFun_QuickLogic_ThingPlus_EOS-S3_R8_Schematic.md` (OCR text of the schematic)
- `QuickFeather.md`
- `../EOS_S3_FPGA_Design_Flow.md`
