---
title: "UART IP for EOS 3B"
source_file: "qorc-sdk/s3-gateware/projects/S3_FPGA_2xUART/docs/FPGA_UART_2x.pdf"
pages: 7
sha256: 7f3e187aa0a80cee377e9a3ca27d1b33b68c53e997389ceedfd9e1e09daa61b1
---

# UART IP for EOS 3B

# UART FPGA IP 

_Revision: 1.01 Date: 21 Sep 2020_ 

## _QuickLogic Corporation_ 

UART IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 1_** 

### **1 Requirement:** 

### **2 Pinout:** 

|**Sl.**<br>**No.**|**Signal Name**|**PAD Number**|**Direction**|**Description**|
|---|---|---|---|---|
|**UART**|||||
|4|UART_TX||Output||
|5|UART_RX||Input||



### **3 FPGA Interrupts:** 

|**Sl. No.**|**FPGA Interrupts to M4**|**Interrupt Description**|
|---|---|---|
|1|FB_INTERRUPT_0|Reserved|
|2|FB_INTERRUPT_1|Reserved|
|3|FB_INTERRUPT_2|UART 0 INTR|
|4|FB_INTERRUPT_3|UART 1 INTR|



UART IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 3_** 

### **4 Address Map Specification** 

#### **4.1 Memory Map** 

The EOS 3B system maps the FPGA IP into the address range of 0x40020000 to 0x4003FFFF. This address range provides 128K bytes of address range for FPGA based IP. The following tables further define the registers within this range. 

**Table 1-1: FPGA IP Register Space** 

|Register|Block|Space Allocated|Remarks|
|---|---|---|---|
|0x40020000 –<br>0x400200FF|FPGA IP Registers|256 bytes||
|0x40020100 –<br>0x40020FFF|Reserved|0x0||
|0x40021000 –<br>0x400217FF|UART 0|512 Words||
|0x40022000 –<br>0x400227FF|UART 1|512 Words||
|0x40022800 –<br>0x4003FFFF|Reserved|0x0||



#### **4.2 Register Address Table** 

The following sections will outline the expected allocation of registers and describe their operations. 

##### **4.2.1 FPGA Registers Address Table** 

Table 1-2 shows the expected allocation of FPGA Registers address space. 

**Table 1-2: FPGA IP Register Table** 

|Register|Block|Reset Value|Remarks|
|---|---|---|---|
|0x40020000|IP Device ID|0xABCD0002|Read only|
|0x40020004|IP Revision number|0x0100|Read only<br>Version|
|0x40020008 –<br>0x400200FF|Not Used|0x0||



**4.2.2 UART 0 and UART 1 Address Map** 

UART 0 has a base address that starts at offset 0x1000 from the FPGA’s base address (0x40020000 + 0x1000). UART 1 has a base address that starts at offset 0x2000 from the FPGA’s base address (0x40020000 + 0x2000). The register map for each UART is described in a separate document, and can be found along with the RTL source code for the UART (currently in QuickLogic’s s3-gateware repository on github, under ip_modules). 

UART IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 5_** 

### **5 Revision History** 

|**Date**|**Revision**|**Author**|**Description**|
|---|---|---|---|
|17 Sep 2020|1.00|Randy O|Initial Release|
|21 Sep 2020|1.01|Randy O|Removed the UART register map, since it’s now<br>described in a separate document. Updated<br>QuickLogic’s address.|



### **6 Copyright and Trademark Information** 

_All trademarks and / or trade names are property of their respective owners._ 

_The information in this specification has been carefully reviewed for technical accuracy. However, QuickLogic does not take the responsibility for the accuracy of the included information. Quicklogic will not be held  liable for damages which result from relying on the accuracy of the information contained in this specification. This specification is subject to change without notification._ 

_If you find any errors or require additional explanation, please inform Quicklogic.  All trademarks and / or trade names are property of their respective owners._ 

_Copyright © 2020 QuickLogic_ 

_All rights reserved._ 

_QuickLogic Corporation 2220 Lunday Ave. San Jose CA. 95131, USA_ 

UART IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 7_** 

