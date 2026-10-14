---
title: "GPIO IP for EOS 3B"
source_file: "qorc-sdk/s3-gateware/ip_modules/GPIO/docs/GPIO_register_map.pdf"
pages: 9
sha256: 1785f23d8a3a2f91dea08426cc1c810bf4840dd2ff52771e2bd47372bf4ac27c
---

# GPIO IP for EOS 3B

# GPIO FPGA IP 

_Revision: 1.01 Date: 22 Oct 2020_ 

## _QuickLogic Corporation_ 

GPIO IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 1_** 

### **1 Theory of Operation** 

The GPIO IP module allows software running on the S3’s M4 microprocessor to control up to 32 individual GPIO’s (General-Purpose I/O’s). Each of the GPIO’s may be mapped to device pins. Each GPIO may be designated as an input or output, and data can be read from, or written to, each I/O pin via control registers. The control registers are connected to the Wishbone interface, so that software running in the M4 microprocessor can control each of the GPIO’s. 

The GPIO_io port on the GPIO Controller module should be connected to top-level ports on the FPGA. These top-level ports on the FPGA correspond to device pins, and firmware running on the M4 microprocessor in the S3 device will need to enable the FPGA to have control of the selected device pins. Refer to the S3 Device Technical Reference Manual for details on how to allow the FPGA to control specific device pins. 

If a particular application requires fewer than 32 GPIO’s, the unused GPIO’s coming out of the GPIO controller module may be left unconnected. If a particular application requires more than 32 GPIO pins, additional instantiations of this GPIO IP module can be inserted into the FPGA. 

#### **1.1 GPIO pad description** 

Each GPIO in the FPGA will be implemented as a bi-directional pad. The output-enable (GPIO_OE[n]) is controlled by the Direction Control register at offset 0x08. The outgoing data (GPIO_out[n]) is controlled by the Output Data register at offset 0x04. The incoming data (GPIO_in[n]) can be read from the Input Data register at offset 0x00. The corresponding bits each each of the 3 registers correspond to the same GPIO. For example, bit 0 in each of the registers all pertain to GPIO 0. Each register is 32 bits wide, with each bit corresponding to one of the 32 possible GPIO’s. 



<!-- Start of picture text -->
GPIO_OE[n]<br>GPIO_OUT[n] GPIO_1O[n]<br>(pad)<br>GPIO_IN[n] C<br><!-- End of picture text -->

GPIO IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 3_** 

### **2 Address Map Specification** 

#### **2.1 Memory Map** 

The EOS 3B system maps the FPGA IP into the address range of 0x40020000 to 0x4003FFFF. This address range provides 128K bytes of address range for FPGA based IP. Each instantiation of this GPIO IP module should be allocated a base address within the FPGA’s address space. The register offsets described in this document are all relative to the GPIO IP’s base address that you have chosen for your design. The GPIO IP module currently uses 256 bytes of address space, although this address space may not be fully utilized. 

##### **2.1.1 GPIO Address Table** 

Table 1 shows the allocation of the GPIO module’s address space. 

**Table 1: GPIO Register Table** 

|Register|Register Name|Reset Value|Description|
|---|---|---|---|
|0x00|GPIO Input Data||Input data from each<br>GPIO pin.|
|0x04|GPIO Output Data|0x00000000|Output data for each GPIO<br>pin.|
|0x08|GPIO Direction Control|0x00000000|Output enables for each<br>GPIO pin.|
|0x0C –<br>0xFF|Reserved|0x00||



#### **2.2 Description of Registers** 

The following sections will detail the registers for the GPIO IP module. 

##### **2.2.1 Conventions** 

|**Access Tag**|**Name**|**Meaning**|
|---|---|---|
|R|Read|field may be read by the user/sw|
|W|Write|field may be written by the user/sw|
|U|Update|field may be updated by hardware|
|S|Set|field may be set by the user|
|C|Clear|field may be cleared by the user|
|RO|Read Only|field can only be read by the user/sw|



##### **2.2.2 GPIO Registers** 

##### **_2.2.2.1 [0x00] GPIO Input Data_** 

Each bit of this register corresponds to one GPIO, and each GPIO signal may be connected to one device pin. The input data seen by each GPIO may be read from this register. 

**Table 2: GPIO Input Data** 

|**Name**<br>GPIO_IN[31:0]|**Bit(s)**<br>[31:0]|**Type**<br>RO|**Description**<br>Input data from each GPIO.|
|---|---|---|---|



##### **_2.2.2.2 [0x04] GPIO Output Data_** 

Each bit of this register corresponds to one GPIO, and each GPIO signal may be connected to one device pin. The output data to be driven out on each GPIO can be set in this register. Note that in order to drive a value out of the device, a given GPIO must be placed in “output mode” (see register 0x08: GPIO Direction Control). 

**Table 3: GPIO Output Data** 

|**Name**<br>GPIO_OUT[31:0]|**Bit(s)**<br>[31:0]|**Type**<br>R/W|**Description**<br>Output data for each GPIO.|
|---|---|---|---|



GPIO IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 5_** 

##### **_2.2.2.3 [0x08] GPIO Direction Control_** 

This register controls the output-enable for each GPIO, thereby setting the direction for each GPIO (input mode vs. output mode). 

**Table 4: GPIO Output Data** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
|GPIO_OE[31:0]|[31:0]|R/W|Output-enable for each GPIO.<br>0 = input mode, tri-state<br>1=output mode|



### **3 Revision History** 

|**Date**|**Revision**|**Author**|**Description**|
|---|---|---|---|
|7 Oct 2020|1.00|Randy O|Initial Release|
||||Added information to Section 1 to more clearly|
|22 Oct 2020|1.01|Randy O|describe the connection between control<br>registers and GPIO’s.|



GPIO IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 7_** 

- **4 Copyright and Trademark Information** 

_All trademarks and / or trade names are property of their respective owners._ 

_The information in this specification has been carefully reviewed for technical accuracy. However, QuickLogic does not take the responsibility for the accuracy of the included information. Quicklogic will not be held  liable for damages which result from relying on the accuracy of the information contained in this specification. This specification is subject to change without notification._ 

_If you find any errors or require additional explanation, please inform Quicklogic.  All trademarks and / or trade names are property of their respective owners._ 

_Copyright © 2020 QuickLogic_ 

_All rights reserved._ 

_QuickLogic Corporation 2220 Lundy Ave. San Jose CA. 95131, USA_ 

GPIO IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 9_** 

