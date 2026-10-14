---
title: "QuickLogic Application 146 - EOS S3LV Integration Guide"
source_file: "QL Application Note 146 \u2013 QL S3LV Integration Guide.pdf"
pages: 5
sha256: bde15e9cb5c2cc75eeffd26a7d6a059d4047fa8a119ab97289f4fdb10e773e11
---

# QuickLogic Application 146 - EOS S3LV Integration Guide

## **QuickLogic**<sup>**®**</sup> **– EOS S3LV – Integration Guide** 

**• • • • • • QuickLogic Application Note 146** 

### **Overview** 

The EOS S3LV operates at 0.85 VDD. This provides a power savings averaging 33% relative to the EOS S3 operating at 1.0 VDD. 

The device’s top frequency is reduced from 80 MHz to 48 MHz with other frequencies scaled by the same 0.6 factor. The S3LV runs industry leading always-on, listening, wake-word technology for hearables and wearables and IOT that fit in this frequency range. 

The maximum frequency for each EOS S3LV Clock Domain is specified in the tables in the guide. 

### **EOS S3LV Operating Frequencies** 

The EOS S3LV platform contains 19 clock domains with different operating frequencies. See **Table 1** for a full listing of the clocks domains. 

Table 1: Clocks Listing 

|**Block Name(s)**|**Maximum**<br>**Frequency**<sup>**a**</sup>|**Clock**<br>**Name**|**Clock Path**|**Notes**|
|---|---|---|---|---|
|**Always-On Domain**|||||
|AP to SPI_Slave, SPI_Slave to<br>TLC, TLC to PKT_FIFO clock|12 MHz|C00|P0_A0||
|TLC clock to AHB Switch (AHB<br>clock)|6 MHz|C01|P0_A0|AHB clock must be greater than or<br>equal to one half of the SPI slave clock<br>(in the line above).|
|AHB Switch, Reg Bank, other<br>blocks connected to the switch on<br>the Always-On Power Domain|6 MHz|C01|P0_A0||
|**A1 Domain**|||||
|CfgSM, CfgDMA, SPI_Master<br>(APB clock)|24 MHz|C02|P0_A1||
|CfgDMA (AHB clock)|6 MHz|C01|P4_A1||
|SPI_Master serial data clock|12 MHz|C02|n/a|The SPI_Master serial clock frequency<br>is one half of the C02 clock frequency.|
|I2S Slave (APB clock)|6 MHz|C01|P5_I2S||
|**I**<sup>**2**</sup>**S Domain**|||||
|I2S slave (DA pin)|6 MHz|C32|P0_I2S||
|I2S Slave APB interface|6 MHz|C01|P5_I2S||



© 2018 QuickLogic Corporation 

# **<mark>CONFIDENTIAL</mark>** 

# **PRELIMINARY** 

<u>www.quicklogic.com</u> **1** ••• ••• 

**_QuickLogic_**<sup>**_®_**</sup> **_– EOS S3LV – Integration Guide Rev. 1.0_** 

Table 1: Clocks Listing _(Continued)_ 

|**Block Name(s)**|**Maximum**<br>**Frequency**<sup>**a**</sup>|**Clock**<br>**Name**|**Clock Path**|**Notes**|
|---|---|---|---|---|
|**Efuse Domain**|||||
|Efuse (APB clock)|24 MHz|C02|P2_FUSE||
|**SDMA Domain**|||||
|For AHB2APB and SDMA (AHB<br>clock)|6 MHz|C01|P6_SDMA||
|**SDMA SRAM Domain**|||||
|SDMA SRAM|6 MHz|C01|P1_A0||
|**FFE Domain**|||||
|AHB switch|6 MHz|C01|P3_FFE||
|X1 clk|6 MHz|C08|X1_P0_FFE||
|X4 clk|24 MHz|C08|X4_P0_FFE||
|For A0|6 MHz|C08|X1_P2_A0||
|for PKT FIFO|6 MHz|C08|X1_P3_PF||
|**Packet FIFO Domain**|||||
|PKF FIFO (AHB clock)|6 MHz|C01|P2_PF||
|PKF FIFO (TLC clock)|12 MHz|C00|P0_A0||
|PKF FIFO (FPGA clock)|6 MHz|C41|n/a||
|PKF FIFO (FFE clock)|6 MHz|C08|X1_P3_PF||
|**M4 Complex Domain**|||||
|M4-Complex: M4 subsystem, M4-<br>AHB switch (AHB clock)|48 MHz|C10|HCLK_P0_M4<br>FCLK_P0_M4||
|M4-Complex: UART, WDT1,<br>Timer1 (APB clock 0)|6 MHz|C11|P0_M4||
|M4-Complex: to Voice SS and<br>CFG_CTL (APB clock 1)|48 MHz|C10|FCLK_PS_AD0||
|M4 CFG_CTL to FPGA (APB<br>clock)|6 MHz|C09|P2_FB||
|A0 (AHB clock M4)|48 MHz|C10|FCLK_P6_A0||
|M4 SWD (DA pin)|12 MHz|CS|P0_M4||
|**M4 SRAM Domain**|||||
|M4 SRAM 0 (AHB clock)|48 MHz|C10|FCLK_P1_MS0||
|M4 SRAM 1 (AHB clock)|48 MHz|C10|FCLK_P2_MS1||
|M4 SRAM 2 (AHB clock)|48 MHz|C10|FCLK_P3_MS2||
|M4 SRAM 3 (AHB clock)|48 MHz|C10|FCLK_P4_MS3||
|**Voice Subsystem Domain**|||||
|Voice SS (AHB clock)|48 MHz|C10|FCLK_P5_AD0|The ratio between the Voice SS AHB<br>and APB clock must be an integer ratio,<br>such as 1-1, 1-2, 1-4|
|Voice SS (APB clock)|16 MHz|C09|P0_AD5||
|PDM left clock|3 MHz|C30|P0_AD1||
|www.quicklogic.com<br>•• •••<br>**2**|**CON**|**FID**|**ENTIAL**|© 2018 QuickLogic Corporation<br>|
|•|**PRE**|**LIMI**|**NARY**||



© 2018 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_– EOS S3LV – Integration Guide Rev. 1.0_** 

Table 1: Clocks Listing _(Continued)_ 

|**Block Name(s)**|**Maximum**<br>**Frequency**<sup>**a**</sup>|**Clock**<br>**Name**|**Clock Path**|**Notes**|
|---|---|---|---|---|
|PDM right clock|3 MHz|C30|P1_AD2||
|I2S clock|3 MHz|C30|P2_AD4||
|LPSD clock|1 MHz|C31|P3_AD3||
|**FPGA Domain**|||||
|FPGA|6 MHz|C16|P0_FB||
|FPGA|6 MHz|C21|P0_FB||
|AHB2WB for FPGA clock|6 MHz|C40|P0_FB||
|FPGA to Packet FIFO clock|6 MHz|C41|P0_FB||



a. Maximum frequency is with VDD = 0.85V ±20mV after device configuration. 

### **S3LV Configuration** 

**Table 2** lists the configuration that must be defined in the Fw_global_config.h file to enable S3LV. 

Table 2: S3LV Configuration 

|**Parameter**||**Description**|
|---|---|---|
|S3_LVD|Enables S3LV|support.|



The main files that support the S3LV features are described in **Table 3** . If the source is ported to a new S3LV platform, the clock configurations and step sizes must be changed as required in the s3lvd_pwrcfg.c and s3lvd_pwrcfg.h files. 

Table 3: Main QD Files 

|**Filename**|**Description**|
|---|---|
|s3lvd_pwrcfg.c|Power configuration for S3 LVD.|
|s3lvd_pwrcfg.h|Step size and clock configuration for each node.|



For information about the Power Management Framework, refer to _QuickLogic S3 OPEN – Power Management Software_ . 

# **<mark>CONFIDENTIAL</mark> PRELIMINARY** 

• • • ••• 

© 2018 QuickLogic Corporation 

<u>www.quicklogic.com</u> **3** 

**_QuickLogic_**<sup>**_®_**</sup> **_– EOS S3LV – Integration Guide Rev. 1.0_** 

### **Contact Information** 

Phone: (408) 990-4000 (US) +(44) 1932-21-3160 (Europe) +(886) 2-6603-8947 (Taiwan) +(86) 139-0517-5302 (China) +(81) 3-5875-0547 (Japan) +(82) 31-601-4225 (Korea) 

E-mail: <u>info@quicklogic.com</u> Sales: <u>America-sales@quicklogic.com Europe-sales@quicklogic.com Asia-sales@quicklogic.com Japan-sales@quicklogic.com Korea-sales@quicklogic.com</u> 

Support: <u>www.quicklogic.com/support</u> 

Internet: <u>www.quicklogic.com</u> 

### **Revision History** 

|**Revision**|**Date**|**Originator and Comments**|
|---|---|---|
|1.0|March 2018|Gaurav Dua and Kathleen Bylsma|



### **Notice of Disclaimer** 

QuickLogic is providing this design, product or intellectual property "as is." By providing the design, product or intellectual property as one possible implementation of your desired system-level feature, application, or standard, QuickLogic makes no representation that this implementation is free from any claims of infringement and any implied warranties of merchantability or fitness for a particular purpose. 

You are responsible for obtaining any rights you may require for your system implementation. QuickLogic shall not be liable for any damages arising out of or in connection with the use of the design, product or intellectual property including liability for lost profit, business interruption, or any other damages whatsoever. QuickLogic products are not designed for use in life-support equipment or applications that would cause a life-threatening situation if any such products failed. Do not use QuickLogic products in these types of equipment or applications. 

QuickLogic does not assume any liability for errors which may appear in this document. However, QuickLogic attempts to notify customers of such errors. QuickLogic retains the right to make changes to either the documentation, specification, or product without notice. Verify with QuickLogic that you have the latest specifications before finalizing a product design. 

**4** <u>www.quicklogic.com</u> •• •••• 

**<mark>CONFIDENTIAL</mark> PRELIMINARY** 

© 2018 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_– EOS S3LV – Integration Guide Rev. 1.0_** 

### **Copyright and Trademark Information** 

Copyright © 2018 QuickLogic Corporation. All Rights Reserved. 

The information contained in this document is protected by copyright. All rights are reserved by QuickLogic Corporation. QuickLogic Corporation reserves the right to modify this document without any obligation to notify any person or entity of such revision. Copying, duplicating, selling, or otherwise distributing any part of this product without the prior written consent of an authorized representative of QuickLogic is prohibited. 

QuickLogic is a registered trademark, and the QuickLogic logo is trademark of QuickLogic. Other trademarks are the property of their respective companies. 

<u>www.quicklogic.com</u> **5** • • • ••• 

**<mark>CONFIDENTIAL</mark> PRELIMINARY** 

© 2018 QuickLogic Corporation 

