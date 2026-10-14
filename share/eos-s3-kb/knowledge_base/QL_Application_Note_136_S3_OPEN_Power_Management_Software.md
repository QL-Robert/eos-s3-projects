---
title: "QuickLogic\u00ae S3 OPEN \u2013 Power Management Software"
source_file: "QL Application Note 136 \u2013 S3 OPEN \u2013 Power Management Software.pdf"
pages: 13
sha256: 8618cd279cc0ceb1ff15e14eb6e808de2d913f8ed56999fca409933256edc966
---

# QuickLogic® S3 OPEN – Power Management Software

## **QuickLogic**<sup>**®**</sup> **S3 OPEN – Power Management Software** 

**• • • • • • QuickLogic**<sup>**®**</sup> **Application Note 136** 

### **Introduction** 

The S3 power management software stack consists of different modules. These modules are designed to use S3 capability to run various functions in the most power-efficient way. 

**Figure 1** shows a block diagram of the power management software stack. 

Figure 1: Power Management Software Stack 



<!-- Start of picture text -->
User Driver<br>Clock Application Programming Interface (API)<br>Clock Framework Internal<br>Power Island (PI) Framework<br>eee Quality of Service (QoS) Framework<br>Dynamic Frequency Scaling (DFS) Framework<br>[Lo<br>Idle Framework<br>LPM Handler Device PM CB<br>—<br><!-- End of picture text -->

# **<mark>PRELIMINARY</mark>** 

<u>www.quicklogic.com</u> **1** ••• ••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Power Management Software Rev. 2017.3.1_** 

#### **Clock API** 

The clock API provides a clock ID-based simple interface layer for applications or user drivers and acts as an entry point to the power management stack. Refer to the _QuickLogic S3 OPEN – Clock Framework HAL API Reference Manual_ for more information about the available API. 

#### **Clock Framework** 

The clock framework handles clock state and frequencies of the different clock domain. Based on clock ID value, the clock framework derives the clock domain and clock gate mask, which is used to update the clock status. 

#### **Power Island Framework** 

Power island framework puts the power islands into a programmable low power state, which can be a Retention or Shutdown state to reduce power consumption. Power island framework uses the clock framework to determine if power island needs to be put into low power mode (LPM). 

#### **Dynamic Frequency Scaling Framework** 

DFS changes frequency runtime based on system load. The objective is to run the system at optimum frequency to reduce dynamic power consumption. 

#### **Quality of Service Software Framework** 

With the DFS algorithm in place, system frequencies can change dynamically at a very fast rate based on system load conditions. QoS framework ensures minimum clock frequency requested for a clock, which is required for any IP block for its stable operations, irrespective of DFS node frequencies. 

#### **Device Power Management Framework** 

When the system goes into Idle mode, the systems static power consumption can be reduced by putting M4 as well as all peripheral devices into low power mode. The device power management framework provides callback to drivers when going into or coming out of low power mode. 

**2** <u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Power Management Software Rev. 2017.3.1_** 

### **Writing Driver/Application on Top of the S3 Power Management Software Stack** 

The S3 power management stack is designed to work in the lowest power configuration, it initializes only the required clocks with default clock rates and not all clocks are enabled (see **Init Configuration of Clock Domains** on page 9 for default configuration). The driver/application writer must ensure that the clock of the subsystem being used is in the enabled state with the required clock rate. The driver must disable the clock as soon as it is done, since keeping an unused clock enabled uses power. 

#### **Enabling a Required Clock** 

A clock can be enabled by passing the clock ID to the hardware application layer (HAL) application programming interface (API). 

ret = S3x_Clk_Enable (S3X_M4_PRPHRL_CLK); if (ret == STATUS_OK) printf(“Uart clock is enabled\n”); 

Use this function call to enable the UART peripheral Clock Gate. Check the return value to confirm the clock is enabled. Enabling the clock increases the use count of the clock ID by one. 

#### **Disabling a Required Clock** 

A clock can be disabled by passing the clock ID to the HAL API. 

ret = S3x_Clk_Disable (S3X_M4_PRPHRL_CLK); if (ret == STATUS_OK) printf(“Uart clock is disabled\n”); 

Use this function to disable a Clock Gate. Disabling a Clock decreases the use count of the clock ID by one. The clock is disabled only after its use count reaches a value of 0. If there is more than one user of a clock, the clock will get disabled only when both of the users have disabled it. 

#### **Changing the Clock Rate** 

The S3 software initializes all clocks with default rates. Use the following API to change clock rate. 

ret = S3x_Clk_Set_Rate (S3X_M4_PRPHRL_CLK, HSOSC_3MHZ); if (ret == STATUS_OK) printf(“Uart clock is updated\n”); 

This function is used to set the Clock Gate at the desired rate. It sets the rate for the corresponding Clock Domain. Thus, all paths emerging from a clock domain are set to the same rate. 

• • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2017 QuickLogic Corporation 

<u>www.quicklogic.com</u> **3** 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Power Management Software Rev. 2017.3.1_** 

#### **Reading the Current Clock Rate** 

To read back the clock rate of a clock use the following API call. 

rate = S3x_Clk_Get_Rate (S3X_M4_PRPHRL_CLK); printf(‘Uart clock rate is %d\n”, rate); 

This function returns the clock rate value in Hz. 

#### **Reading the Current Use Count** 

To read the use count of a clock use the following API call. 

ret = S3x_Clk_Get_Usecnt (S3X_M4_PRPHRL_CLK); printf(‘Uart clock use count is %d\n”, ret); 

#### **QoS Framework** 

The DFS changes the CPU clock and its dependent clock dynamically, and based on highest required clock in a DFS node, the High Speed Oscillator (HSOSC) clock is updated to the highest required value. To ensure minimum frequency for its clock, CPU clock or HSOSC clock, the driver can register with QoS framework. Using QoS node to restrict minimum frequency can increase power consumption, therefore ensure that it uses QoS request only when it is required, and releases it as soon as possible. 

For example, Audio task uses QoS node to restrict the minimum value of CPU frequency to 18 MHz while Audio streaming and clears it when streaming is stopped from the application processor (AP). 

For every clock domain, there can be only one QoS node, and each QoS node can set three different types of requests (MIN_HSOSC_FREQ, MIN_CPU_FREQ and MIN_OP_FREQ). If the same request is made multiple times it will get overwritten with the newest value. However, the user can use multiple requests of a different type. As an example, the user can make a request for MIN_OP_FREQ while MIN_CPU_FREQ is already active for the same clock domain. 

/* registering to QoS for C30 Clock domain, required only once */ S3x_Register_Qos_Node (S3X_PDM_LEFT); /* Start Audio streaming, ensure CPU always to 18 MHZ during streaming */ S3x_Set_Clkd_Qos_Req (S3X_PDM_LEFT, MIN_CPU_FREQ, HSOSC_18MHZ); /* Done with Audio streaming */ S3x_Clear_Qos_Req (S3X_PDM_LEFT, MIN_CPU_FREQ); 

**4** <u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Power Management Software Rev. 2017.3.1_** 

#### **Registering to Peripheral Power Management** 

To use Peripheral Power Management, the user driver must register its callback function, which is called during entry and exit from LPM. 

/* Device LPM function Pseudo code */ Static int mydevice_Lpm_Callback( int state) { int ret = 0; if (state == ENTER_LPM) { /* System is about to enter LPM do minimum required function, such as disable clock, Stop IP, etc. to put device on LPM */ my_device_enter_lpm(); } else if (state == EXIT_LPM) { /* System is exiting from LPM, restore required things enable back clock, restore register if required */ my_device_exit_lpm(); } return ret; } /* registering with Peripheral Power Management */ s3x_Register_Lpm_Cb (mydevice_Lpm_Callback, “MY_DEV_NAME”); 

<u>www.quicklogic.com</u> **5** • • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Power Management Software Rev. 2017.3.1_** 

#### **DFS Configuration** 

DFS configuration is defined in the dfs_node[] structure array file App/Power/s3x_pwrcfg.c. The following example shows the current DFS configuration for C01, C09, C10 and C08X4 clock domains. DFS frequency for clock domain in a node can be changed by updating the .rate value for the corresponding clock domain id in the .clk_domain field. 

S3X_Policy_Node dfs_node[] = { /* 0th Policy is only for lpm not for run mode */ [0] = { .clk_domain = {CLK_C01, CLK_C09, CLK_C10, CLK_C08X4}, .rate = {C01_N0_CLK, C09_N0_CLK, C10_N0_CLK, C8X4_N0_CLK}, .step_width = 0, /* msec */ }, [1] = { .clk_domain = {CLK_C01, CLK_C09, CLK_C10, CLK_C08X4}, .rate = {C01_N1_CLK, C09_N1_CLK, C10_N1_CLK, C8X4_N1_CLK}, .step_width = STEP_1, /* msec */ }, [2] = { .clk_domain = {CLK_C01, CLK_C09, CLK_C10, CLK_C08X4}, .rate = {C01_N2_CLK, C09_N2_CLK, C10_N2_CLK, C8X4_N2_CLK}, .step_width = STEP_2, /* msec */ }, [3] = { .clk_domain = {CLK_C01, CLK_C09, CLK_C10, CLK_C08X4}, .rate = {C01_N3_CLK, C09_N3_CLK, C10_N3_CLK, C8X4_N3_CLK}, .step_width = STEP_3, /* msec */ }, [4] = { .clk_domain = {CLK_C01, CLK_C09, CLK_C10, CLK_C08X4}, .rate = {C01_N4_CLK, C09_N4_CLK, C10_N4_CLK, C8X4_N4_CLK}, .step_width = STEP_4 /* msec */ } } 

**6** <u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Power Management Software Rev. 2017.3.1_** 

The value of DFS configuration macros are declared in App/Power/Inc/s3x_pwrcfg.h, as shown in the following example. 

#define C01_N0_CLK HSOSC_1MHZ #define C09_N0_CLK HSOSC_512KHZ #define C10_N0_CLK HSOSC_1MHZ #define C8X4_N0_CLK HSOSC_1MHZ #define C01_N1_CLK HSOSC_3MHZ #define C09_N1_CLK HSOSC_1MHZ #define C10_N1_CLK HSOSC_18MHZ #define C8X4_N1_CLK HSOSC_1MHZ #define STEP_1 500 #define C01_N2_CLK HSOSC_3MHZ #define C09_N2_CLK HSOSC_2MHZ #define C10_N2_CLK HSOSC_36MHZ #define C8X4_N2_CLK HSOSC_1MHZ #define STEP_2 500 #define C01_N3_CLK HSOSC_3MHZ #define C09_N3_CLK HSOSC_3MHZ #define C10_N3_CLK HSOSC_48MHZ #define C8X4_N3_CLK HSOSC_1MHZ #define STEP_3 500 #define C01_N4_CLK HSOSC_6MHZ #define C09_N4_CLK HSOSC_6MHZ #define C10_N4_CLK HSOSC_72MHZ #define C8X4_N4_CLK HSOSC_1MHZ 

<u>www.quicklogic.com</u> **7** • • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Power Management Software Rev. 2017.3.1_** 

#### **Power Island Configuration** 

To set the LPM of an individual Power Island, configure the cfg_state variable in the S3Pi [] structure array defined in file App/Power/s3x_pwrcfg.c. cfg_state can be set to any of these three states PI_SET_DS, PI_SET_SHDN and PI_NO_CFG based on the required LPM of the Power Island. 

S3x_Pi S3Pi [] = { [PI_A1] = { .name = “A1”, .pctrl = PI_CTRL(0xd0, 0xd4, 0x208, 0x0218, 1, 0x40, 0x40), .ginfo = PI_GINFO(2, S3X_CFG_DMA_A1_CLK, S3X_A1_CLK, 0, 0, 0), .cfg_state = PI_SET_SHDN, } [PI_I2S] = { .name = “I2S_S”, .pctrl = PI_CTRL(0xe0, 0, 0x208, 0x0218, 0x10, 0x20, 0x20), .ginfo = PI_GINFO(1, S3X_I2S_A1_CLK, 0, 0, 0, 0), .cfg_state = PI_SET_SHDN, } [PI_EFUSE] = { .name = “EFUSE”, .pctrl = PI_CTRL(0xe0, 0x208, 0x0218, 0x4, 0x4, 0x4), .ginfo = PI_GINFO(2, S3X_EFUSE_01_CLK, S3X_EFUSE_02_CLK, 0, 0, 0), .cfg_state = PI_SET_SHDN, } [PI_FFE] = { .name = “FFE”, .pctrl = PI_CTRL(0x90, 0x94, 0x2008, 0x0210, 1, 1, 1), .ginfo = PI_GINFO(3, S3X_FFE_X4_CLK, S3X_FFE_X1_CLK, S3X_FFE_CLK,0, 0), .cfg_state = PI_SET_SHDN, } } 

**8** <u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Power Management Software Rev. 2017.3.1_** 

#### **Init Configuration of Clock Domains** 

Configure the init value of clock domains in an array S3clk [] defined in file App/Power/s3x_pwrcfg.c. In the following example the initial value for clock domain C10 is, clock rate at 72MHZ and clock gate mask as 0x5F with value ON. Similarly, for C02 clock domain, initial value for clock domain C02 is, clock rate at 3MHZ and clock gate mask as 0x7 with value OFF. 

S3x_ClkD S3clk [] = { [CLK_C10} = { .name = “C10”, .clkd_id = CLK_C10, .type = SRC_CLK, .sync_clk = SYNC_CLKD(2, CLK_C01, CLK_C09), .cru_crl = CRU_CTRL(0x0, 0x1fe, 9, 0x4, 0x50, 0x7f, 0), .flags = HW_GATED, .def_max_rate = HSOSC_DEF_RATE, .init_state = INIT_STATE(HSOSC_72MHZ, 0x5F, INIT_GATE_ON), } [CLK_C02} = { .name = “C2”, .clkd_id = CLK_C00, .type = SRC_CLK, .sync_clk = SYNC_CLKD(0, 0, 0), .cru_crl = CRU_CTRL(0x8, 0x1fe, 9, 0x130, 0x44, 0x7, 1), .def_max_rate = (HSOSC_40MHZ), .init_state = INIT_STATE(HSOSC_3MHZ, 7, INIT_GATE_OFF), } [CLK_C08x4} = { .name = “C8x4”, .clkd_id = CLK_C08x4, .type = SRC_CLK, .sync_clk = SYNC_CLKD(1, CLK_C08x1, 0), .cru_crl = CRU_CTRL(0x10, 0x1fe, 9, 0x134, 0x48, 0x1, 2), .def_max_rate = (HSOSC_40MHZ), .init_state = INIT_STATE(HSOSC_12MHZ, 0, 0), } [CLK_C11} = { .name = “C11”, .clkd_id = CLK_C11, .type = SRC_CLK, .sync_clk = SYNC_CLKD(0, 0, 0), .cru_crl = CRU_CTRL(0x14, 0x1fe, 9, 0x138, 0x54, 0x1, 3), .flags = LOCK_KEY, .def_max_rate = (HSOSC_12MHZ), #ifdef ENABLE_VOICE_SOLUTION .init_state = INIT_STATE(HSOSC_3MHZ, 0, 0), #else .init_state = INIT_STATE(HSOSC_3MHZ, 0, 0), #endif } 

**<mark>PRELIMINARY</mark>** 

• • • ••• 

© 2017 QuickLogic Corporation 

<u>www.quicklogic.com</u> **9** 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Power Management Software Rev. 2017.3.1_** 

### **Appendix** 

#### **Clock ID** 

**Table 1** lists the available clock path IDs, which can be passed as parameters to the HAL layer APIs. 

Table 1: Clock Gate Path IDs 

|**Path ID**|**Description**|
|---|---|
|**C01 clock gate (Path IDs)**||
|S3X_A0_01_CLK|A0|
|S3X_SDMA_SRAM_CLK|SDMA SRAM|
|S3X_PKT_FIFO_CLK|Packet FIFO|
|S3X_FFE_CLK|FFE clock from C01|
|S3X_CFG_DMA_A1_CLK|CFG DMA bridge inside A1 / AHB2APB bridge|
|S3X_I2S_A1_CLK|I<sup>2</sup>S module inside A1|
|S3X_SDMA_CLK|SDMA|
|S3X_EFUSE_01_CLK|eFuse clock from C01|
|S3X_SPT_CLK|SPT|
|**C02 clock gate (Path IDs)**||
|S3X_A1_CLK|A1 including CFGSM|
|S3X_FB_02_CLK|FB clock from C02|
|S3X_EFUSE_02_CLK|eFuse clock form C02|
|**C08 X4 clock gate (Path IDs)**||
|S3X_FFE_X4_CLK|FFE X4 clk|
|**C08 X1 clock gate (Path IDs)**||
|S3X_FFE_X1_CLK|FFE X1 clk|
|S3X_A0_08_CLK|A0 clock from C08X1|
|S3X_ASYNC_FIFO_0_CLK|PF Async FIFO 0|
|**C9 clock gate (Path IDs)**||
|S3X_AUDIO_APB|Voice APB interface|
|S3X_CLKGATE_PIF|PIF|
|S3X_CLKGATE_FB|FB|
|**C10 clock gate (Path IDs)**||
|S3X_M4_BM_TB_CLK|M4 bus matrix and trace block|
|S3X_M4_S0_S3_CLK|M4 SRAM instance, M4S0~M4S3|
|S3X_M4_S4_S7_CLK|M4 SRAM instance, M4S4~M4S7|
|S3X_M4_S8_S11_CLK|M4 SRAM instance, M4S8~M4S11|
|S3X_M4_S12_S15_CLK|M4 SRAM instance, M4S12~M4S15|
|S3X_AUDIO_DMA_CLK|Audio DMA|



# **<mark>PRELIMINARY</mark>** 

© 2017 QuickLogic Corporation 

**10** <u>www.quicklogic.com</u> •• •••• 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Power Management Software Rev. 2017.3.1_** 

Table 1: Clock Gate Path IDs _(Continued)_ 

|**Path ID**|**Description**|
|---|---|
|S3X_SYNCUP_A0_AHB_CLK|Sync up on A0 and AHB interface of batching memory|
|**C11 clock gate (Path IDs)**||
|S3X_M4_PRPHRL_CLK|M4 peripherals - AHB/APB bridge, UART, WDT and timer|
|**C12 clock gate (Path IDs)**||
|**CS clock gate (Path IDs)**<br>||
|S3X_SWD_PIN_CLK|SWD clock from pin|
|**CU clock gate (Path IDs)**||
|**C16 clock gate (Path IDs)**<br>||
|S3X_FB_16_CLK|FB clock from C16|
|**C19 clock gate (Path IDs)**<br>||
|S3X_ADC_CLK|ADC|
|**C21 clock gate (Path IDs)**||
|S3XFB21CLK|FB (additional clock) from C21|
|___<br>**C30 C31 clock gate (Path IDs)**<br>|<br>|
|S3X_PDM_LEFT|PDM left clock|
|S3X_PDM_RIGHT|PDM right clock|
|S3X_I2S_MASTER|I<sup>2</sup>S master clock|
|S3X_LPSD|LPSD clock|



#### **Constraints While Setting Clock Rate** 

- The actual rate set for a clock can vary from the intended rate depending upon the current value of the source clock. Frame work sets the nearest achievable value which can be greater or less than intended, but within the maximum rate limit of the clock domain. 

- The HSOSC value changes based on the maximum value of rate in a DFS node, a change in HSOSC value can result in a change of the actual clock rate value of a domain. 

- Certain clock domains are sensitive to clock rate value, such as UART which is derived from clock ID S3X_M4_PRPHRL_CLK. The clock rate in DFS node values must be selected such that the clock rate of these sensitive domains are not affected. As an example, if the UART clock is set to a value of 2 MHz, the maximum value of rate in each DFS node will be an integer multiple of 2 MHz. 

<u>www.quicklogic.com</u> **11** • • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Power Management Software Rev. 2017.3.1_** 

### **Contact Information** 

Phone: (408) 990-4000 (US) +(44) 1932-21-3160 (Europe) +(886) 26-603-8950 (Taiwan) +(86) 139-0517-5302 (China) +(81) 3-5875-0547 (Japan) +(82) 31-601-4225 (Korea) 

E-mail: <u>info@quicklogic.com</u> Sales: <u>America-sales@quicklogic.com Europe-sales@quicklogic.com Asia-sales@quicklogic.com Japan-sales@quicklogic.com Korea-sales@quicklogic.com</u> 

Support: <u>www.quicklogic.com/support</u> 

Internet: <u>www.quicklogic.com</u> 

### **Revision History** 

|**Revision**|**Date**<br>|**Originator and Comments**|
|---|---|---|
|2017.3.1|August 2017<br>Initial Release – Inderpal|Singh Saluja, Shubham Jangid and Kathleen Bylsma|



### **Notice of Disclaimer** 

QuickLogic is providing this design, product or intellectual property "as is." By providing the design, product or intellectual property as one possible implementation of your desired system-level feature, application, or standard, QuickLogic makes no representation that this implementation is free from any claims of infringement and any implied warranties of merchantability or fitness for a particular purpose. 

You are responsible for obtaining any rights you may require for your system implementation. QuickLogic shall not be liable for any damages arising out of or in connection with the use of the design, product or intellectual property including liability for lost profit, business interruption, or any other damages whatsoever. QuickLogic products are not designed for use in life-support equipment or applications that would cause a life-threatening situation if any such products failed. Do not use QuickLogic products in these types of equipment or applications. 

QuickLogic does not assume any liability for errors which may appear in this document. However, QuickLogic attempts to notify customers of such errors. QuickLogic retains the right to make changes to either the documentation, specification, or product without notice. Verify with QuickLogic that you have the latest specifications before finalizing a product design. 

**12** <u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Power Management Software Rev. 2017.3.1_** 

### **Copyright and Trademark Information** 

Copyright © 2017 QuickLogic Corporation. All Rights Reserved. 

The information contained in this document is protected by copyright. All rights are reserved by QuickLogic Corporation. QuickLogic Corporation reserves the right to modify this document without any obligation to notify any person or entity of such revision. Copying, duplicating, selling, or otherwise distributing any part of this product without the prior written consent of an authorized representative of QuickLogic is prohibited. 

QuickLogic is a registered trademark, and the QuickLogic logo is a trademark of QuickLogic. Other trademarks are the property of their respective companies. 

<u>www.quicklogic.com</u> **13** • • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2017 QuickLogic Corporation 

