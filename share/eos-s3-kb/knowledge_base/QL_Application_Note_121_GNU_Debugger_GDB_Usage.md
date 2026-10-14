---
title: "GNU Debugger (GDB) Usage"
source_file: "QL Application Note 121 GNU Debugger (GDB) Usage.pdf"
pages: 11
sha256: 089cc91e1c1fda224064076e0234f137a5089a2a178476132b4126a8157803ae
---

# GNU Debugger (GDB) Usage

**GNU Debugger (GDB) Usage** 

**• • • • • • QuickLogic**<sup>**®**</sup> **Application Note 121** 

# **Introduction** 

The Flexible Fusion Engine Algorithm Tool (FFEAT) Eclipse plug-in generates output files in the standard ELF format with the extension .elf. It also generates an .alg file for every .c source file in the directory where the source file is located. These files can be debugged using the following customized debug tools: 

- ffe-gdbserver: The GDB Server connects to the target board using JLINKARM.dll by monitoring a port for a GDB Client. When the GDB Server receives requests from the GDB Client it performs necessary actions (such as read from the device or write to the target device) and forwards the response to the GDB Client. 

- ffe-quicklogic-elf-gdb: The GDB Client connects to the ffe-gdbserver. It accepts commands from the user on its command prompt and sends it to the GDB Server. The responses from the GDB Server are read and displayed on its command prompt for the user. 

# **Usage** 

Invoke the tools using two Microsoft<sup>®</sup> Windows<sup>®</sup> command prompts. The GDB Server and GDB Client emit messages when invoked and also while communicating with each other. 

**NOTE:** Start the GDB Server before starting the GDB Client. 

## **Invoking the GDB Server** 

To start GDB Server type: 

cmd-prompt1> ffe-gdbserver.exe localhost:4444 

After running the GDB Server the following screen is displayed: 



<!-- Start of picture text -->
BB CAWindows\system32\cmd.exe -ffe-gdbserver.exe localhostada4 een x<br>le. \aL1\Fe_quicklogic_e1f_gdb\bin>FFe-gdbserver exe localhost 4444<br>fnandierep() invoked<br><!-- End of picture text -->

## **Invoking the GDB Client** 

To start GDB Client type: 

cmd-prompt2> ffe-quicklogic-elf-gdb.exe 

••• ••• 

**<mark>PRELIMINARY</mark>** 

© 2015 QuickLogic Corporation 

<u>www.quicklogic.com</u> **1** 

**_GNU Debugger (GDB) Usage Rev. B_** 

After running the GDB Client the following screen is displayed: 



<!-- Start of picture text -->
BH C\Windows\sstem32\cmd.exe-He-quicklogice- gd exe = et<br>ke: \aL1\FFe_quicklogic_e1f_gdb\bin>FFe-quicklogic-e1f-gdb.exe<br>anv gdb (G08) 7.9<br>Copyright (C) 2015 Free Softuare Foundation, Ine<br>ILicense GPLu3+: GNU GPL version 3 or later chttp://gnu.org/Licenses/gp1.htal<br>Hthis is free software: you are free to change and redistribute it<br>Hihere is NO WARRANTY, to the extent permitted by law. Type “show copying<br>Jand “show warranty” for detaile<br>HThis GDB was configured ac "--host=iG86-pe-mingu32 ~-target=Ffe-quicklogic-elf”<br>Hype “show configuration” for configuration details<br>For bug reporting instructions, please see<br>kinttp: //aww. gnu.org/softuare/gdb/bugs,<br>Findhttp: the//aun.GOB gnu..org/soFmanual and tware/gdbother docunentation/docunentationresources online at<br>For help. type “help<br>Hype “apropos word” to search for connands related to “word<br>gab)<br><!-- End of picture text -->

At the GDB Client prompt (gdb), the user must input the intended command. 

# **Load an ELF Program** 

To load an .ELF file on the target device: 

**1.** Start the GDB Server using command prompt1. 

cmd-prompt1> ffe-gdbserver.exe localhost:4444 

**2.** Start the GDB Client using command prompt2. 

cmd-prompt2> ffe-quicklogic-elf-gdb.exe 

**3.** At the **(gdb)** prompt type “file” followed by a space followed by the path to the .ELF file. E.g., if the file is located in the current directory, one could type a period, forward-slash and the .ELF filename to be debugged. For example, ./Template1.ELF is the filename. An absolute path or relative path to the .ELF file can also be specified as an argument to file command. 

file ./Template1.ELF 

If the filename is a valid .ELF file the following message appears. Otherwise, an error message is shown. 

Reading symbols from ./Template1.ELF...done 

If the .ELF file does not have any debugging symbols, the following error message will appear, in which case, it will not be feasible to perform symbolic debugging on the executable file: 

Reading symbols from ./Template1.ELF...(no debugging symbols found)...done 

Under such situations, it is possible to execute the .ELF file on the target correctly and examine data memory by their addresses. However, it is not possible to read the values of variables by their names. 

**2** <u>www.quicklogic.com</u> •• •••• 

© 2015 QuickLogic Corporation 

**<mark>PRELIMINARY</mark>** 

**_GNU Debugger (GDB) Usage Rev. B_** 

**4.** Connect to the GDB Server, at the **(gdb)** prompt type: 

target ffe localhost:4444 

The following message appears. 

Remote debugging ffe using localhost:4444 

**5.** Load the .elf file on the target device, at the **(gdb)** prompt type: 

load 

The following message appears. 

Downloading finished. [Starting Template1.ELF at 0x0] Transfer rate: 7 KB/sec. 

After the program is loaded on the target device the following screen is displayed. 



<!-- Start of picture text -->
EB C\Windows\system32\cmd.exe- fe-quicklogicel-gdb.exe bal<br>IE: \OL1\FFe_quicklogic_elf_gdb\bin>FFe-quicklogic-elf-gdb. exe<br>Icnu gdb (GOB) 7.9<br>copyright (C) 2015 Free Softuare Foundation, Inc<br>lLicense GPLU3+: GNU GPL version 3 or later <http://gnu.org/licenses/gp1 html<br>This is free software: you are free to change and redistribute it<br>There is NO WARRANTY, to the extent permitted by law. Type “show copying’<br>jand “shou warranty" for details<br>This GDB was configured as “--host=i686-pe-mingu32 ~-target=Ffe-quicklogic-elf<br>[Type “chow configuration” for configuration details<br>FindForcht tp:bugthe//umis.gnu.org/softuare/gdb/bugs/>reportingGDB manualinstructions,and other documentationplease see resources online at<br>http: //uuw. gnu. org/softuare/gdb/documentation<br>For help, type “help’<br>IType “apropos word” to search for commands related to “word<br>(gdb) File ./Templatel .ELF<br>Reading symbols from ./Templatel .ELF...uarning: Loadable section ".sensor.menory" outside of ELF segments<br>(no debugging symbols found)... .done<br>(gdb) target FFe localhost 4444<br>Remote debugging ffe using localhost :4444<br>(gdb) Load<br>Dounloading Finished.<br>[Starting E:\\OLI\\Ffe_quicklogic_elf_gdb\\bin\\Template! ELF at 0x0]<br>Transfer rate: 8 KB/sec<br>gdb)<br><!-- End of picture text -->

# **Run a Program without Setting Breakpoints** 

This section describes how to run a program only when the breakpoints are not set. When breakpoints are set, see **Run a Program by Setting Breakpoints** on page 5 for a separate set of commands. 

## **Run a Program in Continuous Mode** 

Requisite State: The program must be loaded, see **Load an ELF Program** on page 2. 

To run a program in continuous mode, at the **(gdb)** prompt type: 

ffe_run_continuous 

> © 2015 QuickLogic Corporation **<mark>PRELIMINARY</mark>** 

<u>www.quicklogic.com</u> **3** • • • ••• 

**_GNU Debugger (GDB) Usage Rev. B_** 

The following screen is displayed. 



<!-- Start of picture text -->
BH C\Windows\sstem32\cmd.exe-He-quickogic-e gd exe ror x]<br>fe: \aL1\FFe_quicklogic_e1f_gdb\bin>FFe-quicklogic-e1f-gdb.exe<br>anv gdb (G08) 7.9<br>Copyright (C) 2015 Free Softuare Foundation, Ine<br>lLicense GPLu3+: GNU GPL version 3 or later <http://gnu.org/Licenses/gp1.html><br>Hthis is free software: you are free to change and redistribute it<br>Hihere is NO WARRANTY, to the extent permitted by law. Type “show copying<br>Jand “show warranty for detaile<br>HThis GDB was configured ac "--host=iG86-pe-mingu32 --target=Ffe-quicklogic-elf”<br>Hype “show configuration” for configuration details<br>ror{cntFindtp:bugthe//wuu.gnu.org/soFtware/gdb/buge/reportingGOB manualinstructions,and other docurentationplease see resources online at<br>http: //uuu. gnu..org/s0F tware/gdb /docunentat ion<br>For help. type “help<br>Hype “apropos word” to search for commands related to “word”<br>(gab) File ./Templatet ELF<br>Reading synbols from ./Templatel .ELF...warning: Loadable section “.sensor memory" outside of ELF segments<br>Remote(no(gab)debuggingtargetdebuggingFFesymbolsFfelocalhostusingFound)...:444localhostdone 4444<br>(gab) 108d<br>Dountoading Finished<br>[starting E:\\GLI\\FFe_quicklogic_elf_gdb\\bin\\Tenplate! .ELF at 0x0]<br>Hrancfer rate: 8 KB/sec<br>(gab). FFe_run_continuous<br>Running the program continuously<br>oad)<br><!-- End of picture text -->

## **Stop a Program Running in Continuous Mode** 

To stop a program in continuous mode, at the **(gdb)** prompt type: 

ffe_stop_run_continuous 

The following screen is displayed. 



<!-- Start of picture text -->
BHR C\Windows\system32\cmd.exe-He-quckogic-e- exe or x]<br>ke. \aL1\FFe_quicklogic_e1f_gdb\bin>FFe-quicklogic-elF-gdb.exe<br>anv gdb (G08) 7.9<br>Copyright (C) 2015 Free Softuare Foundation, Inc<br>license GPLu3+: GNU GPL version 3 or later <http://gnu.org/licenses/gp1 html<br>Hihis is free software: you are free to change and redistribute it<br>Hthere is NO WARRANTY, to the extent permitted by law. Type "show copying’<br>Jand “show warranty” for detaile<br>This GDB was configured ac "--host=i686-pe-mingu32 --target=FFe-quicklogic-elf<br>Hype “show configuration” for configuration details<br>{chtFindror tp:bugthe//uuu.gnu.org/soFtware/gdb/bugereportingGOB manualinstructions,and other docunentationplease see resources online at<br>http: //uuu. gnu..org/sof tware/gdb /documentation/<br>For help. type “help<br>Hype “apropos word” to search for connands related to “word<br>(gab) File ./Templatet .ELF<br>Reading symbols from ./Templatel .ELF...warning: Loadable section “.sensor memory outside of ELF segaents<br>Remote(no(gab)debuggingtargetdebuggingFesymbolsFfelocalhostusingFound)...:44Hlocalhostdone 4444<br>(gdb) 108d<br>bounioading Finished<br>[Starting E:\\GLI\\FFe_quicklogic_elf_gdb\\bin\\Template! ELF at 6x0]<br>Hransfer rate: 8 KB/sec<br>(gab). FFe_run_continuous<br>Running the program continuously<br>(gab) FFe_stop_run_continuous<br>stopped the program<br>(oa)<br><!-- End of picture text -->

**4** <u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2015 QuickLogic Corporation 

**_GNU Debugger (GDB) Usage Rev. B_** 

## **Run a Program Once** 

Requisite State: The program must be loaded, see **Load an ELF Program** on page 2. 

To run a program once, at the **(gdb)** prompt type: 

ffe_run_once 

# **Run a Program by Setting Breakpoints** 

**NOTE:** A minimum of two breakpoints must be set, so that these breakpoints are hit continuously. Also, a minimum of two breakpoints must be set if the breakpoints are located inside a loop. 

Since a program can be run in either continuous mode or once, two commands are provided to set the program execution mode. 

## **Set the Program to Continuous Execution Mode** 

To set a program in continuous execution mode, at the **(gdb)** prompt type: 

ffe_set_exec_run_continuous 

## **Set the Program to Single Execution Mode** 

To set a program in single execution mode, at the **(gdb)** prompt type: 

ffe_set_exec_run_once 

**NOTE:** The default execution mode is continuous. 

## **Set Breakpoints** 

**NOTE:** A maximum of four hardware breakpoints can be set. 

To set a breakpoint, at the **(gdb)** prompt type: 

#### break foobar 

where, foobar is a function in the project and has been emitted as a symbol in the ELF file. One can know the symbols in the ELF file using the following command: 

ffe-quicklogic-elf-readelf -s ./Template1.ELF 

## **Get Information About Breakpoints** 

To get information about the breakpoints, at the **(gdb)** prompt type: 

info breakpoints 

• • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2015 QuickLogic Corporation 

<u>www.quicklogic.com</u> **5** 

**_GNU Debugger (GDB) Usage Rev. B_** 

## **Run the Program After Setting Breakpoints** 

#### continue 

The program will be run and will hit a breakpoint. 

After setting the breakpoints, the following screen is displayed. 



<!-- Start of picture text -->
HH C\Windows\system32\cmedexe-fe-quiclogic-elf-gdb exe =o |<br>(gdb) load<br>Dounioading finished<br>[Starting E:\\QLI\\FFe_quicklogic_elf_gdb\\bin\\Template! ELF at 0x0]<br>Hransfer rate: 8 KB/sec<br>(gdb) #Fe_set_exec_run_once<br>(gdb) hbreak dbg_uipshTemplate.clb24<br>Hardware assisted breakpoint 1 at 6x90<br>(gdb) hbreak dbg_ulpshTemplate.clb29<br>liardware assisted breakpoint 2 at 0x96<br>(gdb)<br>Continuing<br>Inunning the program once<br>lereakpoint hit at ox0<br>No ctack<br>(gab) ¢<br>continuing<br>breakpoint hit at 0x90<br>No stack<br>(gdb) ©<br>continuing<br>[Inferior 1 (process 42000) exited normally]<br>(gdb) ¢<br>continuing<br>Inunning the program once<br>breakpoint hit at 0x96<br>No stack<br>(gdb) ©<br>continuing<br>lereakpoint hit at 0x90<br>No stack<br>(gdb) ©<br><!-- End of picture text -->

### **Use-Case 1** 

The user has set an execution as run_continuous with a few breakpoints in the code. Then, the user issues a continue command. Now, the program will break at a location where a breakpoint is set by the user. The user verifies the values of a few variables and deletes all breakpoints. 

To resume execution after deleting all breakpoints, at the **(gdb)** prompt the user types: 

p *0x4004A154=1 

This command will continue the execution from the breakpoint. 

To stop the execution, at the **(gdb)** prompt the user types: 

ffe_stop_run_continuous 

## **Delete a Breakpoint** 

To delete a breakpoint, at the **(gdb)** prompt type: 

delete breakpoint _<breakpoint_number>_ 

where, _<breakpoint_number>_ is the number listed by the info breakpoints command. 

**6** <u>www.quicklogic.com</u> **<mark>PRELIMINARY</mark>** •• •••• 

© 2015 QuickLogic Corporation 

**_GNU Debugger (GDB) Usage Rev. B_** 

## **Delete All Breakpoints** 

To delete all breakpoints, at the **(gdb)** prompt type: 

#### delete breakpoints 

A confirmation from the user will be asked to delete all breakpoints. Type y to delete all breakpoints already set. 

# **Read/Write a Value from/to Memory** 

## **Set the Output-Radix** 

To set the output-radix to 16 to see the values in hex format, at the **(gdb)** prompt type: 

set output-radix 16 

## **Read a Value from Memory** 

To read a value from memory, at the **(gdb)** prompt type: 

#### p _<variable_name>_ 

Where, p refers to the print command and _variable_name_ refers to the variable in the .alg file. Example: 

#### p a 

Where, a refers to the variable name in the .alg file. 

The values printed are in the integer format for all int, long, short and char data types. For the ones with float data type, the value is printed as a conversion of the fixed point value to a floating point value. 

## **Read a Value Using an Address from Memory** 

To read a value using an address from memory, at the **(gdb)** prompt type: 

#### p * _<address>_ 

Where, _address_ refers to a valid address either in the Control Memory or Data Memory. Example: 

#### p *0x40040000 

When this method is used to read the data contents, the result is always printed in Hex format. If the data type is int, long, short, char or float, this value will be the Q15.16 representation of the actual decimal value. If the location is a configurable register, then the value is the raw register contents. 

<u>www.quicklogic.com</u> **7** • • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2015 QuickLogic Corporation 

**_GNU Debugger (GDB) Usage Rev. B_** 

## **Write a Value to Memory** 

To write a value to memory, at the **(gdb)** prompt type: 

p _<variable_name>_ =value 

Where, _variable_name_ refers to a variable in the .alg file. Example: 

p a=0x23 

The value should be given in the normal decimal, octal or hexadecimal format, as the case may be. GDB will internally convert this value to the Q15.16 format that is understood by the underlying machine. Never should the user try to convert the value to Q15.16 before entering it on the command line. 

## **Write a Value Using an Address to Memory** 

To write a value using an address to memory, at the **(gdb)** prompt type: 

p * _<address>_ = _<value>_ 

Where, _address_ refers to a valid address either in the Control Memory or Data Memory. Example: 

p *0x40040000=0x12345678 

**NOTE:** The user must provide a valid memory address of the target for the above commands. GDB does not verify the address given by the user. 

If the value being written is the contents of a register, then the hexadecimal value of the register should be given as it is. However, if the value being set is a variable of type int, long, short, char or float, then the value must be converted to equivalent Q15.16 format before assigning the value on the command line. 

**8** <u>www.quicklogic.com</u> •• •••• 

© 2015 QuickLogic Corporation 

**<mark>PRELIMINARY</mark>** 

**_GNU Debugger (GDB) Usage Rev. B_** 

# **Custom Commands** 

The custom commands are prefixed with ffe_. 

- ffe_print_cpuregs_values: Prints the PC and IR values. 

- ffe_print_datamem: Prints the values of data memory 



<!-- Start of picture text -->
a ffe-quicklogic-elf-gdb.exe - Ea<br>roe -<br>gab) FFc_print_datanen<br>3: oxtoaqo1a axdaneaaaa 6 ao00u8 main. Loopcounter<br>f! Qxaaasoaos ox00070006 $:aaa092 "SECO_-OFPSET<br>2: 949040000 0001000? Paaates SEGO_OFFSET_ENABLE<br>3: Gxduedauac 00030008 31000008 geaun<br>4:3:@: oxdood0014QxdoasooisBx49040004 00010000gx00020008300000009 ipeeré.00013?le0000 Hiy» srGo_OFFSET_suAP .<br>r ><br><!-- End of picture text -->

To get a list of custom commands, at the **(gdb)** prompt type **ffe_** and press TAB twice. 

The following is a sample screenshot of custom commands. 



<!-- Start of picture text -->
IS C.\Windows\system32\cmd.exe - E\QuickLogic\AL4S3_Emulation\Tools\FFEAT\ffe-quicklogic-elf-gdb.exe<br>gdb) Fre<br>Po_printcpursgevsluco  ffe_print_datasou #fe_run_eontinuoue #Fe_run_once<br>gab) hetp #F_print cpurege_vaiuee<br>(gdb) help #Fe.run.continuous<br>Fun the progran continuouoly<br>(gdb) heip #Fe_run-once<br>nun the program once<br>(gdb) help #Fe_setexec_run_continuous<br>set. the program execution to run continuous<br>(gdb) help ffe_set_exec_run_once<br>Set. the program execution to run once<br>Cadb)<br><!-- End of picture text -->

The following are custom commands: 

- ffe_continue_from_breakpoint Continue from a breakpoint. 

- ffe_run_once Run the program only once. 

- • ffe_run_continuous Run the program continuously. 

- ffe_stop_run_continuous Stop the program that is running continuously. 

- ffe_set_exec_run_continuous Set the program execution mode to run continuously. 

• ffe_set_exec_run_once Set the program execution mode to run the program only once. • ffe_force_stop Stop the program execution by force. 

- ffe_hard_reset Perform a hard reset on the FFE. 

<u>www.quicklogic.com</u> **9** • • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2015 QuickLogic Corporation 

**_GNU Debugger (GDB) Usage Rev. B_** 

# **Quit the Debugging Session** 

To quit the debugging session, at the ( **gdb)** prompt type: 

q 

This also closes the GDB Server. 

# **Contact Information** 

Phone: (408) 990-4000 (US) +(44) 1932-21-3160 (Europe) +(886) 26-603-8948 (Taiwan) +(86) 139-0517-5302 (China) +(81) 3-5875-0547 (Japan) +(82) 31-601-4225 (Korea) 

E-mail: <u>info@quicklogic.com</u> 

Sales: <u>America-sales@quicklogic.com Europe-sales@quicklogic.com Asia-sales@quicklogic.com Japan-sales@quicklogic.com Korea-sales@quicklogic.com</u> 

Support: <u>www.quicklogic.com/support</u> Internet: <u>www.quicklogic.com</u> 

# **Revision History** 

|**Revision**|**Date**|**Originator and Comments**|
|---|---|---|
|A|July2015|Initial release - Paul Karazuba|
|BA|October 2015|Syama Pingali and Kathleen Bylsma<br>Major changes/updates.|



# **Notice of Disclaimer** 

QuickLogic is providing this design, product or intellectual property "as is." By providing the design, product or intellectual property as one possible implementation of your desired system-level feature, application, or standard, QuickLogic makes no representation that this implementation is free from any claims of infringement and any implied warranties of merchantability or fitness for a particular purpose. You are responsible for obtaining any rights you may require for your system implementation. QuickLogic shall not be liable for any damages arising out of or in connection with the use of the design, product or intellectual property including liability for lost profit, business interruption, or any other damages whatsoever. QuickLogic products are not designed for use in life-support equipment or applications that would cause a life-threatening situation if any such products failed. Do not use QuickLogic products in these types of equipment or applications. 

**10** <u>www.quicklogic.com</u> •• •••• 

© 2015 QuickLogic Corporation 

**<mark>PRELIMINARY</mark>** 

**_GNU Debugger (GDB) Usage Rev. B_** 

QuickLogic does not assume any liability for errors which may appear in this document. However, QuickLogic attempts to notify customers of such errors. QuickLogic retains the right to make changes to either the documentation, specification, or product without notice. Verify with QuickLogic that you have the latest specifications before finalizing a product design. 

# **Copyright and Trademark Information** 

Copyright © 2015 QuickLogic Corporation. All Rights Reserved. 

The information contained in this document is protected by copyright. All rights are reserved by QuickLogic Corporation. QuickLogic Corporation reserves the right to modify this document without any obligation to notify any person or entity of such revision. Copying, duplicating, selling, or otherwise distributing any part of this product without the prior written consent of an authorized representative of QuickLogic is prohibited. 

QuickLogic and ArcticLink are registered trademarks, and the QuickLogic logo is a trademark of QuickLogic. Other trademarks are the property of their respective companies. 

<u>www.quicklogic.com</u> **11** • • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2015 QuickLogic Corporation 

