---
title: "EOS S3 Pin Planner — Discussion & Change Log"
source_file: "EOS_S3_Pin_Planner_Discussion_Log.md"
type: "notes"
added: 2026-10-09
sha256: e4a91c169f29c3ec48118fb834ae861b562562e741b5686722cfee6f4a532587
---

# EOS S3 Pin Planner — Discussion & Change Log

A record of the requests, decisions, findings and fixes made while iterating on the **EOS S3 Pin Planner** (`pin_planner.html`), a client-side tool that generates a `.pcf` FPGA constraint file and a firmware `pincfg_table.c` from one pin-assignment session, for QuickFeather, QuickThing Plus and Custom boards.

Standing instruction throughout: **if hardware-critical information is missing, ask rather than assume.**

---

## 1. Requests, in order

| # | Request | Outcome |
|---|---------|---------|
| 1 | Boot mode / FPGA-in-use / interfaces-required feature | Master/Slave boot selector, "FPGA fabric in use" toggle (hides FBIO options when off), and an Interfaces Required checklist (UART, J-Link, I2C, SPI, I2S, PDM). |
| 2 | Check QuickFeather pinout and peripheral availability against the official User Guide (Rev 1.2.1) | Pinout rebuilt from the guide; per-board interface candidate pins added. |
| 3 | Remove the "Pins physically available on this board (comma-separated, 0–45)…" field | Removed everywhere, including Custom board (user's explicit choice after the consequence was raised). Custom board now treats all 46 pins as available. |
| 4 | "For QuickFeather use the attached pin map" (`QuickFeather_IO_Map.csv`) | CSV adopted as the authoritative per-pin source; supersedes earlier PDF-derived notes where they conflict. |
| 5 | "Why are UART, JLink, I2C, SPI, I2S and PDM marked with an X?" | Root cause found and fixed (stale saved state — see §3). |
| 6 | Add Bidirectional pin direction; test `pincfg.c` for correctness | Bidirectional added end to end; generated C file compile-tested (see §4). |
| 7 | Add PDM input to Interfaces Required | New "PDM input (mic)" entry, separate from "PDM output (AP_PDM)". |

---

## 2. QuickFeather pin facts (from the official guide and the IO map CSV)

- Pins 0–45 are wired somewhere, **except 9, 26, 35, 37, 39, 41, 42** (not present on the board).
- Key dedicated pins:
  - **UART:** TX = IO_44, RX = IO_45 (J3)
  - **SWD / J-Link:** CLK = IO_14, DATA = IO_15 (J6)
  - **I2C0:** SCL = IO_0, SDA = IO_1 (J2; shared with the onboard accelerometer and pressure sensor)
  - **SPI master:** CLK = IO_34, MISO = IO_36, MOSI = IO_38 (J3; shares the bus with the onboard boot flash), plus CS2 = IO_27 (J2)
  - **I2S:** WCLK = IO_23, DATA = IO_24, CLK = IO_31 (J8)
  - **Onboard PDM mic:** Data = IO_28, CLK = IO_29 (J8)
  - **LEDs:** IO_18 (blue), IO_21 (green), IO_22 (red); **user button:** IO_6; **accelerometer interrupt:** IO_3; **host interrupt:** IO_43
- **Discrepancy flagged and resolved:** an earlier reading of the guide suggested IO_32/IO_33 were a second I2C bus ("I2C1"). The user-supplied CSV lists them as plain IO with no additional function, so the I2C1 claim was removed (and called out in the tool's Notes & Assumptions panel).

---

## 3. Bugs found and fixed

1. **Stale saved state made interfaces show an X.** `ensureBoard()` only set a board's pin list the first time that board was seen, so anyone who had used an earlier version kept the old, narrow pin list forever. It now refreshes the pin list from the presets every time (safe because the list is no longer user-editable). Verified by a test that pre-seeds the old saved data.
2. **VHDL directions never matched the checker's vocabulary.** The VHDL parser returned `in` / `out` / `buffer`, while the direction-mismatch check expected `input` / `output` / `inout`, so VHDL designs silently skipped the check. Directions are now normalized.
3. **Top-level ports table didn't refresh the issues panel.** Changing a port's Direction dropdown updated state but never re-ran the HDL check. Fixed.
4. **Interface candidate model was too generic.** Interface availability now uses confirmed per-board pins where known (currently QuickFeather), falling back to chip-wide candidates otherwise; some interfaces also declare required pads (e.g. PDM output needs IO_39).

---

## 4. New features in the latest round

### Bidirectional direction
- Pin table Direction now offers **Output / Input / Bidirectional**.
- Generated firmware uses `.ucMode = PAD_MODE_OUTPUT_EN | PAD_MODE_INPUT_EN` for Bidirectional pins.
- **Unverified assumption:** this OR'd macro pairing is a best guess. It has not been checked against the real `eoss3_hal_pad_config.h` (not available in the build environment) and is flagged in the tool's Notes. **Please confirm against your SDK.**
- The HDL direction-mismatch check now handles `inout` ports, and treats Bidirectional pins as compatible with any declared direction.

### PDM input (mic)
- New Interfaces Required entry. On QuickFeather it maps to IO_28 (Data) / IO_29 (CLK), and needs at least two free pads.
- Distinct from **PDM output (AP_PDM)**, which is unavailable on QuickFeather because it needs IO_39.

### Testing `pincfg_table.c`
- The real SDK headers aren't available here, so "correct" was tested as **structural C validity**: the generated file is compiled with `gcc -Wall` against stub headers that define the `PadConfig` struct and every macro token the file uses.
- The test configures Output, Input and Bidirectional pins, FBIO and dedicated-peripheral functions, and an irregularly named macro pad (`PAD6_FUNC_SPI_SENSOR_MOSI`). It compiles cleanly.
- **Limit of the test:** it proves the file is well-formed C, not that the macro *values* match the real SDK.

---

## 5. Test status

17 Playwright/gcc tests, all passing at last run: core planner behavior, FBIO handling, irregular macro pads, all-46-pin assignment, filenames, HDL checks (Verilog and VHDL, tables, migration, direction), focus handling, boot mode, QuickFeather pinout, stale-state migration, bidirectional, PDM input, and the `pincfg.c` compile check.

---

## 6. Delivery status and open items

- Latest build delivered to the conversation as `pin_planner.html`.
- The hosted artifact (`eos-s3-pin-planner`) was **not** updated for this round: the link to the user's computer was down at that moment. It needs a re-publish once the link is back.
- **Open for the user:**
  1. Confirm the Bidirectional `.ucMode` macro against the real SDK header.
  2. Confirm the SPI "conflict" result on QuickFeather with Master boot (only one of the three typical SPI pads is free because Master boot reserves IO_34/35/36/38/39) is the intended behavior.
  3. Re-publish the artifact when the computer link is available.
