---
title: "QuickLogic EOS S3 – Timing Constraint & Report Files (session notes)"
source_file: "eos-s3-vpr-timing-notes_1.md"
type: "notes"
added: 2026-10-09
sha256: 199e0fc1ae160b3b270746d231f6dd030eaf3400033e5c886d63b586ad547336
---

# QuickLogic EOS S3 – Timing Constraint & Report Files (session notes)

Context summary from a research session (27 Sep 2026) – for merging into another session.

## 1. ".scp" timing file
- No public `.scp` example exists for the EOS S3. Searched: QuickLogic-Corp/EOS-S3, qorc-sdk,
  quicklogic-fpga-toolchain, symbiflow-arch-defs, f4pga-examples, antmicro/yosys-SpDE-flow, docs, forum.
- Likely a legacy/internal format (SpDE/QuickWorks). Check an internal Aurora/QuickWorks install.

## 2. Timing/constraint formats actually used

| Flow | Constraint file | Passed as |
|---|---|---|
| Aurora (commercial) | `.qdc` (synthesis, placement, routing, timing, power, I/O in one file) | `aurora --compile_design ... -o <file>.qdc -d <device> -k <pkg> --run_all` |
| F4PGA / SymbiFlow (VPR) | `.sdc` (standard SDC, VPR subset) | `ql_symbiflow ... -s <file>.sdc` → `vpr --sdc_file` |
| Pin placement (VPR) | `.pcf` | `ql_symbiflow ... -p <file>.pcf -P PD64` |

### Aurora `.qdc` timing section (qorc-sdk `qorc_apps_au/qorc_helloworldfpga_au/fpga/rtl/helloworldfpga.qdc`)
```tcl
#timingengine
default_clock_period -value 10
device_cell_base_timing_report -value true
select_process_corner -flow_type {FPGA} -value {Typical}

#placer
fixplace_io -iotocell { \
    {blueled IO_18} \
    {greenled IO_21} \
    {redled IO_22} \
}
```

## 3. VPR place & route timing file (SDC)

Real EOS S3 example – `symbiflow-arch-defs/quicklogic/pp3/tests/features/install_test/counter_gclk/counter_gclk.sdc`:
```tcl
create_clock -period 100.0 clk
```

Multi-clock example – `quicklogic/qlf_k4n8/tests/design_flow/counter_4clk/counter_4clk.sdc`:
```tcl
create_clock -period 10.0 clk1 -waveform {0.000 5.000}
create_clock -period 10.0 clk2 -waveform {0.000 5.000}
```

Illustrative fuller template (VPR-supported commands; net names are placeholders):
```tcl
create_clock -period 50.0 -waveform {0.000 25.000} clk
create_clock -period 83.3 -name spi_clk
set_clock_groups -exclusive -group {clk} -group {spi_clk}
set_input_delay  -clock clk -max 5.0 [get_ports {btn*}]
set_output_delay -clock clk -max 5.0 [get_ports {led*}]
set_clock_uncertainty 0.5 [get_clocks clk]
set_false_path -from [get_clocks clk] -to [get_clocks spi_clk]
```

Flow details:
- Command: `ql_symbiflow -compile -src $PWD -d ql-eos-s3 -t top -v counter.v -p chandalar.pcf -P PD64 -s counter.sdc`
- SDC is pre-processed by `process_sdc_constraints.py` (uses the PCF to replace pin names with the net names mapped to them),
  then passed to `symbiflow_pack`, `symbiflow_place`, `symbiflow_route` → `vpr ... --sdc_file top.sdc`.
- If no SDC is given, an empty `top_dummy.sdc` is created → VPR optimises all clocks for max Fmax.
- Cell/routing delay data is NOT in the SDC: see `symbiflow-arch-defs/quicklogic/pp3/timings` and
  EOS-S3 repo `Timing Data Files/` (`*.lib` per corner, `qlal4s3b_RoutingDelays_*.csv`).

## 4. Setup timing report (VPR flow)

Primary file: **`build/report_timing.setup.rpt`**

| File | Contents |
|---|---|
| `report_timing.setup.rpt` | Worst constrained setup paths (critical path, slack) |
| `report_timing.hold.rpt` | Worst constrained hold paths |
| `report_unconstrained_timing.setup.rpt` / `.hold.rpt` | Paths not covered by the SDC |
| `pre_pack.report_timing.setup.rpt` | Estimated timing before packing |
| `top.log` / `vpr_stdout.log` | Final critical path delay, Fmax, setup WNS/TNS |

Notes:
- VPR rewrites the report after placement and again after routing → the final copy is post-route.
- Each path lists start/end points, cell + routing delays, arrival vs. required time, and slack (negative = setup failure).
- Control with `--timing_report_npaths` (default 100) and `--timing_report_detail {netlist|aggregated|detailed_routing}`.

## Sources
- https://github.com/QuickLogic-Corp/qorc-sdk
- https://github.com/QuickLogic-Corp/EOS-S3
- https://github.com/QuickLogic-Corp/symbiflow-arch-defs
- https://github.com/chipsalliance/f4pga-examples
- https://quicklogic-quicklogic-fpga-toolchain.readthedocs-hosted.com/en/latest/tutorial/eos-s3/RunningpackPlaceandRouteto.html
- https://github.com/verilog-to-routing/vtr-verilog-to-routing/blob/v8.0.0/doc/src/vpr/timing_constraints.rst

## Companion `.mcp.json`
Gives the other session GitHub access (for searching the repos above), a web fetch tool for the docs, and filesystem access
to a local EOS S3 project folder. Set `GITHUB_PERSONAL_ACCESS_TOKEN` in your environment and edit the filesystem path before use.
