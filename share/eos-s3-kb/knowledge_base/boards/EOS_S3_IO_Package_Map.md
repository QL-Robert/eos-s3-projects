---
title: "EOS S3 IO to package pin map (WLCSP / BGA PD64 / QFN PU64) with QuickFeather and QuickThing Plus usage"
type: board-reference
topic: pin mapping, PCF constraints, board IO usage
added: 2026-10-11
sources: EOS S3 datasheet v3.3d Table 31 (pinout); QuickFeather pin-planner log (user guide Rev 1.2.1 + IO map CSV); SparkFun QuickLogic Thing Plus hookup guide; QTPLUS_R8 schematic
---

# EOS S3 IO to package pin map

Which package pin each EOS S3 IO uses, and what the **QuickFeather** (QFN, `-P PU64`) and **SparkFun QuickThing Plus** (BGA, `-P PD64`) do with it.

How to use it in a PCF (see `EOS_S3_FPGA_Design_Flow.md`): `set_io red_led IO_22` works for every package that bonds out that IO. The same pad can also be written as the QFN pin number (`34`) or the BGA ball (`G7`). Use the column that matches the `-P` package you build for.

- Package columns come from the datasheet pinout table (Table 31). A `--` means the pad is not bonded out in that package. The datasheet notes that the QFN pinout is given for the QuickFeather board only (not a mass-production package).
- Board columns: QuickFeather data is from the pin-planner log (user guide Rev 1.2.1 + the IO map CSV); QuickThing Plus data is from the SparkFun hookup guide and the R8 schematic. "GPIO" means a general-purpose pin on a header with no fixed function. A blank cell means no source in this knowledge base states a function.
- The SparkFun guide and the schematic text disagree on a few header labels (see `QuickThing_Plus.md`, section "Source conflicts"). Verify against the physical board before wiring.

| IO | VCCIO bank | WLCSP ball | BGA ball (PD64) | QFN pin (PU64) | QuickFeather | QuickThing Plus |
|---|---|---|---|---|---|---|
| IO_0 | VCCIOA | A7 | B1 | 4 | I2C0 SCL (J2) - shared with onboard accelerometer + pressure sensor | I2C0 SCL (J9.11, Qwiic, accelerometer, mic config) |
| IO_1 | VCCIOA | B7 | C1 | 5 | I2C0 SDA (J2) - shared with onboard sensors | I2C0 SDA (J9.12, Qwiic, accelerometer, mic config) |
| IO_2 | VCCIOA | -- | A1 | 6 |  | GPIO (J6.7) |
| IO_3 | VCCIOA | C7 | A2 | 2 | Accelerometer interrupt | Accelerometer INT (IMU_INT, J9.10) |
| IO_4 | VCCIOA | -- | B2 | 3 |  | GPIO (J8.8) |
| IO_5 | VCCIOA | -- | C3 | 64 |  | GPIO (J8.9) |
| IO_6 | VCCIOA | A6 | B3 | 62 | User button | User button (J8.10) |
| IO_7 | VCCIOA | -- | A3 | 63 |  | GPIO (J8.11) |
| IO_8 | VCCIOA | B6 | C4 | 61 |  | GPIO (J8.12) |
| IO_9 | VCCIOA | A5 | B4 | 60 | Not on board IO map |  |
| IO_10 | VCCIOA | B5 | A4 | 59 |  | GPIO (J8.13) |
| IO_11 | VCCIOA | -- | C5 | 57 |  | GPIO (J8.6) |
| IO_12 | VCCIOA | -- | B5 | 56 |  | GPIO (J8.7); also mic INT net S3IO_12 (schematic) |
| IO_13 | VCCIOA | -- | D6 | 55 |  | GPIO (J6.8) |
| IO_14 | VCCIOA | A4 | A5 | 54 | SWD CLK (J6) - never in a PCF | SWD CLK (J7.4) |
| IO_15 | VCCIOA | B4 | C6 | 53 | SWD IO (J6) - never in a PCF | SWD IO (J7.2) |
| IO_16 | VCCIOB | E1 | E7 | 40 |  | SPI peripheral CLK (J9.8) |
| IO_17 | VCCIOB | D1 | D7 | 42 |  | SPI peripheral CIPO (J9.7) |
| IO_18 | VCCIOB | -- | E8 | 38 | Blue LED | Blue LED (not on headers) |
| IO_19 | VCCIOB | C1 | H8 | 36 |  | SPI peripheral COPI (J9.6); boot-strap |
| IO_20 | VCCIOB | F2 | G8 | 37 |  | SPI peripheral CSn (J9.5); boot-strap |
| IO_21 | VCCIOB | -- | H7 | 39 | Green LED | Green LED (not on headers) |
| IO_22 | VCCIOB | -- | G7 | 34 | Red LED | Red LED (not on headers) |
| IO_23 | VCCIOB | E2 | H6 | 33 | I2S WCLK (J8) | I2S WCLK (J8.3) |
| IO_24 | VCCIOB | D2 | G6 | 32 | I2S data (J8) | I2S data out (J8.4) |
| IO_25 | VCCIOB | D3 | F7 | 31 |  | GPIO (J6.9) |
| IO_26 | VCCIOB | -- | F6 | 30 | Not on board IO map | ADC0_EN - battery-voltage monitor enable (schematic) |
| IO_27 | VCCIOB | -- | H5 | 28 | SPI master CS2 (J2) | SPI master CS2 (J9.4) |
| IO_28 | VCCIOB | F3 | G5 | 27 | PDM mic data (J8, onboard mic) | PDM mic data (J8.1, onboard VM3011) |
| IO_29 | VCCIOB | E3 | F5 | 26 | PDM mic clock (J8, onboard mic) | PDM mic clock (J8.2, onboard VM3011) |
| IO_30 | VCCIOB | F4 | F4 | 25 |  | GPIO (J6.10) |
| IO_31 | VCCIOB | E4 | G4 | 23 | I2S CLK (J8) | I2S CLK (J8.5) |
| IO_32 | VCCIOB | -- | H4 | 22 |  |  |
| IO_33 | VCCIOB | -- | E3 | 21 |  |  |
| IO_34 | VCCIOB | D5 | F3 | 20 | SPI master CLK (J3) - shared with boot flash | SPI master CLK (J6.6) + onboard flash |
| IO_35 | VCCIOB | -- | F2 | 18 | Not on board IO map; reserved by Master boot | GPIO (J8.14) |
| IO_36 | VCCIOB | F5 | H3 | 17 | SPI master MISO (J3) - shared with boot flash | SPI master CIPO (J6.4) + onboard flash |
| IO_37 | VCCIOB | -- | G2 | 15 | Not on board IO map |  |
| IO_38 | VCCIOB | E6 | E2 | 16 | SPI master MOSI (J3) - shared with boot flash | SPI master COPI (J6.5) + onboard flash |
| IO_39 | VCCIOB | F6 | H2 | 11 | Not on board IO map; reserved by Master boot | Onboard flash chip select (SPI_MST_SS, schematic) |
| IO_40 | VCCIOB | -- | D2 | 13 |  |  |
| IO_41 | VCCIOB | -- | F1 | 14 | Not on board IO map |  |
| IO_42 | VCCIOB | -- | H1 | 10 | Not on board IO map |  |
| IO_43 | VCCIOB | D7 | D1 | 7 | Interrupt to host | Interrupt output to host (J9.9) |
| IO_44 | VCCIOB | E7 | E1 | 8 | UART TX (J3.2) | UART TX (J6.2) |
| IO_45 | VCCIOB | F7 | G1 | 9 | UART RX (J3.3) | UART RX (J6.3) |

## Quick equivalences (same pad, three spellings)

| Signal | Alias (all packages) | QFN PU64 | BGA PD64 |
|---|---|---|---|
| Red LED | `IO_22` | `34` | `G7` |
| Green LED | `IO_21` | `39` | `H7` |
| Blue LED | `IO_18` | `38` | `E8` |
| User button | `IO_6` | `62` | `B3` |
| UART TX | `IO_44` | `8` | `E1` |
| UART RX | `IO_45` | `9` | `G1` |

The LED rows are confirmed by the SDK's `quickfeather.pcf` comments (red = IO_22 = QFN 34 = BGA G7). The other rows are read from the table above.

## Caution

- IO_14 / IO_15 are SWD on both boards. Do not put them in a PCF.
- QuickFeather: the boot flash shares IO_34/36/38 (and IO_35/39 are reserved by Master boot). Using them from the fabric can break booting from flash.
- QuickThing Plus: IO_19 and IO_20 are boot-strap pins (shunts J2/J3). IO_26 enables the battery-voltage divider.
- Loading a custom FPGA image replaces the USB-serial gateware on both boards.
