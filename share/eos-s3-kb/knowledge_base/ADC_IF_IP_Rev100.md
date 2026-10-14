---
title: "ADC FPGA IP for EOS 3B"
source_file: "qorc-sdk/s3-gateware/adc_ad7476_if/doc/ADC_IF_IP_Rev100.pdf"
pages: 13
sha256: 39972950be3f5ae8886615805b84cd61e2c74a6e353bb473c7c437c5b64f0ce3
---

# ADC FPGA IP for EOS 3B

# ADC Interface FPGA IP 

_Revision: 1.0 Date: 26 Aug 2020_ 

## _QuickLogic Corporation_ 

ADC FPGA IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 1_** 

- **1 Requirement:** 

   1. Interface with Analog devices chip AD7476A (12-bit ADC) 

   2. Fast throughput rate: 1 MSPS 

- **2 System Block Diagram:** 



<!-- Start of picture text -->
S3 ASSP<br>WB  SDMA<br>INTR Master  Signals<br>S3 FPGA<br>WB Slave IF<br>DMA<br>FSM<br>CSn_o<br>FPGA<br>Serializer/ SCLK_o Analog_in<br>Registers & Reserializer AD7476A<br>SDATA_i<br>RX FIFO<br>FSM<br><!-- End of picture text -->

ADC FPGA IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 3_** 

### **3 Pinout (for the QuickFeather board):** 

|**Signal**<br>**Name**|**eFPGA**<br>**port #**<br>**(S3B**<br>**device)**|**QFN**<br>**package**<br>**pin**|**QuickFeather**<br>**J8 connector**|**PMOD**<br>**Interface**<br>**Type 2**<br>**(SPI)**|**Direction**|**Description**|
|---|---|---|---|---|---|---|
|CSn_o|IO_31|23|J8.5|Pin 1|Output|Slave Select, Active Low|
|SCLK_o|IO_7|63|J8.11|Pin 4|Output|SPI Clock|
|SDATA_i|IO_5|64|J8.9|Pin 3|Input|MISO|
|SDATA_o|IO_12|56|J8.7|Pin 2|Output|MOSI,unused|
|GND_o|IO_10|59|J8.13|Pin 5|Output|GND, required on<br>PMOD connector|
||||J8.15|Pin 6||VCC|



### **4 Address Map Specification** 

#### **4.1 Memory Map** 

The EOS 3B system maps the FPGA IP into the address range of 0x40020000 to 0x4003FFFF. This address range provides 128K bytes of address range for FPGA based IP. The following tables further define the registers within this range. 

**Table 1-1: FPGA IP Register Space** 

|Register|Block|Space Allocated|Remarks|
|---|---|---|---|
|0x40020000 –<br>0x400200FF|FPGA IP Registers|256 bytes||
|0x40020100 –<br>0x4002FFFF|Reserved|0x0||
|0x40030000 –<br>0x40030FFF|DMA control/Status<br>registers|1024 Words|Dedicated DMA<br>registers|
|0x40031000 –<br>0x40031FFF|DMA CH0 Port<br>register|1024 Words|Dedicated 4KB space<br>for DMA Channel 0|
|0x40032000 –<br>0x4003FFFF|Reserved|0x0||



#### **4.2 Register Address Table** 

The following sections will outline the expected allocation of registers and describe their operations. 

**4.2.1 FPGA Registers Address Table** 

Table 1-2 shows the expected allocation of FPGA Registers address space. 

ADC FPGA IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 5_** 

**Table 1-2: FPGA IP Register Table** 

|Register|Block|Reset Value|Remarks|
|---|---|---|---|
|0x40020000|IP Device ID|0x0ADC0001|Read only|
|0x40020004|IP Revision number|0x00000100|Read only<br>Version 1.0|
|0x40020008|FIFO Flush|0x00||
|0x4002000C|Sensor Enable Register|0x0|Read/Write|
|0x40020010 –<br>0x400200FF|Not Used|0x0||
|0x40020100 –<br>0x4002FFFF|Reserved|0x0||
|0x40030000|DMA Enable Register|0x0|Read/Write|
|0x40030004|DMA Status Register|0x0|Read only|
|0x40030008|DMA Interrupt Enable<br>Register|0x0|Read/Write|
|0x4003000C –<br>0x40030FFF|Not Used|0x0||
|0x40031000|DMA Read Port register|0x0|Read only|
|0x40031004 –<br>0x40031FFF|Not Used|0x0||
|0x40032000 –<br>0x4003FFFF|Reserved|0x0||



#### **4.3 Description of Registers** 

The following sections will detail the registers for each address space. 

##### **4.3.1 Conventions** 

|**Access Tag**|**Name**|**Meaning**|
|---|---|---|
|R|Read|field may be read by the user/sw|
|W|Write|field may be written by the user/sw|
|U|Update|field may be updated by hardware|
|S|Set|field may be set by the user|
|C|Clear|field may be cleared by the user|
|RO|Read Only|field can only be read by the user/sw|



##### **4.3.2 FPGA IP Registers** 

##### **_4.3.2.1 IP Device ID register_** 

Register Address location: 0x40020000 Reset Value: 0x0ADC0001 

**Table 1-3.1: ID Value Register** 

|**Name**<br>IP Device ID|**Bit(s)**<br>[31:0]|**Type**<br>RO|**Description**<br>0x0ADC0001 : Read only|
|---|---|---|---|



##### **_4.3.2.2 IP revision number register_** 

Register Address location: 0x40020004 Reset Value: 0x0100 

**Table 1-3.2: Revision Number Register** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
|Revision Number|[15: 0]|RW|0x0100 : Read only|
|Not Used|[31:16]|RO|Return “0” when read|



ADC FPGA IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 7_** 

##### **_4.3.2.3 FIFO Reset Register_** 

Register Address location: 0x40020008 

Reset Value: 0x0 

**Table 1-3.3: FIFO Reset Register** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
|FIFO Reset|[0]|RW|RX FIFO Flush<br>HW auto clear|
|Not Used|[31:1]|RO|Return “0” when read|



##### **_4.3.2.4 Sensor Enable Register_** 

Register Address location: 0x4002000C 

Reset Value: 0x0 

**Table 1-3.4: Sensor Enable Register** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
||||0 – Sensor Disabled|
|Sensor 1 Enable|[0]|R/W|1 – Sensor Enabled|
||||When enabled the IP starts reading from the ADC|
|Reserved|[31:4]|R|Return “0” when read|



##### **_4.3.2.5 DMA Enable Register_** 

Register Address location: 0x40030000 Reset Value: 0x00 

**Table 1-3.11: DMA Enable Register** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
||||DMA Enable For channel 0|
||||0 – Disable|
|DMA CH0 Enable|[0]|R/W|1 – Enable|
||||HW clears this bit when the DMA transfer is done.|
||||DMA for reading the Sensor data.|
|Reserved|[31:1]|R|Returns “0”|



##### **_4.3.2.6 DMA Status Register_** 

Register Address location: 0x40030004 

Reset Value: 0x00 

**Table 1-3.12: DMA Status Register** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
|DMA Done Interrupt|[0]|R/W|DMA Read Done Interrupt<br>FW needs to clear the interrupt, write 0 to clear.|
|Reserved|[31:1]|R|Returns “0”|



##### **_4.3.2.7 DMA Interrupt Enable Register_** 

Register Address location: 0x40030008 

Reset Value: 0x00 

**Table 1-3.13: DMA Interrupt Enable Register** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
|DMA Done Interrupt<br>Enable|[0]|R/W|0 – disable<br>1 – enable.|
|Reserved|[31:1]|R|Returns “0”|



##### **_4.3.2.8 DMA CH0 Data Port Register (Read Port)_** 

Register Address location: 0x40031000 Reset Value: 0x00 

**Table 1-3.14: DMA CH0 Data Port Register (Read Port)** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
|DMA CH0 Port|[31:0]|R|DMA CH0 Port (Read Port)<br>RX FIFO Read Port|



ADC FPGA IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 9_** 

### **5 Programming steps:** 

1. Reset FIFO 

2. M4 sets up DMA CH0 (FPGA Channel12) for Reading the Sensor data 

3. M4 Enables the DMA for CH0 

4. M4 Programs the Sensor Enable Register (0x4002000C) 

5. When Sensor Enabled, FPGA IP reads the data from the AD7476A device and writes into the RX FIFO. 

6. FPGA IP generates DREQ to the SDMA controller to read the data 

7. When Read DMA is complete DMA Done Interrupt is generated 

8. M4 repeats step 2 to 3 to set up the next DMA and capture the sensor data 

9. FPGA IP continues to read the Data from AD7476A device until the Sensor is disabled 

### **6 Data Format (32 -bit DMA):** 

Sensor data: 



<!-- Start of picture text -->
 Sensor Data1 [15:0]  Sensor Data0 [15:0]<br>Sensor Data3 [15:0]  Sensor Data2 [15:0]<br>Sensor Data5 [15:0]  Sensor Data4 [15:0]<br>Sensor Data7 [15:0]  Sensor Data6 [15:0]<br>.  .<br>. .<br><!-- End of picture text -->

### **7 Sampling Rate:** 

As mentioned in Step 9 in Section 5 above (Programming Steps), once the sensor has been enabled, the FPGA IP will continually read from the external ADC. Each read takes 18 clock cycles to execute a single SPI read command, including overhead. The clock that is used for the SPI transfer is sys_clk0 in the FPGA, which is driven by C16 in the S3B device. Refer to the S3 Technical Reference Manual (Chapter 10) for more information about configuring the various clocks in the device. 

When C16 is set to 18MHz, the resulting ADC sample rate is 1MHz (18MHz divided by 18 bits per SPI read). The effective ADC sample rate can be changed by using a different frequency for the C16 clock. 

### **8 Revision History** 

|**Date**|**Revision**|**Author**|**Description**|
|---|---|---|---|
|21 Aug 2020|1.0|Randy O|Copied from a previous customer design.<br>Modified for the QuickFeather board. Changed<br>the device and revision ID’s, modified pinout<br>table in section 3.|
|26 Aug 2020|1.0|Randy O|Added sampling rate information. No changes to<br>design source files.|



ADC FPGA IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 11_** 

- **9 Copyright and Trademark Information** 

_All trademarks and / or trade names are property of their respective owners._ 

_The information in this specification has been carefully reviewed for technical accuracy. However, QuickLogic does not take the responsibility for the accuracy of the included information. Quicklogic will not be held  liable for damages which result from relying on the accuracy of the information contained in this specification. This specification is subject to change without notification._ 

_If you find any errors or require additional explanation, please inform Quicklogic.  All trademarks and / or trade names are property of their respective owners._ 

_Copyright © 2016 QuickLogic_ 

_All rights reserved._ 

_QuickLogic Corporation 2220 Lundy Ave. Sunnyvale CA. 95131, USA_ 

ADC FPGA IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 13_** 

