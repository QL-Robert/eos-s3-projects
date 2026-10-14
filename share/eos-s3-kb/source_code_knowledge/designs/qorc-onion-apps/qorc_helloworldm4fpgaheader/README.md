---
title: "QORC HelloWorld M4 FPGA Application (LEGACY HEADER METHOD)"
source_file: "github.com/coolbreeze413/qorc-onion-apps/qorc_helloworldm4fpgaheader/README.rst"
source_commit: a960ca3f450fafde9da07547b35efe8e1caa2574
type: "readme"
topic: "eFPGA designs"
added: 2026-10-09
---

# QORC HelloWorld M4 FPGA Application (LEGACY HEADER METHOD)

## Intro

A template project with both m4 code and fpga design.

`note: the fpga design and m4 code in this template are independent and do not communicate.`

The fpga design is a simple LED-toggle, which toggles the red LED regularly.

The m4 code is a simple CLI application, which also executes a couple of I2C transactions.

Note that, this is practically the same as [qorc_helloworldm4fpga](../qorc_helloworldm4fpga/README.md) .

The difference in this project is that, the fpga code is built to generate a 'C Header' with a binary array containing the FPGA bitstream instead of a separate binary image.

This 'C Header' is included as regular C code and compiled into a single binary for the Cortex-M4, but contains code for both the Cortex-M4 as well as the FPGA.

So, technically, this is equivalent (from a debug/load/flash perspective) to a M4-only project.

This is more of a legacy method, and can be used if needed.

### Project Structure Guide

- top-level `Makefile` should be in the root of this directory
- if m4 code exists, it should have a top-level makefile at `GCC_Project/Makefile`
- if fpga design exists, it should have a top-level Makefile at `fpga/Makefile`
- fpga rtl verilog code should be in `fpga/rtl/`
- if the fpga rtl has API/driver code, the sources should be `fpga/src` and includes should be in `fpga/inc`

### Restructuring Existing QORC SDK Project

`note: this is only a guideline`

- top-level `Makefile`: copy into the existing project root directory

- copy `fpga/Makefile`: into the existing project `fpga/` directory

  `fpga/Makefile` should then be modified with correct 'top' verilog module name instead of `export QORC_FPGA_TOP_MODULE=helloworldfpga`

- compare `GCC_Project/` with this project, and:

  - top-level `GCC_Project/Makefile`: copy and replace from this template

    diff: adds QORC_SDK_PATH check, and removes extra 'FPGA' (loader) dependency, as it is already covered by `GCC_Project/makefiles/Makefile_Libraries`

  - `GCC_Project/makefiles/Makefile_common`: copy and replace from this template

    diff: removes fpga design build rules

  - `GCC_Project/makefiles/Makefile_appfpga`: copy and replace from this template

    diff: removes fpga design build variables

  - `GCC_Project/makefiles/Makefile_appdir`: copy and replace from this template

    diff: removes unnecessary source file filters for m4-code

  For any other diffs, use your discretion.

- copy the `.scaffolding` directory into the root of the existing project

- \[VS Code\] copy the `.vscode` directory into the root of the existing project

  delete any existing `settings.json` file in the `.vscode` directory

  copy the `settings.template.jsonc` as `settings.json`, adjust the values in the file according to the instructions at the top of the file.

## Usage

Once the fpga design and m4 code is loaded and running (load using debugger/reset after flashing on the board) :

- you should see the red LED toggling periodically (fpga design)
- you should see a couple of I2C transactions, and a banner and CLI on the EOS-S3 UART at IO_44/IO_45 (m4 code)

## How To

### Command Line Usage

`note: all the commands below are run from the root of this directory.`

#### Initialize Environment

Before clean/build/load/flash, ensure that the bash environment is setup by doing the below:

1.  Ensure that QORC-SDK is initialized and ready:

    ``` bash
    source ../../envsetup.sh
    ```

    ``` none
    note: assumes this repo 'qorc-onion-apps' is cloned into the QORC SDK dir, at the same level as qf_apps
    ```

    In general, use:

    ``` none
    source <QORC_SDK_PATH>/envsetup.sh
    ```

2.  \[Only\] If you are using the RP2040/Pico as a debugger (picoprobe), then ensure that the RaspberryPi flavor of OpenOCD is initialized and ready:

    ``` bash
    source .scaffolding/onion_openocd_picoprobe_setup.sh
    ```

3.  If you want to use the SVD file for EOS-S3 to watch registers while debugging, then ensure that the SVD file is initialized and ready:

    ``` bash
    source .scaffolding/onion_svd_setup.sh
    ```

    ``` none
    note: the SVD file is in very early alpha and missing many registers, use with discretion!
    ```

    To force download of latest SVD file from repo and replace the existing one, use:

    ``` bash
    source .scaffolding/onion_svd_setup.sh force
    ```

#### Clean/Build/Load/Flash (Command Line)

- Clean using:

  fpga: `make clean-fpga`

  m4: `make clean-m4`

  both: `make clean`

- Build using:

  fpga: `make fpga`

  m4: `make m4`

  both: `make`

- Load and run the code/design on the board using JLinkExe, using:

  (assumes the board has been booted in DEBUG mode)

  ``` bash
  make load-jlink
  ```

- Load and run the code/design on the board using OpenOCD, using:

  (assumes the board has been booted in DEBUG mode)

  ``` bash
  export QORC_OCD_IF_CFG=/path/to/inteface/cfg    # needs to be done only once in the current shell
  make load-openocd
  ```

  The interface cfg file depends on the debug adapter chosen.

  Here are a few common adapters that can be used with the EOS_S3:

  1.  JLink Adapters: `export QORC_OCD_IF_CFG=.scaffolding/jlink_swd.cfg` (available in the current dir)
  2.  FT2232H Boards: `export QORC_OCD_IF_CFG=.scaffolding/ft2232h_swd.cfg` (available in the current dir)
  3.  STLinkv2 Adapters: `export QORC_OCD_IF_CFG=interface/stlink-v2.cfg` (available in the OpenOCD install scripts dir)
  4.  DAPLink Adapters: `export QORC_OCD_IF_CFG=interface/cmsis-dap.cfg` (available in the OpenOCD install scripts dir)
  5.  picoprobe: `export QORC_OCD_IF_CFG=interface/picoprobe.cfg` (available in the OpenOCD install scripts dir, only if RaspberryPi flavor OpenOCD has been initialized)

  Practically, any adapter that supports OpenOCD and SWD can be used with the appropriate cfg file passed in.

- Flash and run the code/design on the board using qfprog:

  (assumes the board is put into `programming` mode)

  ``` bash
  export QORC_PORT=/path/to/serial/port   # needs to be done only once in current shell
  make flash
  ```

  Set the serial port as applicable, this is generally `export QORC_PORT=/dev/ttyACM0`

### VS Code Usage

#### Dependencies

- VS Code Extension: `ms-vscode.cpptools`  
  link: <https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools>  
  why: C/C++ Intellisense, Debugging  

- VS Code Extension: `marus25.cortex-debug`  
  link: <https://marketplace.visualstudio.com/items?itemName=marus25.cortex-debug>  
  why: Cortex-M Debug Launch Configuration  

- VS Code Extension: `augustocdias.tasks-shell-input`  
  link: <https://marketplace.visualstudio.com/items?itemName=augustocdias.tasks-shell-input>  
  why: Scan serial-ports for `flash` task, Select FPGA '.openocd' file for `Debug (OpenOCD)` debug launch config  

#### Initialize Project Configuration

The first time the project is going to be used from VS Code, we need to do the following:

1.  copy `.vscode/settings.template.jsonc` as `.vscode/settings.json`

    Ensure the following variables are correctly defined:

    ``` none
    "qorc_sdk_path" : "${workspaceFolder}/../..",
    ```

    In VS Code:

    `${env:HOME}` refers to \$HOME of the current user

    `${workspaceFolder}` refers to the current directory

    Remaining variables don't need to be changed.

2.  Open the current directory in VS Code using `File > Open Folder` menu

    - To be able to run the 'flash' task or 'Debug (OpenOCD)' launch config, remember to install the extension: `augustocdias.tasks-shell-input`
    - To be able to 'debug' the code with gdb, remember to install the extension: `marus25.cortex-debug`

    On opening the folder, VS Code should prompt to install these "recommended extensions", if not already installed, select `Install All` to automatically install them.

#### Clean/Build/Load/Flash (VS Code)

Any "task" can be run in VS Code using the `Terminal > Run Task` menu, which shows a drop down list of tasks

-OR-

Using keyboard shortcuts: `ctrl+p` and then type `task<space>`, which shows a drop down list of tasks

- Clean using:

  - fpga: run the `clean-fpga` task
  - m4: run the `clean-m4` task
  - both: run the `clean` task

- Build using:

  - fpga: run the `build-fpga` task
  - m4: run the `build-m4` task
  - both: run the `build` task

- Load and run the code/design on the board using JLinkExe, using:

  (assumes the board has been booted in DEBUG mode)

  run the `load (JLink)` task

- Load and run the code/design on the board using OpenOCD, using:

  (assumes the board has been booted in DEBUG mode)

  run the `load (OpenOCD)` task

  This will show a drop down menu with the options of debug adapters currently tested:

  - JLink Adapters `.scaffolding/jlink_swd.cfg`
  - FT2232H Boards `.scaffolding/ft2232h_swd.cfg`
  - STLinkv2 Adapters `interface/stlink-v2.cfg`
  - DAPLink Adapters `interface/cmsis-dap.cfg`

  select the appropriate one.

- Load and run the code/design on the board using OpenOCD and picoprobe, using:

  (assumes the board has been booted in DEBUG mode)

  run the `load (OpenOCD-picoprobe)` task

- Flash and run the code/design on the board using qfprog:

  (assumes the board is put into `programming` mode)

  run the `flash` task

  This will show a 'pickstring' drop down menu with the available serial ports in the system, select the appropriate one.

  (This is usually `/dev/ttyACM0`)

- `load-fpga-debug (JLink)` : This is a special task required only while debugging the code with JLink.

  Refer to the Debug sections for details.

- `x-get-ports` : this is an **internal** task, which is used by the `flash` task to obtain a list of available serial ports on the system to use for flashing. This list is displayed to the user as a 'pickstring' dropdown menu, as described in the `flash` task above.

#### Debug

- Debug the code via JLink :
  1.  To bring up the `Run and Debug` view, select the Run icon in the Activity Bar on the side of VS Code.
  2.  Select `Debug (JLink)` from the drop down at the top of the side bar
  3.  Start Debugging by clicking the green `Play Button`
  4.  The code should load and break at `main()`
  5.  Run the `load-fpga-debug (JLink)` task at this point, to load the FPGA design
  6.  Resume/Continue debugging using the blue `Continue/Break` button at the top or using `F8`
- Debug the code via OpenOCD :
  1.  To bring up the `Run and Debug` view, select the Run icon in the Activity Bar on the side of VS Code.

  2.  Select `Debug (OpenOCD)` from the drop down at the top of the side bar

  3.  Start Debugging by clicking the green `Play Button`

  4.  A drop-down menu appears to select the debug adapter being used, currently the choices are:

      - `.scaffolding/jlink_swd.cfg`
      - `.scaffolding/ft2232h_swd.cfg`
      - `interface/stlink-v2.cfg`
      - `interface/cmsis-dap.cfg`

      More can be added in the `launch.json` file.

      Select the appropriate one.

  5.  The fpga bitstream (.openocd) should get loaded, then the m4 code should load and break at `main()`

  6.  Resume/Continue debugging using the blue `Continue/Break` button at the top or using `F8`
- Debug the code via OpenOCD and picoprobe :
  1.  To bring up the `Run and Debug` view, select the Run icon in the Activity Bar on the side of VS Code.
  2.  Select `Debug (OpenOCD-picoprobe)` from the drop down at the top of the side bar
  3.  Start Debugging by clicking the green `Play Button`
  4.  The fpga bitstream (.openocd) should get loaded, then the m4 code should load and break at `main()`
  5.  Resume/Continue debugging using the blue `Continue/Break` button at the top or using `F8`
- Common Debugging Steps with the `Cortex-Debug` extension in VS Code:
  1.  Place breakpoints in the code by clicking near the line number
  2.  Use the `Step Over`, `Step Into`, `Step Out`, `Restart`, `Stop` buttons to control the debugging session

### References

1.  <https://code.visualstudio.com/docs/editor/debugging>
2.  <https://marketplace.visualstudio.com/items?itemName=marus25.cortex-debug>
3.  <https://mcuoneclipse.com/2021/05/09/visual-studio-code-for-c-c-with-arm-cortex-m-part-4/>
