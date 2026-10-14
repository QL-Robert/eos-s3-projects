---
title: "FLL_I2S IP for EOS 3B"
source_file: "qorc-sdk/s3-gateware/ip_modules/FLL_I2S/docs/FLL_I2S_register_map.pdf"
pages: 9
sha256: 04aeea39e8122327ba8c88ba0affdb1063f545918579ec7eb90c61e76c12c82a
---

# FLL_I2S IP for EOS 3B

# FLL_I2S FPGA IP 

_Revision: 1.01 Date: 13 Nov 2020_ 

## _QuickLogic Corporation_ 

FLL_I2S IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 1_** 

### **1 Theory of Operation** 

The FLL_I2S IP module is a simple Frequency-Locked Loop controller. It can be used to detect frequency differences between a local clock (slave) and an external clock (master). Based on the frequency difference, if any, the FLL_I2S IP module will generate interrupts to the M4 processor in the S3 device so that the local clock speed can be adjusted. This enables the S3 device to be used as an I2S slave, and synchronize its local (slave) clock to the external (master) clock. 

Note that the S3’s high-speed internal oscillator will be locked to its own local 32.768KHz oscillator. Therefore, it cannot be locked to an external I2S master’s clock. However, the local high-speed clock can be digitally controlled, manually, by software running in the S3 device. By using interrupts coming from this FLL_I2S IP module, the M4 software can adjust its own local clock to match an external clock source. 

This IP module contains a few control registers. There is a Control register that can be activated to turn on the FLL. There is a Sample Time register that can be used to control the length of time (in local clock periods) over which the clock speed measurements are made. There is also a Gap Timer that can be used to control the length of time (in local clock periods) between each sample. 

Once enabled, the FLL will count down from the Sample Time register value, to zero, in the local clock domain. Simultaneously it will count down from the Sample Time register value in the external (master) clock domain. Once the sample period is over, the count value in the external (master) clock domain will indicate whether the external clock domain is faster, slower, or the same as the local clock (the master count value will be a negative number, a positive non-zero number, or equal to zero, respectively). The Gap counter will then count down from the Gap Timer value, to zero. Once the Gap counter reaches zero, another sample will be initiated, and the process will repeat until the FLL is disabled. 

Simultaneous to the above, an I2S word count will be maintained in both the local and external clock domains. The I2S Word Size is a parameter in the IP module (default value = 64), which can be overridden if needed when the module is instantiated. Depending on the relative clock speeds, the word counts in each clock domain may be the same, or different, over time. The FLL control logic will compare the word counts between the two clock domains, as well as the relative clock speeds as shown by the Sample Counters described in the previous paragraph, and determine if it needs to generate a “speed up” interrupt, a “slow down” interrupt, or neither. Therefore, the FLL will try to maintain the same word count in each clock domain while also matching the local clock frequency to the external clock frequency. 

Note that software running in the M4 processor only needs to respond to the “speed up” or “slow down” interrupts by adjusting the local bit clock up or down, respectively. It is recommended that the default values for the Sample Timer and Gap Timer be used, until the user becomes sufficiently familiar with the behavior of the FLL. For example, setting one or both of these timer values to very small numbers could result in very frequent interrupts as the FLL tries to lock on to the external clock, which would flood the M4 processor with interrupts. On the other hand, using values that are too large would slow down the locking process and may prevent a lock from happening. 

FLL_I2S IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 3_** 

### **2 Address Map Specification** 

#### **2.1 Memory Map** 

The EOS 3B system maps the FPGA IP into the address range of 0x40020000 to 0x4003FFFF. This address range provides 128K bytes of address range for FPGA based IP. Each instantiation of this FLL_I2S IP module should be allocated a base address within the FPGA’s address space. The register offsets described in this document are all relative to the FLL_I2S IP’s base address that you have chosen for your design. The FLL_I2S  IP module currently uses 256 bytes of address space, although this address space may not be fully utilized. 

##### **2.1.1 FLL_I2S Address Table** 

Table 1 shows the allocation of the FLL_I2S module’s address space. 

**Table 1: FLL_I2S Register Table** 

|Register|Register Name|Reset Value|Description|
|---|---|---|---|
|0x00|Control Register|0x0|Enable bit to turn on the<br>FLL.|
|0x04|Sample Time|0x0400|Number of local clock<br>periods per sample.|
|0x08|Gap Timer|0x0400|Number of local clock<br>periods between samples.|
|0x0C|Word Count Difference<br>[DEBUG]|N/A|Local_wordcount –<br>Master_wordcount|
|0x10|Local & Master Word<br>Counts (lower bits only)<br>[DEBUG]|N/A|{Local_wordcount[15:0],<br>Master_wordcount[15:0]}|
|0x14|Master_wordcount<br>[DEBUG]|N/A|Master_wordcount[31:0]|
|0x18|Local_wordcount<br>[DEBUG]|N/A|Local_wordcount[31:0]|
|0x1C|Master Sample Count<br>[DEBUG]|N/A|Master Sample Count|
|0x20 –<br>0xFF|Reserved|0x0||



#### **2.2 Description of Registers** 

The following sections will detail the registers for the FLL_I2S IP module. 

##### **2.2.1 Conventions** 

|**Access Tag**|**Name**|**Meaning**|
|---|---|---|
|R|Read|field may be read by the user/sw|
|W|Write|field may be written by the user/sw|
|U|Update|field may be updated by hardware|
|S|Set|field may be set by the user|
|C|Clear|field may be cleared by the user|
|RO|Read Only|field can only be read by the user/sw|



##### **2.2.2 FLL_I2S Registers** 

##### **_2.2.2.1 [0x00] Control Register_** 

Bit 0 of this register allows the FLL to operate. Other bits are reserved. 

**Table 2: Control Register** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
|CONTROL[0]|[0]|R/W|FLL Enable. 1=enabled, 0=disabled.<br>Reset value=0.|
|CONTROL[31:1]|[31:1]|RO|Reserved.|



##### **_2.2.2.2 [0x04] Sample Time_** 

This register specifies the length of time, in local clock periods, per sample. During the sample time, the number of clocks in the external clock domain will be counted to determine if the two clock domains are frequency locked, or not. 

**Table 3: Sample Time** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
|SAMPLE_TIME[31:0]|[31:0]|R/W|Sample Time, specified in local clock periods.<br>Resetvalue=0x0400.|



FLL_I2S IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 5_** 

##### **_2.2.2.3 [0x08] Gap Timer_** 

This register specifies the length of time, in local clock periods, between samples. 

**Table 4: Gap Timer** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
|GAP_TIMER[31:0]|[31:0]|R/W|Gap Timer, specified in local clock periods.<br>Reset value=0x0400.|



##### **_2.2.2.4 [0x0C] Word Count Difference [DEBUG]_** 

This is a DEBUG register, used to help verify the FLL IP, and as such, may be removed in the future to reduce the size of the FLL IP. This register shows the difference between the Local Word Count and the Master Word Count (Local_wordcount – Master_wordcount), for the previous sample period. By default, 64 bit clocks equals 1 word clock (this is a parameter in the IP module, which may be modified when the module is instantiated). This register is updated after each sample period. 

**Table 5: Word Count Difference [DEBUG]** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
|WORDCOUNT_DIFF[31:0]|[31:0]|RO|Word Count Difference, Local_wordcount –<br>Master_wordcount.|



##### **_2.2.2.5 [0x10] Local & Master Word Counts (lower bits only) [DEBUG]_** 

This is a DEBUG register, used to help verify the FLL IP, and as such, may be removed in the future to reduce the size of the FLL IP. This register shows the lower 16 bits of the Local and Master Word counts, for the previous sample period. This register is updated after each sample period. 

**Table 6: Local & Master Word Counts (lower bits only) [DEBUG]** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
|WORDCOUNT_LOWERBITS[31:0]|[31:0]|RO|WORDCOUNT_LOWERBITS[31:16] =<br>Local_wordcount[15:0].<br>WORDCOUNT_LOWERBITS[15:0] =<br>Master_wordcount[15:0].|



##### **_2.2.2.6 [0x14] Master Word Count [DEBUG]_** 

This is a DEBUG register, used to help verify the FLL IP, and as such, may be removed in the future to reduce the size of the FLL IP. This register shows the Master Word count (the word count in the external/master clock domain), for the previous sample period. This register is updated after each sample period. 

**Table 7: Master Word Count [DEBUG]** 

|**Name**<br>MASTER_WORDCOUNT[31:0]|**Bit(s)**<br>[31:0]|**Type**<br>RO|**Description**<br>Master_wordcount[31:0].|
|---|---|---|---|



##### **_2.2.2.7 [0x18] Local Word Count [DEBUG]_** 

This is a DEBUG register, used to help verify the FLL IP, and as such, may be removed in the future to reduce the size of the FLL IP. This register shows the Local Word count (the word count in the local clock domain), for the previous sample period. This register is updated after each sample period. 

**Table 8: Local Word Count [DEBUG]** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
|LOCAL_WORDCOUNT[31:0]|[31:0]|RO|Local_wordcount[31:0].|



##### **_2.2.2.8 [0x1C] Master Sample Count [DEBUG]_** 

This is a DEBUG register, used to help verify the FLL IP, and as such, may be removed in the future to reduce the size of the FLL IP. This register shows the Master Sample count (the sample count in the external/master clock domain), for the previous sample period. This register is updated after each sample period. Note that the Local Sample Count will always be zero after each sample time, as it counts down from the Sample Time value (register 0x04) to zero. Depending on the relative speeds of the local and master bit clocks, the Master Sample Count will either be slightly positive, zero, or slightly negative. 

**Table 9: Master Sample Count [DEBUG]** 

|**Name**<br>MASTER_SAMPLE_COUNT[31:0]|**Bit(s)**<br>[31:0]|**Type**<br>RO|**Description**<br>Master_sample_count[31:0].|
|---|---|---|---|



FLL_I2S IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 7_** 

### **3 Revision History** 

|**Date**|**Revision**|**Author**|**Description**|
|---|---|---|---|
|03 Nov 2020|1.00|Randy O|Initial Release|
|13 Nov 2020|1.01|Randy O|Added debug registers and added more<br>explanation to the Theoryof Operation.|



- **4 Copyright and Trademark Information** 

_All trademarks and / or trade names are property of their respective owners._ 

_The information in this specification has been carefully reviewed for technical accuracy. However, QuickLogic does not take the responsibility for the accuracy of the included information. Quicklogic will not be held  liable for damages which result from relying on the accuracy of the information contained in this specification. This specification is subject to change without notification._ 

_If you find any errors or require additional explanation, please inform Quicklogic.  All trademarks and / or trade names are property of their respective owners._ 

_Copyright © 2020 QuickLogic_ 

_All rights reserved._ 

_QuickLogic Corporation 2220 Lundy Ave. San Jose CA. 95131, USA_ 

FLL_I2S IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 9_** 

