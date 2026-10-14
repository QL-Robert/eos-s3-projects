---
title: "QuickLogic EOS S3 — eFPGA Design Flow"
type: "reference"
topic: "FPGA design flow"
added: 2026-10-09
sources: "Local: EOS S3 TRM r1.01a, qorc-sdk (envsetup.sh, quickstart.rst, makefiles, Libraries/FPGA), qorc-onion-apps, knowledge-base notes. Web: QuickLogic FPGA toolchain docs, quicklogic-fpga-toolchain releases, F4PGA examples/arch-defs, Yosys docs. Full list at the end."
---

# QuickLogic EOS S3 — eFPGA Design Flow

How to go from Verilog to a running design in the EOS S3's embedded FPGA (eFPGA): fabric resources, toolchains, design entry, constraints, synthesis/place/route, simulation, output formats, loading onto the board, and the gotchas collected so far.

> **One-line summary:** write Verilog with a `qlal4s3b_cell_macro` instance → constrain pins in a `.pcf` (optionally timing in a `.sdc`) → `ql_symbiflow -compile … -dump …` (Yosys + VPR) → load the result from the M4 (`load_fpga()` with a C header), from SPI flash via the bootloader (`.bin` + `qfprog`), or over SWD (`.jlink` / `.openocd`).

---

## 1. The fabric (what you are designing for)

From the EOS S3 TRM r1.01a, chapter 27, and the toolchain docs.

| Resource | Amount | Notes |
|---|---|---|
| Logic cells | 891 (TRM table 27-1); marketed as "2,400 effective logic cells" | Multiplexer-based cell, up to 22 inputs, 4 outputs (3 combinational + 1 registered). Implements two 3-input functions, any 4-input function, 8:1 mux, etc. One flip-flop with clock enable, set, reset |
| Block RAM | 8 × 8 Kbit (9,216 bits each incl. parity), 64 Kbit total | Dual-port, independent read/write widths (×8/×16/×32 per toolchain docs), independent clocks, write byte enables, pipelined or not. Two blocks concatenate horizontally (512×36) or vertically (1024×18) without extra logic |
| FIFO controllers | 8 | Built on the RAM blocks; sync or async; independent push/pop widths; async pointer reset, synchronous flush |
| Multipliers | 2 × 32×32 (or 4 × 16×16), signed | `qlal4s3_mult_cell_macro` |
| Configurable interface | 32 | FBIO pads with optional registered IN/OUT/EN and FIX_HOLD |
| Configuration memory | SRAM, loaded at runtime | Volatile: the M4 (or bootloader) must load it after every power-up |

Interfaces from fabric to the rest of the SoC (TRM 27.2.3–27.2.4): AHB-to-Wishbone bridge (M4 → fabric registers at 0x4002_0000, 128 KB), SDMA (4 channels), 4 interrupts to the M4 (`FB_msg_out[3:0]`), packet FIFO, SPI-master APB port. Fabric clocks come from the CRU: **C16 = `Sys_Clk0`, C21 = `Sys_Clk1`** (max 72 MHz), C02 = `Sys_Pclk`; the fabric drives `WB_CLK` (C40, **max 10 MHz**) back to the bridge. Details: [Wishbone reference notes](<wishbone/EOS_S3_Wishbone_Reference_Notes.md>).

---

## 2. Toolchain options

| Flow | Status | Constraint files | Command | Notes |
|---|---|---|---|---|
| **QuickLogic Symbiflow** (`ql_symbiflow`) | **Default in qorc-sdk.** Open source. v1.3.1 used by `envsetup.sh`; v1.3.2 (30 Mar, "bug fixes and enhancements") is the latest release | `.pcf`, `.sdc` | `ql_symbiflow -compile …` | Bundles Yosys + plugins, VPR (VTR), iverilog, arch defs, conda. Linux x86-64 only |
| **F4PGA** (successor of SymbiFlow) | Open source, newer packaging | `.pcf`, `.sdc` (via `flow.json`) | `f4pga -vvv build --flow ./flow.json` | `FPGA_FAM=eos-s3`, packages `install-ql ql-eos-s3_wlcsp`. f4pga-examples `eos-s3/btn_counter` keeps the old `ql_symbiflow` command behind `F4PGA_USE_DEPRECATED` |
| **Aurora** (QuickLogic, commercial) | Licensed (`quicklogic_LICENSE`) | `.qdc` (one file: synthesis, placement, routing, timing, power, IO config) | `aurora --console --compile_design <v> --top <top> -o <file>.qdc -d QLAL4S3B -k PU64 --run_all` | Used by `qorc-sdk/qorc_apps_au/*_au`. Output `rtl/config_bit_gen/QLAL4S3B_<top>.bin` |
| **MatrixIDE** (Rapid Silicon) | Licensed (`rapidsilic_LICENSE`) | `.qdc` | via `fpga/Makefile` in `*_mx` apps | Used by `qorc-sdk/qorc_apps_au/*_mx` |
| **SpDE / QuickWorks** (legacy) | Legacy QuickLogic tools | SpDE project (`.chp`), constraint manager | GUI | `.chp` files and `sim/`/`timingSim/` folders in `s3-gateware` and qorc-onion-apps come from SpDE. No public `.scp` timing-file examples exist |

The rest of this document describes the **ql_symbiflow** flow unless noted.

### Toolchain release history (quicklogic-fpga-toolchain)

| Version | Date* | Changes |
|---|---|---|
| v0.1.0 | 02 Jun 2020 | Pre-release for EOS S3 |
| v1.0.0 | 16 Jun 2020 | First production release |
| v1.1.0 | 02 Jul 2020 | Better clock-network use; **post-layout timing simulation with SDF**; ~2× faster, ~8% better critical path |
| v1.2.0 | 10 Sep 2020 | **BRAM inference** in Yosys; BRAM init from hex file; ~11% area improvement |
| v1.3.0 | 19 Nov 2020 | **OpenOCD** download/debug of MCU + FPGA; VTR router lookahead |
| v1.3.1 | 14 Dec 2020 | **IOMUX array in header**; **binary (`.bin`) output with header**; BRAM inference threshold lowered 4096 → 128 bits |
| v1.3.2 | 30 Mar 2021 | Bug fixes and enhancements (latest) |

\*Release pages show day/month only; years inferred from the qorc-sdk timeline (bootloader v2.1 in qorc-sdk v1.5.0, 10 Dec 2020, requires toolchain v1.3.1).

---

## 3. Installation and environment

### Automated (recommended)

```bash
git clone https://github.com/QuickLogic-Corp/qorc-sdk
cd qorc-sdk
source envsetup.sh        # must be sourced, not executed
```

`envsetup.sh` (v1.5.1) installs into the SDK folder, then initialises on every run:

| Component | Version | Install dir |
|---|---|---|
| ARM GCC | gcc-arm-none-eabi 9-2020-q2 | `arm_toolchain_install/` |
| FPGA toolchain | `Symbiflow_v1.3.1.gz.run` | `fpga_toolchain_install/v1.3.1/` |
| Flash programmer | TinyFPGA-Programmer-Application (`qfprog` shell function) + `pip3 install tinyfpgab apio` | `TinyFPGA-Programmer-Application/` |
| OpenOCD | xpack 0.11.0-3 | `openocd_install/` |
| J-Link | V7.60d | `jlink_install/` |

Run `source envsetup.sh` again in every new terminal.

### Manual FPGA toolchain install

```bash
export INSTALL_DIR=${PWD}/fpga_toolchain_install/v1.3.1
wget https://github.com/QuickLogic-Corp/quicklogic-fpga-toolchain/releases/download/v1.3.1/Symbiflow_v1.3.1.gz.run
bash Symbiflow_v1.3.1.gz.run

# every new shell:
export PATH="$INSTALL_DIR/quicklogic-arch-defs/bin:$INSTALL_DIR/quicklogic-arch-defs/bin/python:$PATH"
source "$INSTALL_DIR/conda/etc/profile.d/conda.sh"
conda activate
ql_symbiflow -h
```

Requirements (toolchain docs): 64-bit Linux (Ubuntu/CentOS), ≥2 GB RAM, ≥5 GB disk. On Windows use WSL.

### F4PGA install (alternative)

```bash
export F4PGA_INSTALL_DIR=~/opt/f4pga
export FPGA_FAM=eos-s3
export F4PGA_PACKAGES='install-ql ql-eos-s3_wlcsp'
# then the conda + package-download steps from f4pga-examples "Getting"
cd eos-s3 && source "$F4PGA_INSTALL_DIR/$FPGA_FAM/conda/etc/profile.d/conda.sh" && conda activate $FPGA_FAM
make -C btn_counter
```

`flow.json` for the example: part `EOS3FF512-PDN64` (`ql-eos-s3`, package `PD64`), default target `bitstream`, inputs `pcf`, `sdc-in`, sources.

---

## 4. Design entry

### Language and structure

- **Verilog only** (`-v` takes Verilog files; VHDL is not supported by ql_symbiflow).
- A design that talks to the M4 instantiates **`qlal4s3b_cell_macro`** (the hard interface: Wishbone bridge, clocks/resets, SDMA, interrupts, packet FIFO, SPI-master APB, Device_ID). Standalone designs can use it only for clocks (`.Sys_Clk0(clk)`).
- Route clocks and resets through **`gclkbuff`** (global clock buffer), e.g. `gclkbuff u_clk(.A(Sys_Clk0), .Z(WB_CLK));`.
- Leave `FBIO_*` / `SFBIO` ports on the cell macro unconnected; pads are assigned through the PCF instead.
- IO buffers (`inpad`, `outpad`, `bipad`, `ckpad`) are inserted by synthesis from top-level ports; you normally don't instantiate them.

Typical QuickLogic project layout (s3-gateware, qorc-sdk apps, qorc-onion-apps):

```
fpga/rtl/AL4S3B_FPGA_Top.v          top: cell macro, gclkbuff, pads, interrupts
fpga/rtl/AL4S3B_FPGA_IP.v           Wishbone decode (4 KB blocks on WBs_ADR[16:12]), ACK OR, read mux
fpga/rtl/AL4S3B_FPGA_Registers.v    ID/revision/control registers
fpga/rtl/AL4S3B_FPGA_QL_Reserved.v  reserved block + default-ACK timer
fpga/rtl/<ip>.v                     your blocks
fpga/rtl/quickfeather.pcf           pin constraints
```

Reference designs: [S3_FPGA_2xUART_GPIO](<designs/S3_FPGA_2xUART_GPIO.md>), [qorc-onion-apps](<designs/qorc-onion-apps.md>), `source_code_knowledge/s3-gateware/` (UART 16550, GPIO, FLL_I2S, ADC AD7476, USB-serial).

### Hard macros

| Macro | Use | Notes |
|---|---|---|
| `RAM_8K_BLK` | One 8 Kbit RAM | Params `addr_int`, `data_depth_int`, `data_width_int`, `wr_enable_int`, `reg_rd_int`, `INIT`, `INIT_FILE` (hex) |
| `RAM_16K_BLK` | Two blocks concatenated (512×32 horizontal, 2048×8 vertical) or 16 Kbit | Same params |
| `FIFO_8K_BLK`, `FIFO_16K_BLK` | FIFO on 1 or 2 RAM blocks | Used by s3-gateware (e.g. ADC RX FIFO) |
| `ram8k_2x1_cell_macro` | Low-level RAM primitive (what the wrappers map to) | Appears in s3-gateware RTL |
| `qlal4s3_mult_cell_macro` | Multiplier; `sel_mul_32x32` = 1 → one 32×32, 0 → two 16×16 | Wrappers `MULT_32BIT`, `MULT_16BIT_X2` (toolchain docs) / `qlal4s3_mult_32x32_cell`, `qlal4s3_mult_16x16_cell` (SDK RTL) |
| `gclkbuff` | Global clock/reset buffer | |

Definitions: `<INSTALL_DIR>/conda/share/yosys/quicklogic/` (`pp3_cells_sim.v`, `cells_sim.v`). RAM can also be **inferred** from generic Verilog since v1.2.0 (threshold 128 bits since v1.3.1). **Limitation:** only symmetrical RAM width combinations are supported. Examples: `quicklogic-arch-defs/tests/RAM_Examples`, `tests/ram_test`.

### Yosys synthesis details (for reference)

`synth_quicklogic -family pp3` (PolarPro 3 = EOS S3 fabric): `muxcover -mux8 -mux4`, `abc9 -maxlut 4 -dff`, LUT mapping, `clkbufmap -inpad ckpad Q:P`, `iopadmap … -outpad outpad -inpad inpad -tinoutpad bipad`, `setundef -zero`. Options include `-nobram`, `-nocarry`, `-blif`, `-verilog`.

---

## 5. Constraints

### Pin constraints (`.pcf`, passed with `-p`)

```
set_io <port_name> <pad>
set_io red_led   IO_22          # pad alias (works for every package that has the pad)
set_io red_led   34             # PU64 (QFN) pin number
set_io red_led   G7             # PD64 (BGA) ball
set_io count(0)  A2             # bus bits use name(index)
```

| Package | `-P` value | Board |
|---|---|---|
| QFN 64 | `PU64` | **QuickFeather** (see `boards/QuickFeather.md`) |
| BGA 64 | `PD64` | **SparkFun QuickThing Plus** (`boards/QuickThing_Plus.md`), Chandalar (toolchain examples) |
| WLCSP 42 | `WR42` | Fewer pads (no IO_22, for example) |

- Prefer **`IO_x` aliases** so the PCF works across packages — but only use pads the chosen package actually bonds out.
- Clock-capable pads can also be used as bidirectional IO (toolchain docs).
- Every top-level port should have a `set_io`; remove lines for ports that don't exist.
- QuickFeather notes: IO_14/IO_15 are SWD (leave them out of the PCF); LEDs blue IO_18, green IO_21, red IO_22; UART IO_44/IO_45; boot SPI flash on IO_34/35/36/38/39 (see the pin-planner log).
- Pin mux register settings for the used pads are emitted by the toolchain (IOMUX array in the header / iomux section of the `.bin`, since v1.3.1).

### Timing constraints (`.sdc`, passed with `-s`)

Standard SDC, VPR-supported subset (`create_clock`, `set_input_delay`, `set_output_delay`, `set_clock_groups`, `set_false_path`, `set_clock_uncertainty`, …; see the VPR SDC reference). Example from f4pga-arch-defs:

```tcl
create_clock -period 100.0 clk
```

`process_sdc_constraints.py` rewrites pin names to net names using the PCF before VPR sees the file. **Without `-s`, an empty `top_dummy.sdc` is used and VPR optimises every clock for maximum Fmax.** Cell/routing delays come from the arch timing data (`*.lib` per corner, `qlal4s3b_RoutingDelays_*.csv`), not from the SDC. More: [VPR timing notes](<EOS_S3_VPR_Timing_Constraint_and_Report_Notes.md>).

### Aurora `.qdc` (Aurora/MatrixIDE flows only)

One Tcl-style file with sections `#synthesis`, `#verifier`, `#logicoptimizer`, `#placer` (`fixplace_io -iotocell {{led_b_o IO_18} …}`), `#router`, `#timingengine` (`default_clock_period -value 10`, `select_process_corner … {Typical}`), `#powerestimation`, `#programmer` (`config_io -io {{IO_22 func_sel:0 ctrl_sel:fabric mode:inout pull:none drive:2 slew:slow schmitt:0} …}`). Example: `qorc-sdk/qorc_apps_au/qorc_helloworldfpga_au/fpga/rtl/helloworldfpga.qdc`.

---

## 6. Running the flow (`ql_symbiflow`)

### Options

| Option | Meaning |
|---|---|
| `-synth` | Synthesis only (Yosys) |
| `-compile` | Pack, place, route, generate FASM/bitstream (runs synthesis first if needed) |
| `-src <dir>` | Source folder (use the full path, e.g. `$PWD`) |
| `-d ql-eos-s3` | Device (only value for EOS S3) |
| `-P <pkg>` | Package: `PD64`, `PU64`, `WR42` (case-insensitive in practice; SDK makefiles use `pu64` and `PU64`) |
| `-p <file.pcf>` | Pin constraints |
| `-s <file.sdc>` | Timing constraints |
| `-r timing\|congestion` | Router mode |
| `-t <top>` | Top module name |
| `-v <files>` | Verilog sources (space-separated) |
| `-dump <fmts>` | Extra outputs, any of `header`, `binary`, `jlink`, `openocd`, `post_verilog` |
| `-h` | Help |

Some qorc-sdk makefiles pass `-k PU64` instead of `-P PU64`; `-k` is not in the toolchain's documented option list — use `-P`.

### Typical commands

```bash
# synthesis only
ql_symbiflow -synth -src $PWD -d ql-eos-s3 -t top -v counter_16bit.v -p chandalar.pcf -P PD64

# full flow, all outputs
ql_symbiflow -compile -src $PWD -d ql-eos-s3 -P PU64 -t top \
    -v AL4S3B_FPGA_Top.v AL4S3B_FPGA_IP.v ... -p quickfeather.pcf -s top.sdc \
    -dump header binary jlink openocd post_verilog
```

### Stages and files

All intermediate files go to `build/` under the source folder.

| Stage | Tool | Output |
|---|---|---|
| Synthesis | Yosys + QuickLogic plugins | `<top>.eblif` (netlist for VPR), `<top>_synth.log` |
| Pack | VPR | `<top>.net`, `pack.log` |
| Place | VPR | `<top>.place`, `<top>_io.place`, `placer.log` |
| Route | VPR | `<top>.route`, `router.log` |
| Timing analysis | VPR | `report_timing.setup.rpt`, `report_timing.hold.rpt`, `report_unconstrained_timing.*.rpt`, `pre_pack.report_timing.setup.rpt`, `top.log` / `vpr_stdout.log` (WNS/TNS, final critical path, Fmax) |
| FASM | genfasm | `<top>.fasm` |
| Bitstream | `qlfasm` | `<top>.bit` |
| `-dump post_verilog` | fasm2bels / VPR netlist writer | `top_bit.v` (Verilog rebuilt from the bitstream, for functional sim) + `top_post_synthesis.v` + `top_post_synthesis.sdf` (timing sim) |
| `-dump header` | | `<top>_bit.h` |
| `-dump binary` | | `<top>.bin` |
| `-dump jlink` / `openocd` | | `<top>.jlink`, `<top>.openocd` |

Example result from the toolchain docs (counter_16bit, PD64): hWNS 0 ns, sWNS −35.23 ns, final critical path 35.23 ns, **Fmax 28.4 MHz** — read `top.log` after every build.

VPR rewrites the timing report after placement and again after routing; the final copy is post-route. Control with `--timing_report_npaths` (default 100) and `--timing_report_detail`.

The f4pga-arch-defs equivalent stages (CMake targets `<design>-<board>_<stage>`): eblif → pack → place → route → analysis → fasm → bit → jlink → openocd → bit_v (the last three are pp3-only). Boards: `ql-chandalar`, `ql-quickfeather`.

---

## 7. Simulation

| Level | Files | Simulator |
|---|---|---|
| **Pre-layout (RTL)** | your RTL + testbench | `iverilog -o sim rtl.v tb.v && vvp sim`; `gtkwave dump.vcd` (`$dumpfile` in the testbench) |
| **Post-layout functional** (checks the configuration bits) | `top_bit.v` + `<INSTALL_DIR>/conda/share/yosys/quicklogic/cells_sim.v` | iverilog |
| **Post-layout timing** (SDF) | `build/top_post_synthesis.v` + `build/top_post_synthesis.sdf` + `quicklogic-arch-defs/share/techmaps/quicklogic/techmap/cells_sim.v` + `share/arch/ql-eos-s3_wlcsp/cells/ram_sim.v` | iverilog (toolchain docs) |
| **System (M4 ↔ fabric)** | `pp3_cells_sim.v` from s3-gateware: `qlal4s3b_cell_macro_bfm`, AHB-to-Wishbone bridge model, `ahb_write_word_al4s3b_fabric` / `ahb_read_word_al4s3b_fabric` tasks | iverilog / commercial |

Notes:
- Icarus Verilog supports only part of SDF (IOPATH/INTERCONNECT); PORT-delay-heavy SDFs simulate optimistically. Experience on QuickLogic's Eclipse2 (a different device) found OSS CVC handled full SDF and timing checks, and that `P_FF` models had no notifier, so timing violations only print warnings (Eclipse2 post-layout timing-simulation note, 2026).
- s3-gateware IP folders contain RTL and timing-sim testbenches (`rtlsim/`, `timingSim/`, `sim/`) from the SpDE era.

---

## 8. Getting the design onto the chip

The fabric is SRAM-configured, so something has to load it at every boot. Four ways:

### 8.1 C header, loaded by the M4 (`-dump header`)

Used by every `qf_apps` project. `<top>_bit.h` holds the bitstream array (`axFPGABitStream`) plus the IOMUX settings (v1.3.1+). The M4 code does:

```c
load_fpga(sizeof(axFPGABitStream), axFPGABitStream);   // Libraries/FPGA/src/fpga_loader.c
S3x_Clk_Enable(S3X_FB_21_CLK);                         // start fabric clocks
S3x_Clk_Enable(S3X_FB_16_CLK);
```

What `load_fpga()` does (from the SDK source): enables C02, C08 (A0), C16 and the FB/PIF clock gates → writes `CFG_CTL` (0x4001_4000) = `0xBDFF` to enter configuration mode → writes every 32-bit word to `CFG_DATA` (0x4001_4FFC) → `CFG_CTL` = 0 to exit → clears fabric resets (`FB_SW_RESET` 0x4000_4088, `FB_MISC_SW_RST_CTL` 0x4000_4094) → `PMU->GEN_PURPOSE_0 = 0` → **`PMU->FB_ISOLATION = 0`**. `load_fpga_with_mem_init()` also writes RAM init contents. Clock rates come from `s3x_pwrcfg.c` (e.g. qf_helloworldhw: C21 = 48 MHz).

Pros: one M4 binary contains everything. Cons: bitstream (~230 KB of C source per header) lives in M4 flash/RAM; QuickLogic now calls this the legacy method.

### 8.2 Binary in SPI flash, loaded by the bootloader (`-dump binary`)

Since qorc-sdk v1.5.0 (bootloader v2.1, toolchain v1.3.1) the bootloader loads an **appfpga** image from flash, then the M4 app.

`<top>.bin` = header + bitstream bin + meminit bin + iomux bin:
- **Header:** FPGA bin version (v0.1), size + CRC of each section, reserved word.
- **Bitstream:** 32-bit words exactly as in `<top>.bit`.
- **Meminit:** per RAM block: start address (4 B), size (4 B), data.
- **IOMUX:** per used pad: register address (4 B), value (4 B).

Flash it with `qfprog` (board in programming mode: press RST, then USR within 5 s → green LED breathing):

```bash
qfprog --port /dev/ttyACM0 --appfpga top.bin --mode fpga --reset              # FPGA only
qfprog --port /dev/ttyACM0 --m4app app.bin --appfpga top.bin --mode fpga-m4 --reset
```

`--mode m4|fpga|fpga-m4` tells the bootloader what to load. Flash map (qorc bootloader):

| Region | Start | Size |
|---|---|---|
| bootloader | 0x0000_0000 | 64 KB |
| bootfpga / appfpga / appffe / m4app metadata | 0x0001_0000 / 0x0001_1000 / 0x0001_2000 / 0x0001_3000 | 4 KB each |
| bootfpga (USB-serial image) | 0x0002_0000 | 128 KB |
| **appfpga** | 0x0004_0000 | 128 KB |
| appffe (future) | 0x0006_0000 | 128 KB |
| m4app | 0x0008_0000 | 440 KB |

Older QuickLogic flash tooling (BL0/BL1 file system, `qlflash.exe`) stored the fabric image as `MCU_FPGA.bin` — see the [Flash Tool User Guide](<QL_Flash_Tool_User_Guide.md>).

### 8.3 J-Link over SWD (`-dump jlink`)

`<top>.jlink` is a J-Link Commander script that writes the configuration over SWD. Boot the board in debug mode, then `JLinkExe -CommanderScript top.jlink` (qorc-onion-apps wraps this as `make load-jlink`, combining the FPGA script and M4 binary).

### 8.4 OpenOCD over SWD (`-dump openocd`, toolchain v1.3.0+)

`<top>.openocd` defines a Tcl proc `load_bitstream`:

```bash
openocd -f interface/<adapter>.cfg -f target/eos_s3.cfg -f top.openocd -c init -c "reset halt"
# then from arm-none-eabi-gdb:  monitor load_bitstream
```

Works with J-Link, FT2232H, ST-Link v2, CMSIS-DAP, picoprobe (qorc-onion-apps `make load-openocd`, `QORC_OCD_IF_CFG`).

**Important:** loading your own FPGA image replaces QuickFeather's USB-serial gateware, so the USB port no longer shows up as a serial device — use the hardware UART (IO_44/IO_45) with a USB-UART cable for the console.

---

## 9. How the SDK builds it

### qorc-sdk M4 + FPGA apps (`qf_apps/*/GCC_Project/makefiles/Makefile_common`)

```make
SYMBIFLOW_WARN_PATTERN="^Warning [0-9]\{1,\}:.*no timing specification"
$(MAIN_FPGA_RTL_DIR)/$(FPGA_RTL_OBJ): $(R_FILES)
	ql_symbiflow -compile -src $(MAIN_FPGA_RTL_DIR) -d ql-eos-s3 -t $(RTL_TOP_MODULE) \
	  -v $(FPGA_RTL_SRCS) -p quickfeather.pcf -P PU64 -dump header | grep -v $(SYMBIFLOW_WARN_PATTERN)
```

`make` in `GCC_Project` rebuilds the header when any RTL changes, then compiles the M4 code that includes it. The "no timing specification" warnings are filtered out.

### Standalone FPGA projects (`qorc_apps_au/qorc_helloworldfpga/fpga/Makefile`, qorc-onion-apps)

```make
export QORC_FPGA_TOP_MODULE=helloworldfpga
export QORC_FPGA_PACKAGE=PU64              # PD64/PU64/WR42
export QORC_FPGA_PCF_FILE?=<first *.pcf in rtl/>
export QORC_FPGA_DEVICE=ql-eos-s3
ql_symbiflow -compile -src $(QORC_FPGA_RTL_DIR) -d $(QORC_FPGA_DEVICE) -t $(QORC_FPGA_TOP_MODULE) \
  -v $(FPGA_RTL_SRCS) -p $(QORC_FPGA_PCF_FILE) -P $(QORC_FPGA_PACKAGE) -dump binary openocd jlink
```

qorc-onion-apps top-level targets: `make` / `make fpga`, `make clean`, `make load-jlink`, `make load-openocd`, `make flash` (`QORC_PORT=/dev/ttyACM0`), plus VS Code tasks and Cortex-Debug launch configs.

### s3-gateware IP projects

```bash
ql_symbiflow -compile -d ql-eos-s3 -P pu64 -v ${RTL_SRCS} -t top -p quickfeather.pcf -dump header > build.log
```

Pull shared IP from `../../../ip_modules/<IP>/rtl/` — the project must sit inside the s3-gateware tree.

---

## 10. Checklist and gotchas

1. **Environment:** `source envsetup.sh` (or the manual export + `conda activate`) in every shell; `which ql_symbiflow` must point into `fpga_toolchain_install/v1.3.1/quicklogic-arch-defs/bin`.
2. **WB_CLK ≤ 10 MHz** (TRM). Several examples exceed it (ADC example 18 MHz, qorc-onion-apps 12 MHz).
3. **Power-up order:** the TRM (p.340–341) says power the FB domain, enable C09, configure, then enable C16/C21/C02. The SDK's `load_fpga()` differs: it enables C02/C16 *before* writing the bitstream and clears isolation at the end. Both work on QuickFeather; follow the SDK loader unless you have a reason not to.
4. **Every Wishbone address must ACK** (bridge has no timeout) — keep the QL_Reserved default-ACK block.
5. **PCF hygiene:** every top port constrained; no lines for missing ports; IO_14/IO_15 (SWD) left out; check the package bonds out the pads.
6. **Use `-P` for the package**; give `-src` as a full path.
7. **Add an SDC** with your real clock periods, then read `top.log` and `report_timing.setup.rpt` — without it VPR just maximises Fmax and nothing tells you if you miss your target.
8. **RAM:** only symmetrical width combinations; RAM is inferred from ≥128 bits (v1.3.1).
9. **Verilog only;** IO pads come from top-level ports, not instantiations.
10. **Custom gateware replaces USB-serial** on QuickFeather — use the UART for logging.
11. **Bootloader path** needs bootloader v2.1+ and `-dump binary`; the header path works with any bootloader.
12. **Timing sim** with iverilog under-reports routing delay; cross-check with a full-SDF simulator if timing is tight.

---

## Sources

Local (in this knowledge base / `W:\2026\EOS`):
- [EOS S3 Technical Reference Manual r1.01a](<QL-S3-Technical-Reference-Manual.md>) — ch. 1, 2.3.4, 2.5.3, 27
- `qorc-sdk/envsetup.sh`, `qorc-sdk/quickstart.rst`, `qorc-sdk/Libraries/FPGA/src/fpga_loader.c`, `qf_apps/*/GCC_Project/makefiles/Makefile_common`, `qorc_apps_au/*` (Aurora, MatrixIDE), `s3-gateware/*/rtl/makefile`
- [QORC SDK Getting Started](<QORC_SDK_Getting_Started_QuickFeather.md>)
- [EOS S3 VPR timing constraint & report notes](<EOS_S3_VPR_Timing_Constraint_and_Report_Notes.md>)
- [Wishbone reference notes](<wishbone/EOS_S3_Wishbone_Reference_Notes.md>)
- [qorc-onion-apps overview](<designs/qorc-onion-apps.md>) and its READMEs/scripts (flash map, `.scaffolding` load scripts)
- [S3_FPGA_2xUART_GPIO](<designs/S3_FPGA_2xUART_GPIO.md>), [Pin planner log](<EOS_S3_Pin_Planner_Discussion_Log.md>), [Flash Tool User Guide](<QL_Flash_Tool_User_Guide.md>), Eclipse2 post-layout timing-simulation note (2026)

Web:
- [QuickLogic FPGA Toolchain documentation](https://quicklogic-fpga-tool-docs.readthedocs.io/en/latest/) — [Supported commands](https://quicklogic-fpga-tool-docs.readthedocs.io/en/latest/tutorial/Commandssupported.html), [Synthesis](https://quicklogic-fpga-tool-docs.readthedocs.io/en/latest/tutorial/PerformingDesignSynthesis.html), [Pack/place/route](https://quicklogic-fpga-tool-docs.readthedocs.io/en/latest/tutorial/RunningpackPlaceandRouteto.html), [Pre-layout sim](https://quicklogic-fpga-tool-docs.readthedocs.io/en/latest/tutorial/PerformingthePreLayoutSimula.html), [Post-layout sim](https://quicklogic-fpga-tool-docs.readthedocs.io/en/latest/tutorial/PerformingthePostLayoutSimul.html), [J-Link/OpenOCD](https://quicklogic-fpga-tool-docs.readthedocs.io/en/latest/tutorial/GeneratetheJlinkfile.html), [Header](https://quicklogic-fpga-tool-docs.readthedocs.io/en/latest/tutorial/GeneratetheASCIIheaderfilef.html), [Binary](https://quicklogic-fpga-tool-docs.readthedocs.io/en/latest/tutorial/GeneratetheBinaryFile.html), [PCF](https://quicklogic-fpga-tool-docs.readthedocs.io/en/latest/tutorial/PcfDescription.html), [Limitations](https://quicklogic-fpga-tool-docs.readthedocs.io/en/latest/tutorial/HardwareLimitationsandOnline.html), [S3B hard macros](https://quicklogic-fpga-tool-docs.readthedocs.io/en/latest/ram/S3BDeviceHardmacroResources.html), [RAM usage](https://quicklogic-fpga-tool-docs.readthedocs.io/en/latest/ram/RAMUsage.html), [Multiplier usage](https://quicklogic-fpga-tool-docs.readthedocs.io/en/latest/ram/MultiplierUsage.html)
- [quicklogic-fpga-toolchain (GitHub)](https://github.com/QuickLogic-Corp/quicklogic-fpga-toolchain) and [releases](https://github.com/QuickLogic-Corp/quicklogic-fpga-toolchain/releases)
- [qorc-sdk releases](https://github.com/QuickLogic-Corp/qorc-sdk/releases)
- [f4pga-arch-defs QuickLogic README](https://github.com/f4pga/f4pga-arch-defs/blob/main/quicklogic/README.md), [f4pga-examples getting started](https://raw.githubusercontent.com/chipsalliance/f4pga-examples/main/docs/getting.rst), [eos-s3 btn_counter Makefile](https://raw.githubusercontent.com/chipsalliance/f4pga-examples/main/eos-s3/btn_counter/Makefile) / [flow.json](https://raw.githubusercontent.com/chipsalliance/f4pga-examples/main/eos-s3/btn_counter/flow.json)
- [Yosys `synth_quicklogic`](https://yosyshq.readthedocs.io/projects/yosys/en/0.40/cmd/synth_quicklogic.html)
- [VPR SDC commands](https://docs.verilogtorouting.org/en/latest/vpr/sdc_commands/), [VPR basic flow](https://docs.verilogtorouting.org/en/latest/vpr/basic_flow/)
