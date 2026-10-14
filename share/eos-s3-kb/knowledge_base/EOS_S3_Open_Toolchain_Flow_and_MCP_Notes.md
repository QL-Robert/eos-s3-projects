---
title: "QuickLogic EOS S3 — Open-Toolchain Flow, Verified Notes & MCP Automation"
type: "reference"
topic: "FPGA design flow, place and route, bitstream, board bring-up, agent automation"
added: 2026-10-09
devices: "EOS S3, PolarPro 3 (pp3) fabric, QuickFeather (ql-eos-s3, PU64)"
toolchain: "SymbiFlow v1.3.1 — quicklogic-arch-defs 87dab559, Yosys 0.8 (QuickLogic build), VPR/VTR v8.0.0-rc2 dadca7ecf, quicklogic-fasm; host tools Yosys 0.33, Verilator 5.020, Icarus 12.0 on Ubuntu 24.04 / WSL"
sources: "First-hand: SPI master IP flow and QuickFeather self-test built and run on this toolchain (Sept–Oct 2026); Makefile, MCP server and parsers from that project; VPR/tatum and bitstream_to_binary.py source at the pinned commits; QuickFeather User Guide. Every entry is tagged VERIFIED / SOURCE / DOCS."
confidence_legend: "VERIFIED = observed in a real run of the real tools on a real design · SOURCE = read from the tool's own source or file format at the pinned commit, not yet seen in a live run · DOCS = from QuickLogic documentation only"
related: "EOS_S3_FPGA_Design_Flow.md (the general flow reference), EOS_S3_VPR_Timing_Constraint_and_Report_Notes.md, EOS_S3_Pin_Planner_Discussion_Log.md"
chunking: "every level-2 section is self-contained; split on level-2 headings. Section IDs (QL-SYN-03 etc.) are stable and citable."
---

# QuickLogic EOS S3 open-toolchain FPGA flow — knowledge base

Each section is written to stand alone when retrieved on its own. Device and tool names are repeated
rather than referred to as "it", so a chunk retrieved without its neighbours still makes sense. Every
factual entry carries a confidence tag: **[VERIFIED]**, **[SOURCE]** or **[DOCS]**.

---

## Terminology and aliases for the QuickLogic EOS S3 flow

`QL-TERM-01`

Names that refer to the same things, for query matching:

- **EOS S3** — QuickLogic SoC combining an Arm Cortex-M4F with an embedded FPGA fabric. Also written
  EOS-S3, EOSS3, QuickLogic EOS S3.
- **PolarPro 3 / pp3** — the FPGA fabric inside EOS S3. `pp3` is the Yosys family name:
  `synth_quicklogic -family pp3`. "Synthesising for PolarPro 3", "synthesising for EOS S3" and
  "synth_quicklogic -family pp3" all mean the same operation.
- **QuickFeather** — QuickLogic's open-source development board carrying an EOS S3 in a 64-pin QFN.
  Toolchain device string `ql-eos-s3`, package string `PU64`.
- **FPGA-only mode** — using the EOS S3 fabric without writing any Cortex-M4 firmware. The on-chip
  bootloader loads the FPGA image and supplies the fabric clock.
- **ql_symbiflow** — the QuickLogic command-line wrapper that runs synthesis, packing, placement,
  routing and bitstream generation for EOS S3.
- **QORC SDK** — QuickLogic's open reference SDK for EOS S3. Its pinned toolchain version is
  SymbiFlow v1.3.1, which is why this flow pins the same one.
- **FASM** — FPGA Assembly, the textual intermediate between routing and the bitstream.
  `genfasm` produces it, `qlfasm` turns it into a bitstream.
- **Aurora** — QuickLogic's newer toolchain built on Yosys, VPR and OpenFPGA, used for QuickLogic
  eFPGA IP. The EOS S3 flow described here is the older `ql_symbiflow` path; the structure ports.

---

## Two Yosys installations are required, and they must not share a PATH

`QL-ENV-01` · **[VERIFIED]**

A working EOS S3 open-toolchain setup has **two different Yosys builds**, used for different stages:

| Installation | Version | Used for |
| --- | --- | --- |
| Distribution Yosys (`apt install yosys`) | 0.33 | `synth_quicklogic -family pp3`, resource estimates, gate-level simulation, formal equivalence |
| The SymbiFlow toolchain's Yosys (conda) | 0.8, QuickLogic build from 2020 | only inside `ql_symbiflow`, during place and route |

**Rule: source the toolchain's `env.sh` only in a subshell.** The toolchain's `env.sh` puts the 2020
Yosys 0.8 first on `PATH`. Sourcing it from `.bashrc` or an interactive shell shadows the modern
Yosys, and every other stage then fails in ways that look like Yosys defects — missing commands,
unrecognised options, different cell names.

The correct pattern inside a Makefile recipe is one line that sources and runs together:

```make
source $(QL_ENV) && cd $(PNR_DIR) && ql_symbiflow -compile …
```

**Symptom of getting this wrong:** `synth_quicklogic` does not accept `-family pp3`, or commands such
as `scratchpad` or `setparam` are unknown. **Cause:** the 2020 toolchain Yosys is on `PATH`.
**Fix:** open a new shell that has not sourced `env.sh`.

---

## Installing the QuickLogic SymbiFlow v1.3.1 toolchain for EOS S3

`QL-INSTALL-01` · **[SOURCE]** (recipe assembled and scripted; blocked from running by a restricted network)

The QuickLogic EOS S3 place-and-route toolchain installs natively, without Docker, in about 2 GB,
by default into `~/quicklogic-toolchain`. Pinned components:

- **Miniconda pinned to `Miniconda3-py37_4.12.0-Linux-x86_64.sh`.** The installer's "latest"
  Miniconda can no longer resolve these packages; a Python 3.7 base is required.
- **`quicklogic-arch-defs` commit `87dab559`**, fetched from
  `https://storage.googleapis.com/symbiflow-arch-defs-install/quicklogic-arch-defs-87dab559.tar.gz`.
  This supplies `ql_symbiflow` and the EOS S3 architecture files.
- **conda channel `quicklogic-corp/label/ql`**, packages:
  `yosys=0.8.0_0003_e80fb742f_20201208_122808`, `yosys-plugins=1.2.0_0011_g21045a9`,
  `vtr=v8.0.0_rc2_2894_gdadca7ecf`, `python=3.7`.
- **pip:** `lxml`, `simplejson`, `intervaltree`, `python-constraint`, and
  `git+https://github.com/QuickLogic-Corp/quicklogic-fasm@57b6e60574a9d483dc94710d0d3ff42a62b4ec41`.
- Architecture: **x86_64 Linux only**.

**Network hosts that must be reachable:** `repo.anaconda.com`, `conda.anaconda.org`,
`storage.googleapis.com`, `github.com`. A corporate proxy or sandbox that blocks any one of these
fails the install; `conda.anaconda.org` and `storage.googleapis.com` are the ones most often blocked.

After installation the toolchain is used by sourcing `env.sh`, which activates the conda environment
and prepends `quicklogic-arch-defs/bin` and `quicklogic-arch-defs/bin/python` to `PATH`.

**Verification:** `ql_symbiflow`, `yosys`, `vpr`, `genfasm` and `qlfasm` must all be on the PATH that
`env.sh` produces.

---

## VPR fails to start on Ubuntu 24.04: libtbb.so.2 not found

`QL-INSTALL-02` · **[SOURCE]**

**Symptom:** `vpr` will not run after installing the QuickLogic SymbiFlow v1.3.1 toolchain on Ubuntu
24.04; `ldd $(command -v vpr) | grep "not found"` reports `libtbb.so.2`.

**Cause:** VPR v8.0.0-rc2 links against the older Intel TBB; Ubuntu 24.04 ships oneTBB, which has a
different soname.

**Fix:** inside the toolchain environment,

```bash
source ~/quicklogic-toolchain/env.sh
conda install -y -c conda-forge 'tbb<2021'
```

---

## Synthesising a design for EOS S3 (PolarPro 3) with Yosys

`QL-SYN-01` · **[VERIFIED]**

The complete Yosys invocation for EOS S3 / PolarPro 3 synthesis, as used in a working flow:

```bash
yosys -q -l synth.log -p "
    read_verilog rtl/spi_master.v ip/spi_master_ip.v;
    hierarchy -check -top spi_master_ip;
    scratchpad -set abc9.D 83333;
    synth_quicklogic -family pp3 -top spi_master_ip;
    opt_clean -purge;
    setparam -unset EQN t:LUT*;
    check -assert;
    tee -o stat.txt stat;
    write_verilog -noattr spi_master_ip_netlist.v"
```

Detecting support rather than guessing from a version number:

```bash
yosys -p 'help synth_quicklogic' | grep pp3
```

Checking for inferred latches after synthesis is worthwhile, because latch inference on this fabric
is always an error: grep the written netlist for `DLATCH` or `latch` and fail the build if present.

---

## Setting the clock/delay target for EOS S3 LUT mapping (there is no -clk option)

`QL-SYN-02` · **[VERIFIED]**

`synth_quicklogic` has **no clock-period option**. The LUT-mapping delay target for EOS S3 is set
through the ABC9 scratchpad variable, in picoseconds, before calling synthesis:

```
scratchpad -set abc9.D 83333;     # 83333 ps = 83.333 ns = 12 MHz
```

12 MHz is also the Yosys default and matches the EOS S3 bootloader's fabric clock in FPGA-only mode.

---

## Icarus Verilog cannot compile a pp3 netlist: {0{1'b0}} in LUT EQN parameters

`QL-SYN-03` · **[VERIFIED]**

**Symptom:** gate-level simulation of a `synth_quicklogic -family pp3` netlist fails to compile under
Icarus Verilog, on a parameter written as `{0{1'b0}}`.

**Cause:** Yosys writes the LUT equation string parameter `EQN` as `{0{1'b0}}` when it is empty.
Icarus Verilog rejects a zero-width replication.

**Fix:** strip the parameter after synthesis and before `write_verilog`:

```
setparam -unset EQN t:LUT*;
```

This affects only simulation of the Yosys-written netlist; the `ql_symbiflow` place-and-route flow
re-synthesises internally and is unaffected.

---

## The "Complex async reset for dff" Yosys warning on EOS S3 is benign

`QL-SYN-04` · **[VERIFIED]**

**Symptom:** `synth_quicklogic -family pp3` prints

```
Warning: Complex async reset for dff `\…'.
```

**Cause:** Yosys emits this while reading its own PolarPro 3 flip-flop model, not because of anything
in the user design.

**Action:** none. It is expected and harmless. Automated flows should classify it explicitly as a
known-benign warning so that an agent or a CI gate does not chase it. Every other warning from
`synth_quicklogic` deserves investigation.

---

## Cell types produced by EOS S3 / pp3 synthesis

`QL-SYN-05` · **[VERIFIED]**

Cells that appear in a Yosys `stat` report after `synth_quicklogic -family pp3`:

- `LUT1`, `LUT2`, `LUT3`, `LUT4` — fabric look-up tables; the EOS S3 fabric is LUT4-based.
- `dffepc` — flip-flop with clock enable, preset and clear. This is the fabric register.
- `gclkbuff` — global clock buffer; the only legal way onto the EOS S3 global clock network.
- `mux2x0`, `mux4x0`, `mux8x0` — hard mux chain cells.
- `inpad`, `outpad`, `bipad` — I/O pads.
- `qlal4s3b_cell_macro` — the SoC macro: the Cortex-M4 subsystem, clock sources and the fabric
  interface. One instance per design that uses SoC clocks.
- `logic_0`, `logic_1` — tie cells / constants.

A reasonable resource summary groups these as LUTs, flip-flops, pads, clock buffers, muxes, SoC macro
and constants.

---

## Gate-level simulation of an EOS S3 pp3 netlist: cell models and the duplicate-macro problem

`QL-SIM-01` · **[VERIFIED]**

Simulation models for PolarPro 3 cells ship with Yosys, under `$(yosys-config --datdir)/quicklogic/`:

- `cells_sim.v`
- `pp3_cells_sim.v`
- `lut_sim.v`

**Symptom:** Icarus Verilog reports a duplicate module definition of `qlal4s3b_cell_macro` when
compiling a pp3 netlist together with `pp3_cells_sim.v`.

**Cause:** `pp3_cells_sim.v` defines `qlal4s3b_cell_macro`, and so does the design's own behavioural
model of the SoC macro (or the netlist itself).

**Fix:** make a copy of `pp3_cells_sim.v` with that single module removed, and compile against the
stripped copy plus the design's own macro model. A short Python script that deletes one named module
from a Verilog file is enough.

---

## Formal equivalence checking RTL against an EOS S3 netlist: flatten the gold design

`QL-EQV-01` · **[VERIFIED]**

Yosys `equiv_make` / `equiv_induct` / `equiv_status` can prove a `synth_quicklogic -family pp3`
netlist equivalent to its source RTL.

**Symptom:** a handful of cells remain unproven on a netlist that is known to be correct.

**Cause:** the RTL (gold) side is hierarchical while `synth_quicklogic` flattens the gate (gate)
side, so the two designs do not correspond structurally.

**Fix:** run `flatten` on the gold design before `equiv_make`.

**Observed sensitivity:** with the gold side flattened, inverting the `INIT` truth table of a single
LUT4 in the netlist is detected, and `equiv_status` names the unproven signal. On a real SPI master
IP the check proved 66 of 66 cells.

This check is the mechanism that makes an AI-proposed RTL edit reviewable by machine rather than by
eye: either the netlist is proven equal to the RTL, or the differing signal is named.

---

## The EOS S3 SoC macro clock port has three different names across toolchain versions

`QL-MACRO-01` · **[VERIFIED]**

Even in FPGA-only mode, an EOS S3 design must take its fabric clock from the SoC macro
`qlal4s3b_cell_macro`. **The macro's clock port is named differently in each toolchain generation:**

| Port names | Toolchain |
| --- | --- |
| `Sys_Clk0`, `Sys_Clk0_Rst` | QuickLogic toolchain **v1.3.x** — the version the QORC SDK pins, and what `ql_symbiflow` expects here |
| `Clk_C16` | current F4PGA |
| `Clk16` | upstream Yosys's own pp3 model |

**Symptom:** elaboration fails with a port-not-found error on `qlal4s3b_cell_macro`, or the fabric
has no clock, when a design moves between the installed toolchain and distribution Yosys.

**Fix:** carry all three spellings in the source behind `` `ifdef `` guards and select per stage. A
working convention: no define = v1.3.x (`Sys_Clk0`), `-DF4PGA_CLK_C16` = current F4PGA,
`-DYOSYS_UPSTREAM_PP3` = upstream Yosys. Pre-layout synthesis with distribution Yosys uses
`-DYOSYS_UPSTREAM_PP3`; `ql_symbiflow` place and route uses the default.

---

## Running EOS S3 in FPGA-only mode: clock, reset and start-up state

`QL-BOARD-01` · **[DOCS]**

In FPGA-only mode on a QuickFeather (no Cortex-M4 firmware written by the user):

- The on-chip bootloader loads the FPGA application image and supplies the fabric clock at
  **12 MHz (83.333 ns)**.
- The clock must pass through a `gclkbuff` instance to reach the global clock network.
- **Register start-up values are not guaranteed in this flow.** Any state machine must be able to
  recover from an illegal state, and should reset the logic it drives at the start of each pass.
  Designs that assume power-up zeros can hang.

---

## Running place and route for EOS S3 with ql_symbiflow

`QL-PNR-01` · **[SOURCE]**

Full command line for a QuickFeather (EOS S3, PU64) design:

```bash
source ~/quicklogic-toolchain/env.sh
cd <clean staging directory containing the sources>
ql_symbiflow -compile -src "$PWD" -d ql-eos-s3 -P PU64 -t top \
    -v spi_master.v spi_master_ip.v spi_selftest_top.v top.v \
    -p quickfeather.pcf -s spi_selftest.sdc -dump binary
```

Options: `-d` device (`ql-eos-s3`), `-P` package (`PU64` for the QuickFeather's 64-pin QFN), `-t` top
module name, `-v` the Verilog sources, `-p` the `.pcf` pin constraints, `-s` the `.sdc` timing
constraints, `-dump binary` to emit `top.bin` directly. `-dump post_verilog` instead writes a
post-layout netlist and SDF, which is the entry point for post-layout timing simulation.

Two practical constraints:

- **`ql_symbiflow` writes its working state into the `-src` directory.** Copy the sources into a
  clean staging folder and run there, or build output scatters through the source tree.
- **`ql_symbiflow` cannot pass top-level parameters.** A parameterised design must be wrapped by a
  generated top-level module with the parameter values baked in.

Outputs and logs appear under `<src>/build/`: `top_synth.log`, `pack.log`, `place.log`, `route.log`,
`report_timing.setup.rpt`, `report_timing.hold.rpt`, and the bitstream `top.bin`.

---

## VPR route.log lines worth parsing for EOS S3 place and route

`QL-PNR-02` · **[SOURCE — exact print formats from VPR/VTR v8.0.0-rc2 `dadca7ecf`]**

Lines emitted by VPR that carry the result of an EOS S3 routing run:

```
Final critical path delay (least slack): 21.4471 ns, Fmax: 46.6264 MHz
Final setup Worst Negative Slack (sWNS): 0 ns
Final setup Total Negative Slack (sTNS): 0 ns
Final hold Worst Negative Slack (hWNS): 0 ns
Final hold Total Negative Slack (hTNS): 0 ns
Circuit successfully routed with a channel width factor of 100.
Circuit is unroutable …
Resource usage ...
Device Utilization: 0.07 (target 1.00)
```

`report_timing.setup.rpt` is tatum's format: `Startpoint:`, `Endpoint:`, `Path Type: setup`, a
cumulative delay table, then `slack (MET)` or `slack (VIOLATED)`.

Two reporting rules that prevent false confidence:

1. **Check routed vs unroutable before reporting timing.** A failed routing run still prints timing
   numbers, and they are meaningless.
2. **Check report freshness.** Build directories retain the previous run's logs. Compare report
   modification times against the time the current stage started, and report "not run" rather than
   returning an earlier run's Fmax.

---

## Pin constraints for EOS S3: the .pcf file

`QL-PCF-01` · **[VERIFIED syntax, DOCS pad map]**

EOS S3 pin constraints use a `.pcf` file. Syntax is one `set_io` per net; `#` starts a comment:

```
set_io sclk       IO_2
set_io cs_n       IO_13
set_io mosi       IO_25
set_io miso       IO_30
```

The right-hand name is the **EOS S3 pad number** (`IO_25`), not the QFN pin number.

QuickFeather pad map used by a working SPI self-test design:

| Net | Pad | QFN pin | Board connection |
| --- | --- | --- | --- |
| sclk | IO_2 | 6 | header J3.7 |
| cs_n | IO_13 | 55 | header J3.8 |
| mosi | IO_25 | 31 | header J3.9 |
| miso | IO_30 | 25 | header J3.10 |
| red_led | IO_22 | — | on-board LED_R, active high |
| green_led | IO_21 | — | on-board LED_G, active high |
| blue_led | IO_18 | — | on-board LED_B, active high |

**Pads to avoid on a QuickFeather:** `IO_34`, `IO_36`, `IO_38` (M4 SPI master, shared with the boot
flash); `IO_19`, `IO_20` (boot-strap pins); `IO_14`, `IO_15` (SWD); `IO_44`, `IO_45` (UART).

**Pull resistors:** the toolchain configures FPGA inputs with **no pull resistor**, so an
unconnected fabric input floats. A loopback self-test can rely on this: removing the jumper makes the
input float and the test genuinely fails rather than silently passing.

---

## Timing constraints for EOS S3: the .sdc file and the net-not-port rule

`QL-SDC-01` · **[VERIFIED]**

A minimal EOS S3 FPGA-only timing constraint, for the 12 MHz bootloader clock:

```
create_clock -period 83.333 clk
```

**VPR matches `create_clock` targets against netlist clock *nets*, not top-level ports.** The
constraint must name the net driven by the `gclkbuff` output — in the example above, `clk` — and not
the SoC macro port the clock came from.

**Symptom of getting this wrong:** the run completes, timing is reported, and the Fmax figure is
meaningless because the constraint matched nothing.

Paths to and from pads can reasonably be left unconstrained when the interface is slow relative to
the fabric clock; document that choice in the `.sdc` so the omission is not read as an oversight.

---

## The EOS S3 .bin bitstream container loaded by the QuickFeather bootloader

`QL-BIT-01` · **[SOURCE — `bitstream_to_binary.py` in the toolchain]**

Layout of the `.bin` file the QuickFeather bootloader loads:

```
header     8 × uint32 little-endian:
           version, bitstream size, bitstream crc,
           meminit size, meminit crc, iomux size, iomux crc, reserved
bitstream  <bitstream size> bytes
meminit    <meminit size> bytes
iomux      <iomux size> bytes of (address, value) uint32 LE pairs,
           one pair per pad register the design configures
```

Pad register addressing and fields:

- Pad *N*'s register address is `0x40004C00 + 4*N`.
- **Bit 11 = input enable.**
- **Bits 7:6 = pull**: 0 none, 1 up, 2 down, 3 keeper.

This makes three board-free checks possible on any built bitstream: the header sizes add up to the
file length; every pad named in the `.pcf` is actually configured by the iomux section; and every net
intended as an input really has input-enable set. The third check catches a silently floating input
before the board is ever connected.

---

## Programming a QuickFeather with an FPGA-only bitstream

`QL-PROG-01` · **[DOCS for the button sequence, SOURCE for the command]**

Put the QuickFeather into programming mode first: **press RST, then press USR while the LED blinks
blue.** The LED then breathes green, indicating the bootloader is waiting.

```bash
python tinyfpga-programmer-gui.py --port /dev/ttyACM0 \
    --appfpga path/to/top.bin --mode fpga --reset
```

`--appfpga` with `--mode fpga` writes **only the FPGA application image**; the bootloader images are
not touched, so this operation cannot brick the board.

Programmer and prerequisites: clone
`https://github.com/QuickLogic-Corp/TinyFPGA-Programmer-Application` with `--recursive`, and install
the Python packages `pyserial` and `tinyfpgab`.

---

## Programming a QuickFeather on a Windows COM port from WSL, without usbipd

`QL-PROG-02` · **[SOURCE — exercised against recorded mock interop commands]**

A flow running in WSL can program a QuickFeather on a Windows COM port without passing the USB device
through to Linux. The design flow stays in WSL and only the programmer runs on the Windows side.

Mechanics:

1. Convert the bitstream path and the programmer path to Windows form with `wslpath -w`. A programmer
   stored in WSL is reachable from Windows as `\\wsl$\<distro>\home\<user>\…` (newer Windows builds
   use `\\wsl.localhost\<distro>\…`).
2. Run it with Windows Python: `py.exe <programmer> --port COM14 --appfpga <windows path to top.bin>
   --mode fpga --reset`.

One-time setup, in Windows PowerShell:

```powershell
py -m pip install pyserial tinyfpgab
```

Variations: if Windows has `python.exe` but no `py` launcher, use `python.exe`. To use a copy of the
programmer stored on the Windows side instead of the WSL copy, point at its Windows path.

Worthwhile pre-flight checks before touching the board, each with a specific fix message: Windows
Python is reachable from WSL; `pyserial` and `tinyfpgab` are installed on the Windows side; Windows
actually enumerates the named COM port (`powershell.exe` can list them); the bitstream file exists.

**Alternative:** pass the board through to Linux with usbipd-win (`usbipd list`, then
`usbipd attach --wsl --busid <id>`) and use `/dev/ttyACM0`. This works but is more setup for no gain
when the Windows-interop route is available.

---

## Measured EOS S3 resource figures for calibration

`QL-DATA-01` · **[VERIFIED]**

Real numbers from `synth_quicklogic -family pp3` runs, useful as sanity checks on new results:

| Design | Result |
| --- | --- |
| SPI master IP, 8-bit data, clock divider 4 | 114 cells: 46 LUTs (1×LUT1, 17×LUT2, 20×LUT3, 8×LUT4), 39 flip-flops, 27 pads |
| Same IP, formal equivalence vs RTL | 66 of 66 cells proven |
| Same IP, RTL and gate-level simulation | 64 of 64 transfers, 0 errors, all four CPOL/CPHA modes |
| SPI self-test top (IP + loopback sequencer + LED logic), pre-layout | 202 LUTs, 118 flip-flops, 7 pads |
| Regression across data widths 2, 8, 16, 32 | all pass |

No post-layout figures have been measured. Any Fmax, channel-width or utilisation number in the test
fixtures of this flow is synthetic.

---

## Designing an MCP server around an FPGA flow: rules that proved necessary

`QL-MCP-01` · **[VERIFIED]**

Lessons from wrapping a QuickLogic EOS S3 make-based flow as an MCP server with one tool per stage.
These generalise to any toolchain.

- **Return parsed structured results, not raw logs.** Each tool returns pass/fail, counts, resource
  figures and named failing signals. The model should never grep a log.
- **`ok` must mean the design passed, not that `make` exited 0.** A simulation that prints
  `TEST RESULT: FAIL` under a make that returns 0 is a failure.
- **Distinguish a timeout from a failed check.** They imply completely different next actions.
- **Never return stale results.** After a failing stage, later stages' outputs from an earlier run
  are still on disk. Report them as `not_run` instead of returning them.
- **Make cannot see every variable.** Settings such as a simulation seed, waveform dumping or a
  synthesis delay target are not file dependencies, so `make <stage> SEED=7` reports "nothing to be
  done". Delete that stage's stamp file first and report the forced rerun.
- **Classify known-benign tool warnings explicitly** (see `QL-SYN-04`), or an agent spends its turn
  on them.
- **Any write to hardware takes two calls:** the first returns a plan and runs nothing; the second,
  with an explicit confirmation flag, performs it. Keep it out of any auto-approve list.
- **Pin the MCP SDK below 2.0** (`mcp>=1.2,<2`): version 2 renamed the FastMCP API and an unpinned
  install breaks server start-up.
- **FastMCP reads a tool's description from the docstring literal.** A docstring built by string
  concatenation produces no description, and the model then cannot tell the tools apart.
- **Context budget:** 22 tool definitions ≈ 7,500 tokens; a full-flow or place-and-route result
  ≈ 1,000 tokens. A local model needs ≥16k context and a reduced tool set.
- **Background jobs held in the server process are lost if the client restarts the server.** Results
  on disk should be readable by a separate "read the last run" tool.

---

## What this EOS S3 flow does not yet cover

`QL-GAP-01` · **[VERIFIED as of 2026-10-09]**

1. **No documentation knowledge base.** The flow can run tools but cannot explain a QuickLogic
   warning from vendor documentation. Competing vendor assistants (Lattice Prompt, AMD Ross) ship a
   retrieval index over their own documents; Ross also ships an air-gapped package.
2. **Timing exists only in the board flow.** The IP-level stages stop at synthesis; Fmax and slack
   come only from the QuickFeather place-and-route run.
3. **Post-layout timing simulation is not wired up.** `ql_symbiflow -dump post_verilog` produces the
   netlist and SDF; nothing runs the testbench against them yet.
4. **No Cortex-M4 side.** Register map, fabric-to-M4 bridge and driver are unbuilt, so only the
   fabric is covered.
5. **No internal logic analyser.** The board reports results through one LED. A capture block in the
   fabric, read out through the M4, would let the flow compare captured silicon behaviour against
   the simulation it already ran.
6. **Place and route, bitstream generation and COM-port programming have not been run against real
   hardware.** They are implemented and tested against mocks built from tool source.

---

## Reference sources for the QuickLogic EOS S3 open toolchain

`QL-REF-01`

- `quicklogic-arch-defs` commit `87dab559` — `ql_symbiflow` and the EOS S3 architecture files.
- `QuickLogic-Corp/quicklogic-fasm` — FASM to bitstream (`qlfasm`).
- `QuickLogic-Corp/TinyFPGA-Programmer-Application` — the QuickFeather programmer.
- QORC SDK — the reference for which toolchain version to match.
- VTR / VPR v8.0.0-rc2, commit `dadca7ecf` — authoritative for log and report formats.
- QuickFeather User Guide — IO map and J3 header pin table.
- Yosys `synth_quicklogic` documentation and the pp3 cell libraries under
  `$(yosys-config --datdir)/quicklogic/`.
