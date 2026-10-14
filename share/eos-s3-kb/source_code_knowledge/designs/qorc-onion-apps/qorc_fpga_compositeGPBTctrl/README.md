---
title: "QORC FPGA Composite Controller Application"
source_file: "github.com/coolbreeze413/qorc-onion-apps/qorc_fpga_compositeGPBTctrl/README.rst"
source_commit: a960ca3f450fafde9da07547b35efe8e1caa2574
type: "readme"
topic: "eFPGA designs"
added: 2026-10-09
---

# QORC FPGA Composite Controller Application

## Intro

This combines multiple FPGA Designs into one, and makes all of them accessible over the AHB2WB interface - exposing the addresses as simple AHB addresses that the M4 can write/read. This also demonstrates the usage of the Interrupt mechanism from the FPGA to the M4 (with a simple timer based design) and how the M4 code can be setup to configure and handle the interrupts.

The following are individual projects, which describe in detail each of the FPGA designs used, and can be referred to:

1.  Simple GPIO CONTROLLER Example : control all EOSS3 IOs using FPGA, from M4

    [qorc_fpga_gpioctrl](../qorc_fpga_gpioctrl/README.md)

2.  Simple PWM CONTROLLER Example : built on top of the PWM example, use from M4

    [qorc_fpga_pwmctrl](../qorc_fpga_pwmctrl/README.md)

3.  Simple BREATHE CONTROLLER Example : built on top of the BREATHE example, use from M4

    [qorc_fpga_breathectrl](../qorc_fpga_breathectrl/README.md)

4.  Simple TIMER CONTROLLER Example : use TIMER on FPGA, use from M4, provides Interrupt on Timer Expiry from FPGA to M4, illustrates both Wishbone access and Interrupt Path

    [qorc_fpga_timerctrl](../qorc_fpga_timerctrl/README.md)

## Usage

Once the board is flashed, and reset, you should see a pattern of:

1.  Triple-Magenta-Blink controlled using the GPIO Controller FPGA Module
2.  Triple-Magenta-PWMBlink controlled using the PWM Controller FPGA Module
3.  Triple-Magenta-Breathe controlled using the BREATHE Controller FPGA Module

indicating the code has loaded and started execution (FPGA and M4).

### Main Menu

This is followed by a banner like the below on the serial terminal:

``` none
##########################
ONION FPGA Composite Controller Experiment
SW Version: qorc-onion-apps/qorc_fpga_compositeGPBTctrl
Mar  9 2021 22:43:55
##########################



Hello GPIO/PWM/BREATHE/TIMER CONTROLLER!

FPGA Device ID: 0x0000c00f
[0] >
```

Each of the Module submenus are available, using help displays:

``` none
[0] > help
help-path: (top)
gpioctrl       - FPGA GPIO Controller
pwmctrl        - FPGA PWM Controller
breathectrl    - FPGA BREATHE Controller
timerctrl      - FPGA TIMER Controller
exit           - exit/leave menu
help           - show help
?              - show help
help-end:
```

### GPIOCTRL SubMenu

Enter the GPIO Controller submenu using `gpioctrl` and then type `help` in the gpioctrl submenu for commands.

``` none
[0] > gpioctrl
[1] gpioctrl > help
help-path: gpioctrl
setout         - setout IO_X VAL
setin          - setin IO_X
getval         - getval IO_X (must be setin first)
exit           - exit/leave menu
help           - show help
?              - show help
help-end:
```

To set a GPIO as output with specific value, use `setout IO_PADNUMBER VALUE_TO_SET`

For example, to set IO_22 to value 1 (this is connected to RED LED on the PygmyBB4/QF):

``` none
[1] gpioctrl > setout 22 1
io = 22
val = 1
```

The RED LED should have turned on.

To set IO_22 to value 0:

``` none
[1] gpioctrl > setout 22 0
io = 22
val = 0
```

The RED LED should have turned off.

### PWMCTRL SubMenu

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

To set a GPIO as output with specific value, use `enpwm IO_PADNUMBER VALUE_TO_SET(0-255)`

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

### BREATHECTRL SubMenu

Enter the Breathe Controller submenu using `breathectrl` and then type `help` in the breathectrl submenu for commands.

``` none
[0] > breathectrl
[1] breathectrl > help
help-path: breathectrl
enbreathe      - enbreathe IO_X period_msec
disbreathe     - disbreathe IO_X
getbreathe     - getbreathe IO_X
exit           - exit/leave menu
help           - show help
?              - show help
help-end:
```

To set a GPIO as breathe output with specific period, use `enbreathe IO_PADNUMBER PERIOD_MSEC`

For example, set IO_22 to 2 sec breathe(1 sec inhale, 1 sec exhale):

``` none
[1] breathectrl > enbreathe 22 2000
io = 22
val = 2000
```

The RED LED should have be breathing with approx 1 sec inhale, and 1 sec exhale period

To read current breathe config, use `getbreathe IO_PADNUMBER`

For reading IO_22 for example:

``` none
[1] breathectrl > getbreathe 22
io = 22
breathe_period = 999 [0x000003e7] msec
```

To disable the breathing on IO_22:

``` none
[1] breathectrl > disbreathe 22
io = 22
```

The RED LED should have got turned off.

Read IO_22 breathe config:

``` none
[1] breathectrl > getbreathe 22
io = 22
breathe is disabled
```

### TIMERCTRL SubMenu

Enter the Timer Controller submenu using `timerctrl` and then type `help` in the timerctrl submenu for commands.

``` none
[0] > timerctrl
[1] timerctrl > help
help-path: timerctrl
entimer        - entimer ID period_msec
distimer       - distimer ID
gettimer       - gettimer ID
exit           - exit/leave menu
help           - show help
?              - show help
help-end:
```

To set a Timer with specific period, use `entimer TIMER_ID TIMER_PERIOD_MSEC`

Currently, only one Timer is instantiated, and its ID is 0, so `TIMER_ID = 0`

For example, set TIMER0 to period 1 second:

``` none
[1] timerctrl > entimer 0 1000
id = 22
val = 1000
```

You should see the prints on the serial terminal shortly after:

``` none
timer0 enabled

timer0 ISR

timer0 disabled
```

These are output by a small monitor task - to which we send messages from the HAL enable/disable functions, and from the FPGA Interrupt Handler.

As a "debug" output, the TIMER0 also triggers the BLUE LED, and it should be visible for a very small amount of time, when the timer expires - we disable the timer as soon as the Interrupt Handler is hit, which disables the TIMER Interrupt, as well as the debug output.

To disable TIMER0 manually:

``` none
[1] timerctrl > distimer 0
io = 0
[1] timerctrl > 
timer0 disabled
```

# Details

The code is structured (with only interesting files shown) as:

``` none
.
├── binaries                                      ==> (prebuilt) BINARIES
│   ├── AL4S3B_FPGA_Top.bin                       ==> appfpga BINARY
│   ├── flash_binaries.txt
│   ├── qorc_fpga_compositeGPBTctrl.bin           ==> m4app BINARY
│   ├── qorc_fpga_compositeGPBTctrl.elf
│   └── qorc_fpga_compositeGPBTctrl.map
├── fpga
│   ├── inc                                       ==> FPGA "HAL" sources
│   │   ├── hal_fpga_onion.h
│   │   ├── hal_fpga_onion_gpioctrl.h
│   │   ├── hal_fpga_onion_pwmctrl.h
│   │   ├── hal_fpga_onion_breathectrl.h
│   │   └── hal_fpga_onion_timerctrl.h
│   ├── rtl                                       ==> FPGA RTL Verilog Code
│   │   ├── AL4S3B_FPGA_IP.v
│   │   ├── AL4S3B_FPGA_ONION_BREATHECTRL.v
│   │   ├── AL4S3B_FPGA_ONION_GPIOCTRL.v
│   │   ├── AL4S3B_FPGA_ONION_PWMCTRL.v
│   │   ├── AL4S3B_FPGA_ONION_TIMERCTRL.v
│   │   ├── AL4S3B_FPGA_QL_Reserved.v
│   │   ├── AL4S3B_FPGA_Top.v
│   │   ├── ONION_BREATHE.v
│   │   ├── ONION_PWM.v
│   │   ├── ONION_TIMER.v
│   │   └── quickfeather.pcf
│   └── src                                       ==> FPGA "HAL" sources
│       ├── hal_fpga_onion_breathectrl.c
│       ├── hal_fpga_onion.c
│       ├── hal_fpga_onion_gpioctrl.c
│       ├── hal_fpga_onion_pwmctrl.c
│       └── hal_fpga_onion_timerctrl.c
├── GCC_Project                                   ==> Makefile Build Infra
│   ├── config-GCC.mk
│   ├── config.mk
│   ├── Makefile
│   ├── makefiles
│   ├── output
│   └── quickfeather.ld
├── inc
│   ├── minimal_task.h                            ==> "monitor" task header for TIMER0
│   └── s3x_pwrcfg.h                              ==> EOSS3 power/clock configuration header
├── README.rst
└── src
    ├── exceptions.c                              ==> Interrupt Handlers
    ├── main.c                                    ==> m4app entry point
    ├── main_dbg_cli_menu.c                       ==> m4app command line interface
    ├── minimal_task.c                            ==> "monitor" task source for TIMER0
    ├── pincfg_table.c                            ==> EOSS3 m4app pinmuxing
    └── s3x_pwrcfg.c                              ==> EOSS3 power/clock configuration source
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
