---
title: "QORC SDK — Getting Started on QuickFeather"
source_file: "attachment.txt (text of the qorc-sdk README; original: source_code_knowledge/README.rst)"
type: "notes"
topic: "QORC SDK getting started"
added: 2026-10-09
---

# QORC SDK

QuickLogic Open Reconfigurable Computing (QORC) SDK provides components needed to get started on the QuickLogic's EOSS3 device and open source development boards such as Quickfeather.

*(GitHub Workflow Status / Read the Docs badges)*

Currently, the following boards are supported:

- Quickfeather Development Kit
- SparkFun Thing Plus
- Qomu Development Kit

## Getting started on Quickfeather board

Easiest way to get started on quickfeather development kit is to build and run example application projects included in this SDK on a quickfeather development kit.

### Pre-requisites

#### Software

- Clone this repository using: `git clone https://github.com/QuickLogic-Corp/qorc-sdk`
- Navigate to the directory where the repo is cloned: `cd qorc-sdk`
- Install/Initialize all required tooling using: `source envsetup.sh`

For detailed steps or manual installation of each of the tools needed, refer to the docs here: Quickstart

#### Hardware

- Quickfeather development kit
- A micro USB cable
- [Optional] A serial-to-USB cable
- [Optional] J-Link Debug probe

## Baremetal Example

The `qf_baremetal` app tests `qf_baremetalsetup` which sets up the power domains and clocks without using the `S3X_CLK_XXX` management, or the power management schemes. As a result the code is smaller and simpler, however all of the responsibility is on the user to get the right power domains enabled, and the clocks set correctly.

## Lesson #1a: M4 only – qf_helloworldsw

This section describes how to build and run the qf_helloworldsw project.

1. Navigate to qf_helloworldsw build folder and run make

   ```bash
   cd qorc-sdk/qf_apps/qf_helloworldsw/GCC_Project
   make
   ```

2. Reset QuickFeather board and press ‘user button’ while blue LED is flashing.
   - Should switch to mode where green LED is breathing.
   - If green LED not breathing, press reset again and ‘user button’ within 5 seconds of releasing reset (while blue LED is still flashing)

3. With green LED breathing, program qf_helloworldsw app into QuickFeather:

   ```bash
   qfprog --port /dev/ttyXX --m4app output/bin/qf_helloworldsw.bin
   ```

   replace `/dev/ttyXX` with the actual device path.

4. After programming has completed, reset the QuickFeather board and do not press the user button.
   - Blue LED should flash for 5 sec and then load the m4app and run it.

5. Run PuTTY or some other terminal emulator and attach to the QuickFeather (NOTE: the port name will most probably be different than the port name used for programming).

You should see a banner that says:

*(image: qf_helloworldsw banner)*

The prompt `[0]` indicates that you are level 0 in the CLI menus system. Type `diag red` and you should see the red LED on QuickFeather light up

Type `help` and you should see:

*(image: qf_helloworld CLI Help)*

Which lists what is in the top-level CLI menu:

- `diag` is a user defined sub-menu
- the others are there by default

Type `diag` to enter the diag sub-menu. You should see

*(image: qf_helloworld CLI diag)*

Where the `[1] diag` indicates that you are in a 1st level submenu called diag

Type `help` to get help for this menu and you should see:

*(image: qf_helloworld CLI diag sub-menu)*

You can try these by typing `red` (should turn the red led off), `green` and so forth. Note that if you are level 0, you can access submenu elements by typing `submenuname submenu action`, which is what we did earlier when we typed `diag red`

## Lesson #1b: M4 only – modify qf_helloworldsw

1. Using the editor of your choice, edit `qorc-sdk/qf_apps/qf_helloworldsw/src/main.c`. Change the line

   ```c
   dbg_str("\n\nHello world !!\n\n")
   ```

   to say something else. Save the changes

2. Now naviagte to qf_helloworldsw build folder and run make.

   ```bash
   cd qorc-sdk/qf_apps/qf_helloworldsw/GCC_Project
   make
   ```

3. Reset QuickFeather board and press ‘user button’ while blue LED is flashing.
   - Should switch to mode where green LED is breathing
   - If green LED not breathing, press reset again and ‘user button’ within 5 seconds of releasing reset

4. With green LED breathing, program the updated qf_helloworldsw app into QuickFeather:

   ```bash
   qfprog --port /dev/ttyXX --m4app output/bin/qf_helloworldsw.bin
   ```

5. After programming has completed, reset the QuickFeather board and do not press the user button.
   - Blue LED should flash for 5 sec and then load the m4app and run it

6. Run PuTTY or some other terminal emulator and attach to the QuickFeather (NOTE: the port name will most probably be different than the port name used for programming).

You should see a banner and then your changed message.

## Lesson #2a: FPGA only – qf_helloworldhw

1. Navigate to qf_helloworldsw build folder and run make.

   ```bash
   cd qorc-sdk/qf_apps/qf_helloworldhw/GCC_Project
   make
   ```

2. Reset QuickFeather board and press ‘user button’ while blue LED is flashing.
   - Should switch to mode where green LED is breathing
   - If green LED not breathing, press reset again and ‘user button’ within 5 seconds of releasing reset

3. With green LED breathing, program qf_helloworldhw app into QuickFeather:

   ```bash
   qfprog --port /dev/ttyXX --m4app output/bin/qf_helloworldhw.bin
   ```

4. After programming has completed, reset the QuickFeather board and do not press the user button.
   - Blue LED should flash for 5 sec and then load the m4app which will load the FPGA and run that
   - You should see the green LED flashing about 3 times/second.

You will not see QuickFeather mounted on USB, because now the FPGA is used for the custom FPGA code, not the standard USB2SERIAL code. And because of this you cannot use PuTTY to monitor the application. (See Lesson#3 for how to monitor applications while running custom FPGA code).

### How does this work

If you look at `main.c` you will find the following code fragment:

```c
load_fpga(sizeof(axFPGABitStream),axFPGABitStream);     // Load bitstream into FPGA
S3x_Clk_Enable(S3X_FB_21_CLK);                          // Start FPGA clock
S3x_Clk_Enable(S3X_FB_16_CLK);
```

The array, `axFPGABitStream`, is located in `fpga/rtl/helloworldfpga_bit.h` which is generated from the Verilog by ql_symbiflow

What the `load_fpga()` does is take the bitstream from array `axFPGABitSTream` and program the FPGA

What the `S3x_Clk_Enable(S3X_FB_21_CLK)` does is to enable CLK 21 which is one of two clocks from the M4 that drive the FPGA

The frequency of the clock is specified in `src/s3xd_pwrcfg.c` to be 48MHz:

```c
[CLK_C21] = { .name = "C21", .clkd_id = CLK_C21, .type = SRC_CLK, .sync_clk = SYNC_CLKD (0, 0, 0), .cru_ctrl = CRU_CTRL (0x34, 0x1fe, 9, 0x38, 0x70, 0x1, 8), .def_max_rate = (F_48MHZ), .init_state = INIT_STATE(F_48MHZ, 1, INIT_GATE_OFF),},
```

## Lesson #2b: FPGA only – modify qf_helloworldhw

1. Using the editor of your choice, edit `qf_apps/qf_helloworldhw/fpga/rtl/helloworldfpga.v`
   - Change the terminal counter from 4000000 to 2000000
   - Change the `assign greenled = led` to `assign redled = led`
   - Save the changes

2. Activate the conda script from quicklogic-fpga-toolchain and add it's binaries to PATH. (This step can be skipped if you have installed the toolchain in the current terminal window and session).

   ```bash
   export INSTALL_DIR="specify the installpath of fpga-toolchain"
   export PATH="$INSTALL_DIR/install/bin:$INSTALL_DIR/install/bin/python:$PATH"
   source "$INSTALL_DIR/conda/etc/profile.d/conda.sh"
   ```

3. Navigate to qf_helloworldhw build folder and run make (note: for make use ql_symbiflow you will have to activate the ql_symbiflow conda)

   ```bash
   cd qf_apps/qf_helloworldhw/GCC_projects
   conda activate
   make
   conda deactivate
   ```

4. Reset QuickFeather board and press ‘user button’ while blue LED is flashing
   - Should switch to mode where green LED is breathing
   - If green LED not breathing, press reset again and ‘user button’ within 5 seconds of releasing reset

5. With green LED breathing, program the updated qf_helloworldhw app into QuickFeather:

   ```bash
   qfprog --port /dev/ttyXX --m4app output/bin/qf_helloworldhw.bin
   ```

6. After programming has completed, reset the QuickFeather board and do not press the user button
   - Blue LED should flash for 5 sec and then load the m4app which loads the new FPGA code and runs it
   - You should see the red LED flashing about 6 times/second

You will not see QuickFeather mounted on USB, because now the FPGA is used for the custom FPGA code, not the standard USB2SERIAL code. And because of this you cannot use PuTTY to monitor the application. (See Lesson#3 for how to monitor applications while running custom FPGA code

## Lesson #3: Advanced fpga M4 + FPGA– qf_advancedfpga

1. Go to directory `qf_apps/qf_advancedfpga/GCC_projects`
2. Activate conda, run make and deactivate conda
3. Connect to the QuickFeather UART
   - Connect a serial-to-USB cable to the QuickFeather board
   - Connect PuTTY to the serial port associated with the serial-to-USB cable
   - Set baud rate to 115200
4. Reset QuickFeather board and press ‘user button’ while blue LED is flashing
   - Should switch to mode where green LED is breathing
   - If green LED not breathing, press reset again and ‘user button’ within 5 seconds of releasing reset
5. With green LED breathing, program m4 app into QuickFeather

   ```bash
   python tinyfpgaprogrammer - -port /dev/ttyXX - -m4app output/bin/qf_advancedfpga.bin
   ```

6. After programming has completed, reset the QuickFeather board and do not press the user button
   - Blue LED should flash for 5 sec and then load the m4app and run it
7. The banner should be printed on PuTTY and then the CLI prompt
8. Switch to the ledctlr sub-menu by entering `ledctlr`
9. Set the color for timeslot 0 to blue by `color0 1` – led should go blue
10. Set the color for timeslot 1 to green by `color1 2` – no visible change
11. Set the color for timeslot 2 to red by `color2 4` – no visible change
12. Set the duration of timeslot 0 to 500ms by `duration0 500`
13. Set the duration of timeslot 1 to 500ms by `duration1 500`
    - Now the LED should display green for 500ms, then blue for 500ms and repeat
14. Set the duration of timeslot 2 to 1000ms by `duration2 1000`
    - Now LED should be blue for 500ms, green for 500ms and red for 1000ms and repeat

## Creating an application

To create an application start by choosing an existing application that is a close match to your end goal and simply copy the entire application directory giving the name you want. The make files assume that the application directory is two levels from the top-level directory. For example `qorc-sdk/qf_apps/` so you can either create your own project directory and copy the app there, for example `qorc-sdk/qf_myprojects/qf_myapp`, or put it in one of the existing project directories, for example `qorc-sdk/qf_apps/qf_myapp`

## Using Eclipse to Build/Debug applications

Please refer to Using Eclipse (`using_eclipse.rst` in the SDK root).

---

## Notes on this text (added for the knowledge base)

These are quirks in the original README, kept unchanged above:

- **Lesson #2a** step 1 says "Navigate to qf_helloworldsw build folder" but the command is for `qf_helloworldhw`, which is the right one.
- **Lesson #2b / #3** use `GCC_projects`; the folder in the SDK is `GCC_Project` (as in Lessons #1a/#2a).
- **Lesson #3** programming command `python tinyfpgaprogrammer - -port … - -m4app …` has split dashes; it means `--port` and `--m4app`. The other lessons use `qfprog` with the same arguments.
- The images (CLI banner, help screens) are not included in the source text; see the SDK `README.rst` / Read the Docs.
