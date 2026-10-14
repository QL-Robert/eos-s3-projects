---
title: "QORC FPGA PWM Controller Application"
source_file: "github.com/coolbreeze413/qorc-onion-apps/qorc_fpga_pwmctrl/README.rst"
source_commit: a960ca3f450fafde9da07547b35efe8e1caa2574
type: "readme"
topic: "eFPGA designs"
added: 2026-10-09
---

# QORC FPGA PWM Controller Application

## Intro

This example application demonstrates one of the use-cases of the eFPGA core in the EOSS3.

There is no built-in PWM Controller available in the EOSS3.

The eFPGA on the EOSS3 can access all of the 46 pads (IO_0 to IO_45) and use it according to any design on the eFPGA.

In this application, we take the first 32 pads (IO_0 to IO_31) and enable usage as PWM pins via the eFPGA design.

To control the PWMs exposed in this way, from the M4, we use the AHB-Wishbone Interconnect between the M4 Subsystem and the eFPGA, hence making it possible to use it like any other peripheral on the M4 Subsystem.

Using a set of 32-bit registers, exposed over the AHB-Wishbone Interconnect, M4 code can just set bits on the registers and control the IO pads to set a duty-cycle/enable for PWM function.

## Usage

`note: ensure that you have connected a USB-UART adapter connected to the EOSS3 UART pins (IO_44/IO_45), and you have a serial terminal connected to that port at 115200 8N1.`

Once the board is flashed, and reset, you should see a pattern of 3 sets of Triple Magenta Blinks (after the flashing BLUE LED pattern put out by the bootloader as usual) indicating the code has loaded and started execution (FPGA and M4).

This pattern of 3 Triple-Magenta-Blinks is executed using the eFPGA based PWM Controller Design itself.

Each Triple-Magenta-Blink would be seen with 3 increasing brightness levels of the leds.

This can be see in the code of [src/main.c \[Line 85 - Line 131\]](src/main.c#L85-L131)

This is followed by a banner like the below on the serial terminal:

``` none
##########################
OnionApps FPGA PWM Controller Example
SW Version: qorc-onion-apps/qorc_fpga_pwmctrl
Feb 19 2021 18:57:15
##########################



Hello PWM CONTROLLER!

#*******************

Command Line Interface

App SW Version: qorc-onion-apps/qorc_fpga_pwmctrl

#*******************
FPGA Device ID: 0x0000c002
[0] > 
```

Enter the PWM Controller submenu using `pwmctrl` and then type `help` in the pwmctrl submenu for commands.

``` none
[0] > pwmctrl
[1] pwmctrl > help
help-path: pwmctrl
enpwm          - enpwm IO_X VAL(0-255)
dispwm         - dispwm IO_X
getpwm         - getpwm IO_X
exit           - exit/leave menu
help           - show help
?              - show help
help-end:
```

To set a GPIO as output with specific value, use `enpwm IO_PADNUMBER VALUE_TO_SET`

For example, to set IO_22 to value 50 (this is connected to RED LED on the PygmyBB4/QF):

``` none
[1] pwmctrl > enpwm 22 50
io = 22
val = 50
```

The RED LED should have turned on, with approximately half brightness.

To read current PWM config, use `getpwm IO_PADNUMBER`

For reading IO_22 for example

``` none
[1] pwmctrl > getpwm 22
io = 22
read value = 0x80000032
```

To set IO_22 to value 150:

``` none
[1] pwmctrl > enpwm 22 150
io = 22
val = 150
```

The RED LED should have got set to approximately 80% brightness.

Read IO_22 PWM:

``` none
[1] pwmctrl > getpwm 22
io = 22
read value = 0x80000096
```

To disable the PWM on IO_22:

``` none
[1] pwmctrl > dispwm 22
io = 22
```

The RED LED should have got turned off.

Read IO_22 PWM:

``` none
[1] pwmctrl > getpwm 22
io = 22
read value = 0x00000000
```

## Details

Note that the `IO_PADNUMBER` is the actual pad number of the EOSS3 and is clearly marked on the PygmyBB4 pins.

In the schematic also, we can see this pad number mentioned, for example, IO_22 can be seen connected to R_LED.

In brief, the PWM Controller is instantiated in the FPGA, and defines 32 registers to control IO_0 - IO_31.

These registers are accessed like normal 32-bit registers from M4 code using the AHB-Wishbone interconnect.

From the M4 side, it looks like memory mapped AHB registers, just like any other peripheral.

The AHB-Wishbone Bridge converts the AHB read/write transactions into Wishbone read/write transactions.

We implement the Wishbone read/write transaction decoding in the eFPGA verilog code, and interpret the register read/write into logic for PWM Control.

``` none
.
FURTHER INFORMATION TO BE ADDED
.
```

## How To

### Command Line Usage

`Note: all the commands below are run from the root of this directory.`

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
