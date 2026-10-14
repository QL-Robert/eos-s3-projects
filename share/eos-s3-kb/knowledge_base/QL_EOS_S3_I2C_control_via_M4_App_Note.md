---
title: "QL EOS S3 I2C control via M4 App Note"
source_file: "QL EOS S3 I2C control via M4 App Note.pdf"
pages: 15
sha256: b4b14c592d48d6423d50bda7253b29f286a498c9092c7c6c5aacd3dabc10c5ad
---

# QL EOS S3 I2C control via M4 App Note

**_QuickLogic® EOSTM S3 I2C control via M4 Application Note Rev 1.0_** 

# **QuickLogic**<sup>**®**</sup> **EOS™ S3 I2C IP Control Via M4 Application Note** 

- **• • • • •** 

## **Introduction** 

This document provides the required EOS S3 configuration to interface with external I2C devices using M4 via on-chip I2C IP. 

The EOS S3 contains two I2C Master IPs and one SPI Master IP. These IPs can be control by either M4 or Sensor Manager, selectable via configuration registers. The IPs share the same Wish Bine bus on the front end. The IPs have direct control of the associated assigned IO. 

Figure below shows the block level diagram for the internal connection for the IPs control. 



<!-- Start of picture text -->
SPiSlave EOS<br>Interface System<br>a a es<br>AHB Control<br>Master<br><!-- End of picture text -->



<!-- Start of picture text -->
Flexible<br>Fusion<br>Engine(FFE)<br>Wishbone<br>Bus #0<br>MasterInterfacePC #0 ExternalPC Bus #0<br>Sensor<br><!-- End of picture text -->



<!-- Start of picture text -->
anager #0 rr} PC<br>(SM) Master #1 External PC Bus #1<br>Interface<br>Sensor SPI<br>. _—<br>Wishbone<br><!-- End of picture text -->

**Figure 1: I2C IP controls** 

© 2020 QuickLogic Corporation 

<u>www.quicklogic.com</u> 1 

**_QuickLogic® EOSTM S3 I2C control via M4 Application Note Rev 1.0_** 

## **System Configuration** 

### **Power configuration** 

The I2C IP resides inside the Flexible Fusion Engine (FFE) power domain. Coming out of Power On Reset or system hard reset (SYS_RST_N assertion), the FFE power is off. Turning on FFE power is done via PMU register. 

Recommend sequence: 

1. Check FFE power 

2. If not on, turn on FFE power 

#### FFE Power registers 

##### **FFE_STATUS (address 0x40004490)** 

|**0x90**|**FFE_Status**|**31:0**||||
|---|---|---|---|---|---|
||**Bit Field**|**bit**|**R/W/C**|**Default**|**Description**|
||**RESERVED**|**31:4**|||**Reserved**|
||FFE_Clock_Gating|3|RHW|0x0|Test mode for clockgating;do not set|
||FFE_Shut_Down|2|RHW|0x1|Power domain is off|
||FFE_Deep_Sleep|1|RHW|0x0|Power domain in DeepSleepmode|
||FFE_Active|0|RHW|0x0|Power domain is on|



##### **FFE_FPGA_PF_Software_PD (power down) (address 0x40004600)** 

|**0x200**|**FFE_FB_PF_SW_PD**|**31:0**||||
|---|---|---|---|---|---|
||**Bit Field**|**bit**|**R/W/C**|**Default**|**Description**|
||**RESERVED**|**31:3**|||**Reserved**|
||PF_Software_PD|2|RWHC|0x0|1'b1: Put the power domain to power saving mode according to<br>configuration setting, HW will clear it once power down sequence is<br>finished.|
||FB_Software_PD|1|RHW|0x0|1'b1: Put the power domain to power saving mode according to<br>configuration setting, HW will clear it once power down sequence is<br>finished.|
||**FFE_Software_PD**|**0**|**RHW**|**0x0**|**1'b1: Put the power domain to power saving mode according to**<br>**configuration setting, HW will clear it once power down sequence**<br>**is finished.**|



##### **FFE_FPGA_PF_Software_WU (power on) (address 0x40004610)** 

|**0x200**|**FFE_FB_PF_SW_W**<br>**U**|**31:0**||||
|---|---|---|---|---|---|
||**Bit Field**|**bit**|**R/W/C**|**Default**|**Description**|
||**RESERVED**|**31:3**|||**Reserved**|
||PF_Software_WU|2|RWHC|0x0|1'b1: wake up power domain, HW will clear it once power up<br>sequence is finished.|
||FB_Software_WU|1|RHW|0x0|1'b1: wake up power domain, HW will clear it once power up<br>sequence is finished.|
||**FFE_Software_WU**|**0**|**RHW**|**0x0**|**1'b1: wake up power domain, HW will clear it once power up**<br>**sequence is finished.**|



© 2020 QuickLogic Corporation 

<u>www.quicklogic.com</u> 2 

**_QuickLogic® EOSTM S3 I2C control via M4 Application Note Rev 1.0_** 

### **Clocks Configuration** 

The I2C IP uses FFE clock to generate the SCL frequency. S3 clocks are derived from the onboard speed clock circuit (HOSC). The maximum frequency for C08x1 clock is 10MHz. 

Figure below shows the S3 clocks system. The flow for clock is OS >> C08X4 >> C08X1 >> I2C SCL 







<!-- Start of picture text -->
Divider<br>LI ovisoi<br>aa |<br>Cf = | a“<br>=e<br>[|<br>Cl | we<br>c s oe<br>e S oe<br>Ci | vu<br><!-- End of picture text -->









<!-- Start of picture text -->
sowie<br><!-- End of picture text -->





<!-- Start of picture text -->
oa<br><!-- End of picture text -->



















































<!-- Start of picture text -->
®<br><!-- End of picture text -->



















Recommend configuration: 

1. Set OSC and enable output (active by default) 

2. Set C08X4 

3. Enable C08X4 (gated by default) 

© 2020 QuickLogic Corporation <u>www.quicklogic.com</u> 

3 

**_QuickLogic® EOSTM S3 I2C control via M4 Application Note Rev 1.0_** 

##### 4. Enable C08X1 (gated by default) 

#### Clock registers 

##### **OSC_CTRL_0 (address 0x40005480)** 

|**0x80**|**OSC_CTRL_0 **|**31:0**||||
|---|---|---|---|---|---|
||**Bit Field**|**bit**|**R/W/C**|**Default**|**Description**|
||**RESERVED**|**31:2**|||**Reserved**|
||fref16k_sel|1|RW|0x0|1'b0: reference clock is 32KHz<br>1'b1: reference clock is 16KHz|
||en|0|RW|0x1|1'b0: OSC OFF<br>1'b1: OSC ON<br>(NO SYNC needed,OSCguarantee there is no Glitch)|



##### **OSC_CTRL_1 (address 0x40005484)** 

|**0x84**|**OSC_CTRL_1 **|**31:0**||||
|---|---|---|---|---|---|
||**Bit Field**|**bit**|**R/W/C**|**Default**|**Description**|
||**RESERVED**|**31:13**|||**Reserved**|
||prog|12:0|RW|0x92D|Please refer TRM for details of OSC frequency programming<br>(No SYNC Needed)<br>Power On Default Value is 76.97 MHz<br>No Support on "Delta Mode"|



##### **CLK_Control_C_0 (address 0x40004010)** 

|**0x10**|**CLK_Control_C_0 **|**31:0**||||
|---|---|---|---|---|---|
||**Bit Field**|**bit**|**R/W/C**|**Default**|**Description**|
||**RESERVED**|**31:10**|||**Reserved**|
||Enable Clock Divider|9|RW|0x1|1'b1 Clock Divider is ON<br>1'b0 Clock Divider is OFF,Output the Source Clock Directly|
||Clock_Divider_Ratio|8:0|RW|0x4|High Speed Clock Divider Ratio,<br>0x0 --> Divide by 2<br>0x1 --> Divide by 3<br>...<br>0x1FE --> Divide by 512<br>Others --> Reserved<br>Default 0x4,Divided by6.|



© 2020 QuickLogic Corporation 

<u>www.quicklogic.com</u> 4 

**_QuickLogic® EOSTM S3 I2C control via M4 Application Note Rev 1.0_** 

##### **C01_CLK_GATE (address 0x40004040)** 

|**0x40**|**C01_CLK_GATE**<br>**Bit Field**|**31:0**<br>**bit**|**R/W/C**|**Default**|**Description**|
|---|---|---|---|---|---|
||**RESERVED**|**31:10**|||**Reserved**|
||Path_9_Gating_Control|9|RW|0x1|1'b0: Clock is Stop.<br>1'b1: Clock is running<br>For SPT.|
||Reserved|8|||Reserved|
||Path_7_Gating_Control|7|RW|0x1|1'b0: Clock is Stop.<br>1'b1: Clock is running<br>To eFUSE|
||Path_6_Gating_Control|6|RW|0x0|1'b0: Clock is Stop.<br>1'b1: Clock is running<br>To SDMA|
||Path_5_Gating_Control|5|RW|0x0|1'b0: Clock is Stop.<br>1'b1: Clock is running<br>To I2S module inside A1|
||Path_4_Gating_Control|4|RW|0x1|1'b0: Clock is Stop.<br>1'b1: Clock is running<br>To AHB2APB Bridge /CFG DMA Bridge inside A1 , Allow M4 to<br>configure SPI Master to load the code|
||**Path_3_Gating_Control**|**3**|**RW**|**0x0**|**1'b0: Clock is Stop.**<br>**1'b1: Clock is running**<br>**To FFE**|
||Path_2_Gating_Control|2|RW|0x0|1'b0: Clock is Stop.<br>1'b1: Clock is running<br>To PKFIFO|
||Path_1_Gating_Control|1|RW|0x0|1'b0: Clock is Stop.<br>1'b1: Clock is running<br>To SDMA SRAM|
||Path_0_Gating_Control|0|RO|0x1|1'b0: Clock is Stop.<br>1'b1: Clock is running<br>To A0|



Note: Set Path_3_Gating_control to 0x1 

##### **C08_X4_CLK_GATE (address 0x40004048)** 

|**0x48**|**C08_X4_CLK_GATE**|**31:0**||||
|---|---|---|---|---|---|
||**Bit Field**|**bit**|**R/W/C**|**Default**|**Description**|
||**RESERVED**|**31:1**|||**Reserved**|
||Path_0_Gating_Control|0|RW|0x0|1'b0: Clock is Stop.<br>1'b1: Clock is running<br>To FFE X4 clk|



Note: Set Path_0_Gating_control to 0x1 

5 

© 2020 QuickLogic Corporation 

<u>www.quicklogic.com</u> 

**_QuickLogic® EOSTM S3 I2C control via M4 Application Note Rev 1.0_** 

##### **C08_X1_CLK_GATE (address 0x4000404C)** 

|**0x4C**|**C08_X1_CLK_GATE**|**31:0**||||
|---|---|---|---|---|---|
||**Bit Field**|**bit**|**R/W/C**|**Default**|**Description**|
||**RESERVED**|**31:4**|||**Reserved**|
||Path_3_Gating_Control|3|RW|0x0|1'b0: Clock is Stop.<br>1'b1: Clock is running<br>To PF ASYNC FIFO 0|
||Path_2_Gating_Control|2|RW|0x0|1'b0: Clock is Stop.<br>1'b1: Clock is running<br>To A0|
||Reserved|1||0x0||
||Path_0_Gating_Control|0|RW|0x0|1'b0: Clock is Stop.<br>1'b1: Clock is running<br>To FFE X1 clk|



Note: Set Path_2_Gating_control to 0x1 & Set Path_2_Gating_control to 0x1 

### **FFE Wishbone Bus Configuration** 

The FFE Wishbone Bus controller has configuration registers that can enable one of the three IPs: I2C0 master, I2C1 master and SPI master for Sensor. The target IP is selected using WB_ADDR. 

The programming sequence is described in the programming examples section. 

FFE Wishbone Control registers 

**WB_ADDR (address 0x4004A000)** 

|**0x0**|**WB_ADDR**|**31:0**||||
|---|---|---|---|---|---|
||**Bit Field**|**bit**|**R/W/C**|**Default**|**Description**|
||**RESERVED**|**31:8**|||**Reserved**|
||slave_sel|7:6|RW|0x0|MSB to select which slave accessed by WB master<br>0x0 = I2C_0<br>0x1 = I2C_1<br>0x2 = SPI_0|
||RESERVED|5:3||0x0||
||Addr|2:0|RW|0x0|IP register address via WB master|



<u>www.quicklogic.com</u> 6 

© 2020 QuickLogic Corporation 

**_QuickLogic® EOSTM S3 I2C control via M4 Application Note Rev 1.0_** 

##### **WDATA (address 0x4004A004)** 

|**0x04**|**WDATA**|**31:0**||||
|---|---|---|---|---|---|
||**Bit Field**|**bit**|**R/W/C**|**Default**|**Description**|
||**RESERVED**|**31:8**|||**Reserved**|
||Wdata|7:0|RW|0x0|IP register data via WB master|



##### **CSR (address 0x4004A008)** 

|**0x8**|**WB_ADDR**|**31:0**||||
|---|---|---|---|---|---|
||**Bit Field**|**bit**|**R/W/C**|**Default**|**Description**|
||**RESERVED**|**31:8**|||**Reserved**|
||spi0_mux_sel|7|RW|0x0|SPI_0 wishbone control mux select<br>1 = Control from WB Master<br>0 = Control from SM1|
||i2c1_mux_sel|6|RW|0x0|I2C_1 wishbone control mux select<br>1 = Control from WB Master<br>0 = Control from SM1|
||i2c0_mux_sel|5|RW|0x0|I2C_0 wishbone control mux select<br>1 = Control from WB Master<br>0 = Control from SM0|
||OVFL|4|RO|0x0|ffe_push_overflow|
||BUSY|3|RO|0x0|WB Busy|
||mux_wb_sm|2|WO|0x0|Mux select between SM and WB masters (1 = WB master, 0 = SM<br>WB master)|
||wb_ms_wen|1|RW|0x0|WB master write enable<br>1 = Write<br>0 = Read|
||wb_ms_start|0|RW|0x0|WB master start transactions. This bit is self clear|



##### **RDATA (address 0x4004A00C)** 

|**0xC**|**RDATA**|**31:0**||||
|---|---|---|---|---|---|
||**Bit Field**|**bit**|**R/W/C**|**Default**|**Description**|
||**RESERVED**|**31:8**|||**Reserved**|
||Rdata|7:0|RO|0x0|Read data from IP to WB master is registered|



### **I2C Master IP Control** 

The S3 I2C master Controller is based on the OpenCore I2C Master IP develop by Richard Herveille (revision 0.9); the IP has minor modification to fit with S3 architecture and compatible with QuickLogic Flexible Fusion Engine. There is no direct access to the I2C registers. The Wishbone Bus control registers manage the write/read to the I2C controller registers. 

© 2020 QuickLogic Corporation 

<u>www.quicklogic.com</u> 

7 

**_QuickLogic® EOSTM S3 I2C control via M4 Application Note Rev 1.0_** 

#### I2C Master Control registers 

##### **Control Register (address 0x2)** 

|**Bit #**|**Access**|**Description**|
|---|---|---|
|7|RW|EN, I<sup>2</sup>C IP enable bit.<br>When set to ‘1’, the IP is enabled.<br>When set to ‘0’, the IP is disabled.|
|6|RW|IEN, I<sup>2</sup>C IP interrupt enable bit.<br>When set to ‘1’, interrupt is enabled.<br>When set to ‘0’, interrupt is disabled.|
|5|RW|Enable / disable arbitration lost logic<br> 0 – enables it (default to enable)<br>1 – disables it|
|4|RW|Enable / disable wait state (clock stretching) for pre-scale= 0<br> 0 – enables it (default to enable)<br>1 – disables it|
|3:0|RW|Reserved|



##### **Transmit Register (address 0x3) - W** 

|**Bit #**|**Access**|**Description**|
|---|---|---|
|7:1|W|Next byte to transmit via I<sup>2</sup>C|
|0|W|In case of a data transfer this bit represent the data’s LSB.|
|||In case of a slave address transfer this bit represents the RW bit.|
|||‘1’ = reading from slave<br>‘0’ = writing to slave|



© 2020 QuickLogic Corporation 

<u>www.quicklogic.com</u> 

8 

**_QuickLogic® EOSTM S3 I2C control via M4 Application Note Rev 1.0_** 

##### **Receive Register (address 0x3) - R** 

|**Bit #**|**Access**|**Description**|
|---|---|---|
|7:0|R|Last byte received via I<sup>2</sup>C|



##### **Command Register (address 0x4) - W** 

|**Bit #**|**Access**|**Description**|
|---|---|---|
|7|W|STA, generate (repeated) start condition|
|6|W|STO, generate stop condition|
|5|W|RD, read from slave|
|4|W|WR, write to slave|
|3|W|ACK, when a receiver, sent ACK (ACK = ‘0’) or NACK (ACK = ‘1’)|
|2:1|W|Reserved|
|0|W|_IACK, Interrupt acknowledge. When set, clears a pending interrupt._|



The STA, STO, RD, WR, and IACK bits are cleared automatically. These bits are always read as zeros. 

**Status Register (address 0x4) - R** 

|**Bit #**|**Access**|**Description**|
|---|---|---|
|7|R|RxACK, Received acknowledge from slave.<br>This flag represents acknowledge from  the addressed slave.<br>‘1’ = No acknowledge received<br>‘0’ = Acknowledge received|
|6|R|_Busy, I_<sup>_2_</sup>_C bus busy_<br>‘1’ after START signal detected<br>‘0’ after STOP signal detected|
|5|R|_AL, Arbitration lost_<br>This bit is set when the IP lost arbitration. Arbitration is lost when:<br>•<br>a STOP signal is detected, but non requested<br>•<br>The master drives SDA high, but SDA is low.<br>See_bus-arbitration_section for more information.|
|4:2|R|Reserved|
|1|R|TIP, Transfer in progress.<br>‘1’ when transferring data<br>‘0’ when transfer complete|



© 2020 QuickLogic Corporation 

<u>www.quicklogic.com</u> 

9 

**_QuickLogic® EOSTM S3 I2C control via M4 Application Note Rev 1.0_** 

|0<br>R|IF, Interrupt Flag. This bit is set when an interrupt is pending, which will cause a<br>processor interrupt request if the IEN bit is set.|
|---|---|
||The Interrupt Flag is set when:|
||•<br>one byte transfer has been completed<br>•<br>arbitration is lost|



## **M4 Programming examples** 

### **M4 programming sequence: I2C Register Write** 

A typical I2C register write cycle has 3 transfer phases: 

Phase 1: I2C device address phase – write: 7-bit device address + W + ACK; check WB bus status 

- Set WB_ADDR: select I2C and select I2C TXR register 

- Set WDATA: set I2C device address + W bit 

- Set CSR: initiate WB transfers; update I2C register TXR with WDATA content 

- Set WB_ADDR: select I2C and select I2C CR register 

- Set WDATA: set I2C transfer cycle type - write 

- Set CSR: initiate WB transfers; update I2C registers CR with WDATA content and start I2C address phase transfer 

Phase 2: I2C device register address phase: 8-bit + ACK; check WB bus status 

- Set WB_ADDR: select I2C and select I2C TXR register 

- Set WDATA: set I2C device register address 

- Set CSR: initiate WB transfers; update I2C register TXR with WDATA content 

- Set WB_ADDR: select I2C and select I2C CR register 

- Set WDATA: set I2C transfer cycle type - write 

- Set CSR: initiate WB transfers; update I2C registers CR with WDATA content and start I2C register address phase transfer 

Phase 3: I2C device register data (write): 8-bit + ACK (could be multiple data bytes); the last write data byte must terminated with I2C STOP condition; check I2C TIP (Transfer in Progress) status 

- Set WB_ADDR: select I2C and select I2C TXR register 

- Set WDATA: set I2C register write data 

- Set CSR: initiate WB transfers; update I2C register TXR with WDATA content 

- Set WB_ADDR: select I2C and select I2C CR register 

- Set WDATA: set I2C transfer cycle type (select STOP or Multiple DATA I2C cycles) - write 

- Set CSR: initiate WB transfers; update I2C registers CR with WDATA content and start I2C register data phase transfer 

Note: to write multiple bytes, repeat Phase 3 until the last byte write; change the CR content to generate STOP condition upon writing the last byte. 

### **M4 programming sequence: I2C register Read** 

A typical I2C register read cycle has 4 transfer phases: 

Phase 1: I2C device address phase – write: 7-bit device address + W + ACK; check WB bus status 

- Set WB_ADDR: select I2C and select I2C TXR register 

- Set WDATA: set I2C device address + W bit 

- Set CSR: initiate WB transfers; update I2C register TXR with WDATA content 

© 2020 QuickLogic Corporation <u>www.quicklogic.com</u> 10 

**_QuickLogic® EOSTM S3 I2C control via M4 Application Note Rev 1.0_** 

- Set WB_ADDR: select I2C and select I2C CR register 

- Set WDATA: set I2C transfer cycle type - write 

- Set CSR: initiate WB transfers; update I2C registers CR with WDATA content and start I2C address phase transfer 

Phase 2: I2C device register address phase: 8-bit + ACK; check WB bus status 

- Set WB_ADDR: select I2C and select I2C TXR register 

- Set WDATA: set I2C device register address 

- Set CSR: initiate WB transfers; update I2C register TXR with WDATA content 

- Set WB_ADDR: select I2C and select I2C CR register 

- Set WDATA: set I2C transfer cycle type - write 

- Set CSR: initiate WB transfers; update I2C registers CR with WDATA content and start I2C register address phase transfer 

Note: a STOP condition or RESTART condition is required at the end of this phase. 

Phase 3: I2C device address phase – read: 7-bit device address + R + ACK; check WB bus status 

- Set WB_ADDR: select I2C and select I2C TXR register 

- Set WDATA: set I2C device address + R bit 

- Set CSR: initiate WB transfers; update I2C register TXR with WDATA content 

- Set WB_ADDR: select I2C and select I2C CR register 

- Set WDATA: set I2C transfer cycle type - write 

- Set CSR: initiate WB transfers; update I2C registers CR with WDATA content and start I2C address phase transfer 

Phase 4: I2C device register data read phase: 8-bit + ACK; check WB bus status 

- Set WB_ADDR: select I2C and select I2C CR register 

- Set WDATA: set read one byte and send ACK 

- Set CSR: initiate WB transfers; update I2C register CR with WDATA content 

- Set WB_ADDR: select I2C and select I2C TXR register 

- Set CSR: initiate WB transfers; to transfer data to read registers 

- Read from RDATA 

Note: to read multiple bytes, repeat Phase 3 & 4 until the last byte read; change the CR content to generate STOP condition upon reading the last byte. 

### **Programming Examples** 

#### Example 1: 

Write data 0x10 to register 0x1A of I2C device with address 0x51 

- Slave address + W = {0x51 (b”1010001”), 0x0} = 0xA2 (8’b10100010) 

- Register address = 0x1A 

- Write Data = 0x10 

Details: 

1. Write 0x03 to address 0x4004a000 

2. Write 0xA2 to address 0x4004a004 

3. Write 0x23 to address 0c4004a008 

4. Write 0x04 to address 0x4004a000 

5. Write 0x90 to address 0x4004a004 

© 2020 QuickLogic Corporation 

<u>www.quicklogic.com</u> 

11 

**_QuickLogic® EOSTM S3 I2C control via M4 Application Note Rev 1.0_** 

6. Write 0x23 to address 0c4004a008 

7. Write 0x03 to address 0x4004a000 

8. Write 0x1A to address 0x4004a004 

9. Write 0x23 to address 0c4004a008 

10. Write 0x04 to address 0x4004a000 

11. Write 0x10 to address 0x4004a004 

12. Write 0x23 to address 0c4004a008 

13. Write 0x03 to address 0x4004a000 

14. Write 0x10 to address 0x4004a004 

15. Write 0x23 to address 0c4004a008 

16. Write 0x04 to address 0x4004a000 

17. Write 0x50 to address 0x4004a004 

18. Write 0x23 to address 0c4004a008 

#### Example 2 

Read a byte data from register 0x1A of I2C device with address 0x51 

- Slave address + W = {0x51 (b”1010001”), 0x0} = 0xA2 (8’b10100010) 

- • Slave address + R = {0x51 (b”1010001”), 0x1} = 0xA3 (8’b10100011) 

- Register address = 0x1A 

Details: 

1. Write 0x03 to address 0x4004a000 

2. Write 0xA2 to address 0x4004a004 

3. Write 0x23 to address 0c4004a008 

4. Write 0x04 to address 0x4004a000 

5. Write 0x90 to address 0x4004a004 

6. Write 0x23 to address 0c4004a008 

7. Write 0x03 to address 0x4004a000 

8. Write 0x1A to address 0x4004a004 

9. Write 0x23 to address 0c4004a008 

10. Write 0x04 to address 0x4004a000 

11. Write 0x50 to address 0x4004a004 

12. Write 0x23 to address 0c4004a008 

13. Write 0x03 to address 0x4004a000 

14. Write 0xA3 to address 0x4004a004 

15. Write 0x23 to address 0c4004a008 

16. Write 0x04 to address 0x4004a000 

17. Write 0x90 to address 0x4004a004 

18. Write 0x23 to address 0c4004a008 

19. Write 0x04 to address 0x4004a000 

20. Write 0x68 to address 0x4004a004 

21. Write 0x23 to address 0c4004a008 

22. Write 0x03 to address 0x4004a000 

© 2020 QuickLogic Corporation 

<u>www.quicklogic.com</u> 

12 

**_QuickLogic® EOSTM S3 I2C control via M4 Application Note Rev 1.0_** 

23. Write 0x21 to address 0x4004a004 

24. Read from address 0c4004a00C 

© 2020 QuickLogic Corporation 

<u>www.quicklogic.com</u> 

13 

**_QuickLogic® EOSTM S3 I2C control via M4 Application Note Rev 1.0_** 

## **Contact Information** 

Phone: (408) 990-4000 (US) +(44) 1932-21-3160 (Europe) +(886) 26-603-8948 (Taiwan) +(86) 139-0517-5302 (China) +(81) 3-5875-0547 (Japan) +(82) 31-601-4225 (Korea) E-mail: <u>info@quicklogic.com</u> 

Sales: <u>America-sales@quicklogic.com Europe-sales@quicklogic.com Asia-sales@quicklogic.com Japan-sales@quicklogic.com</u> 

<u>Korea-sales@quicklogic.com</u> Support: www.quicklogic.com/support 

Internet: www.quicklogic.com 

## **Notice of Disclaimer** 

QuickLogic is providing this design, product or intellectual property "as is." By providing the design, product or intellectual property as one possible implementation of your desired system-level feature, application, or standard, QuickLogic makes no representation that this implementation is free from any claims of infringement and any implied warranties of merchantability or fitness for a particular purpose. You are responsible for obtaining any rights you may require for your system implementation. QuickLogic shall not be liable for any damages arising out of or in connection with the use of the design, product or intellectual property including liability for lost profit, business interruption, or any other damages whatsoever. QuickLogic products are not designed for use in life-support equipment or applications that would cause a life-threatening situation if any such products failed. Do not use QuickLogic products in these types of equipment or applications. 

QuickLogic does not assume any liability for errors which may appear in this document. However, QuickLogic attempts to notify customers of such errors. QuickLogic retains the right to make changes to either the documentation, specification, or product without notice. Verify with QuickLogic that you have the latest specifications before finalizing a product design. 

## **Copyright and Trademark Information** 

Copyright © 2020 QuickLogic Corporation. All Rights Reserved. 

The information contained in this document is protected by copyright. All rights are reserved by QuickLogic Corporation. QuickLogic Corporation reserves the right to modify this document without any obligation to notify any person or entity of such revision. Copying, duplicating, selling, or otherwise distributing any part of this product without the prior written consent of an authorized representative of QuickLogic is prohibited. 

QuickLogic and ArcticLink are registered trademarks, and the QuickLogic logo is a trademark of QuickLogic. Other trademarks are the property of their respective companies. 

© 2020 QuickLogic Corporation 

<u>www.quicklogic.com</u> 

14 

**_QuickLogic® EOSTM S3 I2C control via M4 Application Note Rev 1.0_** 

## **Revision History** 

|**Revision**|**Date**||**Comments**|
|---|---|---|---|
|1.0|August 2016|1<sup>st</sup>release||





15 

© 2020 QuickLogic Corporation 

<u>www.quicklogic.com</u> 

