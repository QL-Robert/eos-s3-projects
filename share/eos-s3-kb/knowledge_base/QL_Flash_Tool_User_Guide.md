---
title: "QL Flash Image Tool User Guide"
source_file: "QL Flash Tool User Guide.pdf"
pages: 17
sha256: 8b6b023e49fe2af9957e375b6a2a9d999cae8be7715a20646eaf67f92a2aafc0
---

# QL Flash Image Tool User Guide

_<u>QuickLogic Flash Tool</u> User Guide_ 

_Version: 1.0_ 

**_www.quicklogic.com_** 

**_Flash Tool_** 

**_Page 1_** 

# **Table of Contents** 

|1|QuickLogic Flash Tool ............................................................................................................................ 3|
|---|---|
|1|.1<br>Introduction .................................................................................................................................. 3|
|1|.2<br>Purpose ......................................................................................................................................... 3|
|1|.3<br>Scope ............................................................................................................................................. 3|
|1|.4<br>Prerequisites ................................................................................................................................. 3|
|1|.5<br>Target Systems .............................................................................................................................. 3|
|2|Flash Tool .............................................................................................................................................. 3|
|3|Device Connection ................................................................................................................................ 3|
|4|Flash Partition ....................................................................................................................................... 3|
|5|SREC File Transmission .......................................................................................................................... 4|
|5|.1<br>QLRAW .......................................................................................................................................... 4|
|5|.2<br>QLFILE ............................................................................................................................................ 4|
|5|.3<br>QLCMD .......................................................................................................................................... 4|
|6|Flash Command-line Interface .............................................................................................................. 5|
|6|.1<br>With Direct Command-line Arguments ........................................................................................ 5|
|6|.2<br>Command-line Option File (JSON File) .......................................................................................... 6|
|7|Configuration File .................................................................................................................................. 8|
|8|Bare-board Flashing/Device Recovery .................................................................................................. 8|
|9|Binary Upgrade ..................................................................................................................................... 9|
|10|Customize Flash Tool ........................................................................................................................ 9|
|11|Flash Status ..................................................................................................................................... 10|
|1|1.1<br>Command Status ......................................................................................................................... 10|
|12|List of Binary File Tag Names .......................................................................................................... 12|
|13|Error Messages................................................................................................................................ 13|
|14|Warnings ......................................................................................................................................... 16|
|15|Copyright and Trademark Information ........................................................................................... 16|



# **1 QuickLogic Flash Tool** 

## **1.1 Introduction** 

The QuickLogic Flash software is a standalone application to flash the EOS S3 devices. 

## **1.2 Purpose** 

The objective of this document is to provide guidelines on the flash binary transfer application and its various user interface options to flash the device. 

## **1.3 Scope** 

This document is intended for the application programmers, device test engineers and for anyone who flashes EOS S3 devices. 

It will not cover the procedures to build various binary images. One should refer the respective build tools’ user guide to build the binary image. 

## **1.4 Prerequisites** 

The following software prerequisites should be installed in the machine before using this software. 

- Microsoft® Windows® 8 (or higher) 64 bit for Windows platform. 

- Install appropriate UART cable driver supported for the OS version. 

## **1.5 Target Systems** 

All S3 devices can be flashed using this tool. The device should have required version of the Boot Loader code that has the flash support. 

# **2 Flash Tool** 

The tool is developed using python. For windows machines the tool is provided as an executable (qlflash.exe). The python source code is provided in the directory **py_src** for reference. The code is Python 3.4 compatible. All sample scripts, examples and snapshots given in the document use the flash tool executable. 

# **3 Device Connection** 

The file transfer occurs via. the serial UART medium. The tool first establishes a serial connection with the device. To initiate the connection, the tool requires the comport name (through which the device is connected) and the UART transmission speed (baud-rate). 

# **4 Flash Partition** 

The device flash is partitioned into two regions. The raw area and the file system area. The raw area consists of a fixed 1MB size dedicated for the Boot Loader (both BL0 and BL1). Other than Boot Loader, any binary file or a configuration input file should go into the file system partition. 

**_www.quicklogic.com_** 

**_Flash Tool_** 

**_Page 3_** 

# **5 SREC File Transmission** 

Once a reliable connection is established between the tool and the device, the input files can be transferred to the device. All input files are sent as SRecord files. The srecord file comes with multiple advantages like auto-error detection in the transmission, embedded target address, custom command records to perform operations in the file system, etc. Before sending a file, the tool by default converts it into the SRecord format internally. Go to the Wikipedia page to know more about srecord file format, 

<u>https://en.wikipedia.org/wiki/SREC_(file_format)</u> 

Three types of SRecord files are supported with the flash tool. 

## **5.1 QLRAW** 

This record type indicates direct flash addresses are specified in the data records. It is mainly used to flash files into the raw area. 

## **5.2 QLFILE** 

This record type is used to flash files into the file system. 

## **5.3 QLCMD** 

It is supported to provide commands to perform various operations in the file system. Given below the list of commands supported along with QLCMD SRecords. These arguments should be provided in the command-line with option _‘--commands’_ . 

The supported commands are listed in the table, Table 1. 

|**Sl. No.**|**Operation**|**Command**|**Expected**<br>**Response**|**Sample Usage**|
|---|---|---|---|---|
|1|File Delete|**DEL**<FILE_NAME>|Success/Fail<br>message|**DEL**FFE.bin|
|2|File Rename|**REN**<ORIG_NAME> <NEW_NAME>|Success/Fail<br>message|**REN**<br>BL1.bin<br>BL1.bkp|
|3|Find a File|**FIND**<FILE_NAME>|Success/Fail<br>message|**FIND**FFE.bin|
|4|File System<br>Format|**FRMT**|Success/Fail<br>message|**FRMT**|
|5|List the files<br>in file system|**LIST**|Success/Fail<br>Message|**LIST**|



**Table 1: Commands for file system operations.** 

The response for these commands for a sample usage is given in section <u>Command Status</u> 

# **6 Flash Command-line Interface** 

The tool works in the command-line with appropriate arguments. To flash a single file, one can provide the options in the command-line directly. But to flash multiple files in the single invocation, the arguments should be provided through a JSON input file. 

## **6.1 With Direct Command-line Arguments** 

To flash a file, the comport number, baud-rate and the filename are required. Some additional arguments are needed for SRecord file generation. Table 2 shows the available command-line options. 

||**Option**||
|---|---|---|
|**Short option**|**Long option**|**Description**|
|-h|--help|Display thehelp dialog.|
|-p<PORT>|--port<PORT>|Serialcomm.portnumber.|
|-b<BAUD>|--baud<BAUD>|Serialcomm.baudrate.|
|-f<FILE>|--file<FILE>|JSON command-line arg. file.|
|-i<FILE>|--input<FILE>|Input file to flash.|
|-st<TYPE>|--srec-type<TYPE>|SRecord header type. The supported SRecord types<br>are QLRAW, QLFILE & QLCMD.|
|-ft<TAG>|--file-tag<TAG>|The fixed name for the input file. This is the unique<br>identifier for the input binary file.|
|-a<ADDR>|--addr<ADDR>|Flash target address for the input file. Required when<br>–srec-type is QLRAW|
|-c<CMD>|--commands<CMD>|Commands for file system operations. Use comma<br>delimiter to provide multiple commands.|
|-nh|--no-header|Avoid binary header.|
|-cs|--chunk-size|Chunk size to split a binary file before sending it. The<br>default chunk size is 400KB.|
|-r|--reset|Reset the device after flashing the file.|
|-v|--version|Display program version number and exit.|



**Table 2: command-line options.** 

The list of binary file tag names used in the reference design can be found at section <u>List of Binary File Tag Names</u> 

Sample usage: 

**_www.quicklogic.com_** 

**_Flash Tool_** 

**_Page 5_** 

### **<u>QLRAW type:</u>** 

qlflash.exe --port=COM4 --baud=460800 --input="D:/binaries/BL_1_0.bin" --addr=0x10000 --srectype="QLRAW" --file-tag="BL1.bin" 

### **<u>QLFILE type:</u>** 

qlflash.exe --port=COM4 --baud=460800 --input="D:/binaries/FFE_1.bin"  --srec-type="QLFILE" --filetag="MCU_FFE.bin" 

### **<u>QLCMD type:</u>** 

qlflash.exe --port=COM4 --baud=460800 --srec-type="QLCMD" --commands="DEL MCU_FFE.bin, REN BL1.bin BL1.bkp" 

**NOTE:** Target address for BL0 in the flash is 0x0. Similarly, the target address for BL1 primary is fixed to 0x10000 and the target address for BL1 secondary is fixed 0x80000. 

When ‘--command’ options are specified along with QLRAW or QLFILE SRecord type, the respective file system commands are executed before flashing the binary data. 

### For example: 

qlflash.exe --port=COM4 --baud=460800 --input="D:/binaries/FFE_1.bin" --srec-type="QLFILE" -- file-tag="MCU_FFE.bin" –commands=”REN MCU_FFE.bin MCU_FFE.bkp” 

File MCU_FFE.bin will be first renamed into MCU_FFE.bkp (if already present) and then the incoming data will be flashed into a new MCU_FFE.bin file. 

**NOTE:** Both Windows style and Linux style file path can be used for specifying file names. Better enclose the file name in double quotes to avoid any character escaping with white-space or any other special character. 

## **6.2 Command-line Option File (JSON File)** 

To flash a single file, user can directly specify the arguments in the command line. But to flash multiple files in a single invocation, one should provide the options in a JSON file. JSON, or Java Script object Notation is a simple data representation format in which the data fields are entered as a list of key-value pairs. The value can be a single field or an array of values. 

|**Key**|**Value**|**Type**|
|---|---|---|
|Input|Input file|String|
|Tag|File tag name|String|
|Type|Srecord type|String|
|Addr|Start address|String|



|Commands|Comma separated commands|Array of String|
|---|---|---|
|NoHeader|No header flag|Boolean (true/false)|
|Comment|A comment statement|String|



**Table 3: Key-value pair for Config section.** 

Various key-pair values are given in the table (Table 3) with the supported type for the value field. All keys are of string type. 

A sample JSON input file is given in Figure 1. A list of four entries are given in the sample. The list contains 4 items of dictionary like syntax where each item represents various options as key-value pairs for one input file. 

**NOTE:** “Args” in the JSON file represents the list of options and it is a keyword for the flash tool to parse each option list. The JSON file should begin with the keyword “Args” enclosed in a pair of curly braces as given in Figure 1. 



<!-- Start of picture text -->
arg_filejson<br>{<br>wargs" : [<br>{<br>“Input": "D:/binaries/BL_1_0.bin",<br>"Tag": "BL1.bin",<br>type": "QLRAW",<br>"addr": "0x10000",<br>"Comment" : "Flash BL1 Primary"<br>,<br>{<br>"Input": "£OSS3_M4.bin",<br>"tag": "MCU_M4.bin",<br>type": "QLFILE",<br>"Comment" : "Flash M4 binary to file system."<br>h<br>(<br>"Type": "QLCMD",<br>"Commands": ["FIND MCU_FFE.bin"],<br>"Comment" : "Look for FFE binary in the file system."<br>h,<br>{<br>"Input": "../E0SS3_FFE.bin",<br>"Tag": "MCU_FFE.bin",<br>"Type": "QLFILE",<br>"Commands": ["REN MCU_FFE.bin MCU_FFE.bkp"],<br>"Comment" : "Backup the existing FFE binary (if found) and then flash the new file."<br>}<br>1<br>}<br><!-- End of picture text -->

**Figure 1: sample JSON file.** 

**Item 1:** Flash BL1 binary directly to address starting at 0x10000 **Item 2** :  Flash M4 binary to file system. **Item 3:** Execute the command to find **FFE** binary in the file system. 

**_www.quicklogic.com_** 

**_Flash Tool_** 

**_Page 7_** 

**Item 4** : Take a backup of the FFE binary (if present in the file system) and then flash new FFE binary to file system. 

<u>Sample usage:</u> 

qlflash.exe --port=COM4 --baud=460800 --reset --file arg_file.json 

**NOTE:** JSON file holds the options for binary_files/commands. The common options comport, baud-rate, chunk-size & reset flag are still required in the command-line. 

# **7 Configuration File** 

BL1 is responsible for loading the images from the file system.  It uses a configuration input file to decide the binary files for loading. Along with the binaries, this file should also be flashed into the file system with appropriate configuration in it. 

**NOTE:** The file tag name for the configuration file is fixed to **CONFIG.txt** . This name should be provided while flashing this file. 

The format of the configuration file used in the reference design is given below: 

<MODULE>:<M4_ENABLE_BIT>:<FPGA_ENABLE_BIT>:<FFE_ENABLE_BIT> END 

This configuration is for loading M4, FPGA & FFE in the order as indicated. The enable bit is a flag that can be either 1 or 0. The value 1 indicates that BL1 will try to load the binary, and 0 indicates not to load it. 

**NOTE:** The order of bit positions is important. First M4, then FPGA and finally FFE. 

For example: **MCU:1:0:1** 

**END** 

The bit positions indicate load M4, ignore FPGA and load FFE. 

# **8 Bare-board Flashing/Device Recovery** 

The light-weighted Boot Loader (BL0) should be in the device to begin the flash process. Using BL0 one should be able to flash BL1 that in-turn helps the users to flash other files in to the file system.  This section explains how to **flash BL0 for the first time** or **recover BL0** whenever the device crashes. 

**Step 1:** Change the device boot strap pins into JLink positions. 

**Step 2:** Connect the device to a host machine using a JLink and run the following commands in JLink commander to load the BL1 binary into SRAM directly. 



<!-- Start of picture text -->
1. loadbin BL1.bin 0x0<br>2.6<br>3.8<br>4.q<br><!-- End of picture text -->

**1.** Load BL1 binary to SRAM at location 0x0 **2.** Reset the target CPU 

**3.** Start the target CPU **4.** Quit. 

**Step 3:** Once the BL1 binary is running, we can flash BL0 to device flash using the tool qlflash.exe. 

qlflash.exe --port=COM4 --baud=460800 --input="BL0.bin" --addr=0x0 --srec-type="QLRAW" --filetag="BL0.bin" 

**Step 4:** Change the boot-strap pins to boot-mode and reset the device, it will boot from flash using BL0 binary. Now the device has BL0 binary running, one can flash BL1 and later using BL1, the file system can be flashed. 

# **9 Binary Upgrade** 

This section explains the steps to upgrade a binary (BL0, BL1, M4 App, etc.) with a newer version, when there is a valid configuration currently in the flash. 

On power reset and when BL1 starts it looks for the flash tool handshake in the initial 3 to 4 seconds. If there is no signal from the tool, BL1 tries to load the binaries as per CONFIG.txt file. When the binaries are successfully loaded, the tool won’t be able to establish the device connection. 

In order to upgrade a binary: 

**Step 1:** Reset the device. 

**Step 2:** Run the flash tool within next 3 seconds. Tool should be able to establish the device connection and flash the binaries. 

**NOTE:** The BL0 can also be upgraded using the same process. 

# **10 Customize Flash Tool** 

The flash tool is made to function independent of the boot loader customization or any binary image changes. However, users can customize the flash tool (only in the rare scenarios) if needed. The python source code provided with the SDK can be modified and later create the flash tool EXE using the software **PyInstaller** (or using a similar software). 

The python source code is compatible with Python 3.4 version. That is the minimum version one should install in the host machine to modify and run the source files. 

**_www.quicklogic.com_** 

**_Flash Tool_** 

**_Page 9_** 

PyInstaller can be installed using PIP (Python Installation Package): 

- Make sure **python 3.4** and **pip** are installed first in the host machine. 

- Add python install directory and scripts directory to windows environment variable. (For instance, ‘C:\Python34’ and C:\Python34\Scripts’) 

- Run the command ‘ **pip install pyinstaller’** in windows command-prompt. 

To create flash tool EXE from python sources: 

- Open windows command-prompt and change directory to python source file directory, **py_src** . There must be a directory named **utils** that contains 3 python scripts ( _qlsrecords.py_ , _qlcrc.py_ & _qlcommon.py_ ) and the top-level flash script file, _qlflash.py._ 

- Run the command ‘ **pyinstaller -F qlflash.py** ’. 

The option **-F** will create a one-file bundled executable for the flash tool. The executable **qlflash.exe** will be found in the temporary folder ‘ **dist** ’ created while running the command. 

# **11 Flash Status** 

The tool prints the exit status and a diagnostic message after flashing every file. For the user commands, the tool displays the status and or a response in the output window. 

## **11.1 Command Status** 

The output status for various commands are listed here. 

### **<u>List Command:</u>** 



<!-- Start of picture text -->
$ qlflash.exe --port=com4 --baud=460800 --srec-type=QLCMD --commands="LIST”<br>Trying device connection ...<br>connected to the device through BL1 using ‘coM4'...<br>sending command(s) to device.<br>LIST status :<br>Listing directory '/SPIFLASH/' contents<br>mcum4.binmcu_ffe.bin~—~—~—«[writable(writable ff il e]e] [s[s iz e=29704]e=151980]<br>.: Cdirectory] [size=1024]<br>. Cdirectory] [size=1024]<br>SUCCESS<br><!-- End of picture text -->

**Figure 2: List Command.** 

### **<u>Rename command:</u>** 

**Success:** 



<!-- Start of picture text -->
$ qlflash.exe --port=com4 --baud=460800 --srec-type=QLCMD --commands="REN MCU_M4.bin MCU_M4.bkp”<br>Trying device connection ...<br>Connected to the device through BL1 using 'coM4"...<br>sending command(s) to device.<br>REN status : SUCCESS<br><!-- End of picture text -->

**Figure 3: Rename command success.** 

### **Failure:** 



<!-- Start of picture text -->
$ qlflash.exe --port=com4 --baud=460800 --srec-type=QLCMD --commands="REN MCU_FPGA.bin MCU_FPGA.bkp"<br>Trying device connection ...<br>Connected to the device through BL1 using ‘com4'...<br>sending command(s) to device.<br>REN status : FILE NOT FOUND<br><!-- End of picture text -->

**Figure 4: Rename command failure.** 

### **<u>Delete Command:</u>** 

### **Success:** 



<!-- Start of picture text -->
$ qlflash.exe --port=com4 --baud=460800 --srec-type=QLCMD --commands="DEL MCU_M4.bin"<br>Trying device connection ...<br>Connected to the device through BL1 using 'com4'...<br>sending command(s) to device.<br>DEL status : SUCCESS<br><!-- End of picture text -->

**Figure 5: Delete command success.** 

### **Failure:** 



<!-- Start of picture text -->
$ qlflash.exe --port=com4 --baud=460800 --srec-type=QLCMD --commands="DEL MCU_FPGA.bin”<br>Trying device connection ...<br>Connected to the device through BL1 using ‘CoM4'...<br>sending command(s) to device.<br>DEL status : FILE NOT FOUND<br><!-- End of picture text -->

**Figure 6: Delete command failure.** 

### **<u>Find Command:</u>** 

### **Success:** 

**_www.quicklogic.com_** 

**_Flash Tool_** 

**_Page 11_** 



<!-- Start of picture text -->
$ qlflash.exe --port=com4 --baud=460800 --srec-type=QLCMD --commands="FIND MCU_M4.bin"<br>Trying device connection ...<br>Connected to the device through BL1 using ‘COM4'...<br>Sending command(s) to device.<br>FIND status : FILE EXISTS<br><!-- End of picture text -->

**Figure 7: Find command success.** 

### **Failure:** 



<!-- Start of picture text -->
$ qlflash.exe --port=com4 --baud=460800 --srec-type=QLCMD --commands="FIND MCU_FPGA.bin"<br>Trying device connection ...<br>Connected to the device through BL1 using ‘CoM4'...<br>sending command(s) to device.<br>FIND status : FILE NOT FOUND<br><!-- End of picture text -->

**Figure 8: Find command failure.** 

### **<u>Format Command:</u>** 

**Success:** 



<!-- Start of picture text -->
$ qlflash.exe --port=com4 --baud=460800 --srec-type=QLCMD --commands="FRMT"<br>Trying device connection ...<br>Connected to the device through BL1 using 'CoM4’...<br>Sending command(s) to device.<br>FRMT status : SUCCESS<br><!-- End of picture text -->

**Figure 9: Format command.** 

# **12 List of Binary File Tag Names** 

There is a fixed name required for each binary in the file system. This name is required at the load time to recognize a binary. 

The BL0 and BL1 should have a fixed name that can’t be modified. The tag names for the boot loader images (both BL0 & BL1) are fixed in the flash tool. See Table 4. 

|**BINARY IMAGE**|**TAG NAME**|
|---|---|
|BL0|BL0.bin|
|BL1|BL1.bin|



**Table 4: File tag names for Boot Loader binaries.** 

Other binary images and the configuration inputs may vary from design to design. Listing down the tag names used for the reference design binaries included in the **SDK** . See Table 5. 

|**BINARY IMAGE**|**TAG NAME**|
|---|---|
|M4 binary|MCU_M4.bin|
|FFE|MCU_FFE.bin|
|FABRIC|MCU_FPGA.bin|



**Table 5: File tag name for file system binaries.** 

User can customize the BL1 binary according to their design. While configuring other binaries, one should use a distinct tag name for a binary that goes into file system. 

# **13 Error Messages** 

The tool captures all possible errors during the flash process. Given below the major scenarios that may cause a failure and the corresponding error message. 



<!-- Start of picture text -->
error: the following arguments are required: -p/--port, -b/--baud<br><!-- End of picture text -->

### **Figure 10** 

This error (Figure 10) occurs when the mandatory fields are missing in the command-line. It can be either the **port number** or the **baud rate** . 



<!-- Start of picture text -->
CmdArgError: Missing SRecord type. Use -st|--srec-type option.<br><!-- End of picture text -->

### **Figure 11** 

This error (Figure 11) occurs when there is no SRecord type provided. 



<!-- Start of picture text -->
CmdArgError: Missing input file. Use -i|--input option.<br><!-- End of picture text -->

### **Figure 12** 

This error (Figure 12) occurs when the input file option is missing while trying to flash a file. File input should be provided when SRecord type is either QLRAW or QLFILE. 

**_www.quicklogic.com_** 

**_Flash Tool_** 

**_Page 13_** 



<!-- Start of picture text -->
error: can't find input file, ‘D:/binaries/BL1.bin’<br><!-- End of picture text -->

### **Figure 13** 

This error (Figure 13) occurs when the tool failed to locate the given input file. 



<!-- Start of picture text -->
CmdArgError: Missing file tag name. Use -ft|--file-tag option.<br><!-- End of picture text -->

### **Figure 14** 

This error (Figure 14) occurs when the binary file tag name is not found. 



<!-- Start of picture text -->
CmdaArgError: Missing address value for QLRAW SRecords.<br>Use -a|--addr option.<br><!-- End of picture text -->

### **Figure 15** 

This error (Figure 15) occurs when there is no address specified in the command line while trying to flash a file with QLRAW SRecord type. 



<!-- Start of picture text -->
CmdArgError: Provide a non-zero address to '-a' | '--addr’ command-line option.<br>Address 0x0 is only allowed for flashing BLO.<br><!-- End of picture text -->

### **Figure 16** 

This error (Figure 16) occurs when zero address is provided with a binary file flash other than BL0. This might be a minor mistake at user end that the zero address is given. But the tool prevents the flash process to avoid overwriting the BL0 code unintentionally. 



<!-- Start of picture text -->
CmdArgError: '0x100G0' is an invalid numeric value.<br>Provide a valid address to '-a' | '--addr' command-line option.<br><!-- End of picture text -->

### **Figure 17** 

This error (Figure 17) occurs when an invalid numeric value is given for address. 



<!-- Start of picture text -->
CmdArgError: Missing command arguments for QLCMD type.<br>Use -c|--commands option.<br><!-- End of picture text -->

### **Figure 18** 

This error (Figure 18) occurs when there is no command provided when the SRecord type is QLCMD. 



<!-- Start of picture text -->
CmdArgError: Device is running with BLO binary.<br>Use srec_type of only 'QLRAW'.<br><!-- End of picture text -->

### **Figure 19** 

This error (Figure 19) occurs when the user tries to flash a file to the file system (with QLFILE SRecord type) when the device is connected to the flash tool via. BL0 binary. BL0 binary can flash only to the raw partition using QLRAW SRecord type. 



<!-- Start of picture text -->
CmdArgError: Device is running with BLO binary. Can't send commands.<br><!-- End of picture text -->

**Figure 20** 

This error (Figure 20) occurs when the user tries to send some commands (with srec-type=QLCMD) when the device is connected to the tool using BL0 binary. 



<!-- Start of picture text -->
Expecting value: line 9 column 5 (char 194)<br>CmgArgError: commandline argument file 'cmd_input.json' read failed<br><!-- End of picture text -->

**Figure 21** 

This error (Figure 21) occurs when JSON argument file has missing value field. 



### **Figure 22** 

This error (Figure 22) occurs when an un supported key is specified in the JSON file. Here ‘Sig’ is not a valid key. 

**_www.quicklogic.com_** 

**_Flash Tool_** 

**_Page 15_** 



<!-- Start of picture text -->
error: Device is connected via. BLO binary. Provide options directly in the command-line or<br>use the JSON argument file with options to flash only a single file.<br><!-- End of picture text -->

### **Figure 23** 

When the device is connected via. BL0 binary, only one file can be flashed in a single instance of the tool. This error (Figure 23) occurs when a JSON argument file is provided with options for flashing multiple input files. It is recommended to use direct command-line options. If one wants use JSON file, make sure there is only parameters provided for flashing a single file. 

# **14 Warnings** 

This section records some of the warnings printed by the tool. Warning doesn’t stop the flash tool from functioning. However, it is an indication to the user. For instances, additional arguments are given while flashing some configurations. 



<!-- Start of picture text -->
Warning: The device has only BLO. Ignoring user commands.<br><!-- End of picture text -->

### **Figure 24** 

BL0 binary only receives QLRAW SRecord files. Any other SRecord type will be ignored. This warning (Figure 24) occurs when user provides a command along with BL1 binary flash while the device connected to the flash tool via. BL0 binary. 



<!-- Start of picture text -->
Warning: The device has only BLO. Ignoring reset flag.<br><!-- End of picture text -->

### **Figure 25** 

This warning (Figure 25) occurs when device connection established via. BL0 binary. When the user provides the reset flag along with BL1 flash process. The reset flag is passed as a command to the device and BL0 doesn’t process any command. 

- **15 Copyright and Trademark Information** 

Copyright © 2019 QuickLogic Corporation. All Rights Reserved. The information contained in this document is protected by copyright. All rights are reserved by QuickLogic Corporation. QuickLogic Corporation reserves the right to modify this document without any obligation to notify any person or entity of such revision. Copying, duplicating, selling, or otherwise distributing any part of this product without the prior written consent of an authorized representative of QuickLogic is prohibited. QuickLogic, ArcticLink, and the ArcticLink design are registered trademarks, SenseMe, QuickWorks and the QuickLogic logo are trademarks of QuickLogic. Other trademarks are the property of their respective companies. 

**_www.quicklogic.com_** 

**_Flash Tool_** 

**_Page 17_** 

