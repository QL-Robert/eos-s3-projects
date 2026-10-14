---
title: "QuickLogic QuickFeather (EOS S3) - board reference"
type: board-reference
topic: QuickFeather hardware, pins, boot, flash map, programming
added: 2026-10-11
sources: QORC SDK (BSP/quickfeather, qf_apps, docs); QuickFeather pin-planner log (user guide Rev 1.2.1 + IO map CSV); datasheet v3.3d Table 31; github.com/QuickLogic-Corp/quick-feather-dev-board README
---

# QuickLogic QuickFeather development kit (EOS S3)

An open-hardware, Adafruit-Feather-compatible board built around the QuickLogic **EOS S3** (Cortex-M4F + eFPGA). Design files were created by Antmicro with QuickLogic (repo `quick-feather-dev-board`, CC-BY-SA-4.0; user guide `doc/QuickFeather_UserGuide.pdf`, schematic `quickfeather-board.sch`). It is the main board of the QORC SDK and of this knowledge base.

**Package:** 64-pin QFN, `-P PU64` for `ql_symbiflow`. The datasheet says the QFN is provided for the QuickFeather only (not a mass-production package). See `EOS_S3_IO_Package_Map.md` for every IO.

## What is on the board

Sources: the board repo README and the datasheet; part numbers come from the README feature list.

| Item | Detail |
|---|---|
| MCU / FPGA | QuickLogic EOS S3 (Cortex-M4F + eFPGA). Fabric: 891 logic cells, 8 x 8 Kbit RAM, 8 FIFO controllers, 2 multipliers (see the datasheet) |
| Flash | 16 Mbit (2 MB) SPI NOR, GigaDevice GD25Q16C. Shares IO_34/36/38 with the SPI-master header pins |
| Accelerometer | mCube MC3635 on I2C0; interrupt on IO_3 |
| Pressure sensor | Infineon DPS310 on I2C0 |
| Microphone | Infineon IM69D130 MEMS PDM mic: data IO_28, clock IO_29 |
| UI | One user button (IO_6), one RGB LED (blue IO_18, green IO_21, red IO_22) |
| Power | Micro-USB or a single Li-Po cell; onboard charger |
| USB | Micro-USB. USB data lines go to the eFPGA, so the USB-serial port exists only while the stock USB-to-serial gateware is loaded |
| Debug | SWD (J-Link) header J6: SWD CLK IO_14, SWD IO IO_15 |
| Expansion | Feather-style 0.1" headers, breadboard compatible |
| Simulation | Supported in Renode (Antmicro) |

## Pins used by the board (do not re-use blindly)

From the pin-planner log (user guide Rev 1.2.1, with the user-supplied IO map CSV taking priority where they differ):

| Function | IO | Connector |
|---|---|---|
| UART TX / RX | IO_44 / IO_45 | J3.2 / J3.3 (J3.1 = GND) |
| SWD CLK / IO | IO_14 / IO_15 | J6 |
| I2C0 SCL / SDA | IO_0 / IO_1 | J2 (shared with accelerometer and pressure sensor) |
| SPI master CLK / MISO / MOSI | IO_34 / IO_36 / IO_38 | J3 (shares the bus with the boot flash), plus CS2 = IO_27 on J2 |
| I2S WCLK / DATA / CLK | IO_23 / IO_24 / IO_31 | J8 |
| PDM mic data / clock | IO_28 / IO_29 | J8 |
| LEDs blue / green / red | IO_18 / IO_21 / IO_22 | onboard |
| User button | IO_6 | onboard |
| Accelerometer interrupt | IO_3 | onboard |
| Interrupt to host | IO_43 | |

- Pins 0-45 are wired somewhere except **9, 26, 35, 37, 39, 41, 42**, which the IO map lists as not present on the board.
- With Master boot (boot from the flash), IO_34/35/36/38/39 are reserved, so only one of the usual SPI pads is free. See the open items at the end of the pin-planner log.
- The earlier reading "IO_32/IO_33 = I2C1" was removed: the IO map CSV lists them as plain IO.
- Fabric LED PCF (from the SDK): `set_io redled IO_22`, `greenled IO_21`, `blueled IO_18`. Package spellings: red QFN 34 / BGA G7, green 39 / H7, blue 38 / E8.

## Boot and programming workflow (QORC SDK)

Details: `QORC_SDK_Getting_Started_QuickFeather.md`.

1. Build an app (`make` in `qf_apps/<app>/GCC_Project`, Linux or WSL with `source envsetup.sh`).
2. Reset the board. The **blue LED flashes for about 5 s**. Press the user button during that time: the bootloader starts and the **green LED breathes**. If it does not, reset again and press the button within 5 s of releasing reset.
3. Program: `qfprog --port /dev/ttyXX --m4app output/bin/<app>.bin` (also `--appfpga x.bin`, `--mode fpga|fpga-m4`).
4. Reset again **without** pressing the button. The blue LED flashes for 5 s, then the bootloader loads the M4 app (and the app FPGA image) from flash and runs it.
5. In the stock setup the board enumerates as a USB serial port; use PuTTY or similar for the console. After loading a custom FPGA image (for example `qf_helloworldhw`) the USB serial port **disappears** because the fabric no longer runs the USB-serial gateware. Use the hardware UART on J3 (IO_44/IO_45) with a USB-UART adapter, or J-Link.

Prebuilt initial binaries would live in `qf_apps/quickfeather-initial-binaries` (the folder is empty in the local SDK copy). The equivalent recovery procedure for the Thing Plus (J-Link loads `qf_loadflash`, then the factory binaries are programmed) is in `QuickThing_Plus.md`; confirm the QuickFeather procedure in the SDK docs before relying on it.

## Flash map (2 MB flash, from `BSP/quickfeather/inc/flash_defines.h`)

| Address | Size | Content |
|---|---|---|
| 0x000000 | 64 KB | Bootloader (raw flash) |
| 0x010000 | 4 KB | Metadata {CRC, byte count}: USB-to-serial FPGA image |
| 0x011000 | 4 KB | Metadata: application FPGA image |
| 0x012000 | 4 KB | Metadata: application FFE image |
| 0x013000 | 4 KB | Metadata: application M4 image |
| 0x014000 | 44 KB | Reserved |
| 0x01F000 | 4 KB | Bootloader metadata |
| 0x020000 | 128 KB | USB-to-serial FPGA image |
| 0x040000 | 128 KB | **Application FPGA image** (`appfpga`) |
| 0x060000 | 128 KB | Application FFE image |
| 0x080000 | 440 KB | Application M4 image (last 64 KB + 8 KB used by the bootloader for copying) |
| 0x0EE000 | 72 KB | Reserved |
| 0x100000 | 1 MB | Unused |

## M4 memory regions (linker script `quickfeather.ld`; `thingplus.ld` in the QuickThing apps is identical)

| Region | Origin | Length |
|---|---|---|
| rom (code) | 0x00000000 | 0x27000 |
| ram | 0x20027000 | 0x3C800 |
| spiram | 0x20063800 | 0x800 |
| HWA | 0x20064000 | 0x18000 |
| shm | 0x2007C000 | 0x4000 |

## Firmware BSP notes

- BSP in `BSP/quickfeather`: `qf_hardwaresetup.c`, `leds.c/.h` (`LedBlueOn()`, `LedGreenOn()`, `LedOrangeOn()` etc.; they set `IO_MUX->PAD_xx_CTRL = 0x103` and bits in `MISC_CTRL->IO_OUTPUT`), `battery_level_monitor.c`, `flash_defines.h`.
- The same BSP and linker script are used for the SparkFun QuickThing Plus (see `QuickThing_Plus.md`).
- `qf_baremetalsetup.c` sets up power domains and clocks without the `S3X_CLK_XXX` management or power-management scheme (`qf_baremetal` app; not in the local SDK copy).
- Example apps: `qf_helloworldsw` (M4 only, CLI with `diag red` etc.), `qf_helloworldhw` (M4 + FPGA LED design), `qf_advancedfpga`, `qf_fpgauart_app`, `qf_uart2usbser`, `qf_ssi_ai_app`, `qf_mqttsn_ai_app`, bootloaders (`qf_bootloader`, `qf_bootloader_uart`, `qf_rs_bootloader`), `qf_loadflash`, `qf_gwtestharness`.

## Using the eFPGA on QuickFeather

- Toolchain: `ql_symbiflow ... -d ql-eos-s3 -P PU64 ... -p quickfeather.pcf`. See `EOS_S3_FPGA_Design_Flow.md`.
- Wishbone window to the fabric: `0x4002_0000`-`0x4003_FFFF` (see `wishbone/`).
- Reference LED design: `qf_apps/qf_helloworldhw/fpga/rtl` (`helloworldfpga.v`, `quickfeather.pcf` using QFN pins 34/39/38).
- Designs with PCFs for QuickFeather: `source_code_knowledge/designs/` (qorc-onion-apps, S3_FPGA_2xUART_GPIO) and `s3-gateware/projects/*/rtl/quickfeather.pcf`.
- Example GPIO choices in the SDK PCFs: UART0 on IO_2/IO_3, UART1 on IO_4/IO_5 (`S3_FPGA_2xUART`). Note that IO_3 is the accelerometer interrupt on QuickFeather, so check these assignments for conflicts before reusing them.

## Related files

- `EOS_S3_IO_Package_Map.md` - every IO with QFN pin, BGA ball and board usage
- `EOS_S3_Pin_Planner_Discussion_Log.md` - how the QuickFeather pin facts were derived and checked
- `QuickThing_Plus.md` - the sibling SparkFun board
- `QORC_SDK_Getting_Started_QuickFeather.md` - step-by-step lessons
