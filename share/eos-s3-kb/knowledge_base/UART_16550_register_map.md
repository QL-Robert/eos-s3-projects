---
title: "UART IP for EOS 3B"
source_file: "qorc-sdk/s3-gateware/ip_modules/UART_16550/docs/UART_16550_register_map.pdf"
pages: 17
sha256: 2d55403c37b0057719d122f76c8200dad8f53756154fa5334381902daa856c70
---

# UART IP for EOS 3B

# UART 16550 FPGA IP 

_Revision: 1.01 Date: 29 Sep 2020_ 

## _QuickLogic Corporation_ 

UART IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 1_** 

### **1 Address Map Specification** 

#### **1.1 Memory Map** 

The EOS 3B system maps the FPGA IP into the address range of 0x40020000 to 0x4003FFFF. This address range provides 128K bytes of address range for FPGA based IP. Each instantiation of this UART IP should be allocated a base address within the FPGA’s address space. The register offsets described in this document are all relative to the UART IP’s base address(es) that you have chosen for your design. 

##### **1.1.1 UART Address Table** 

Table 1-1 shows the expected allocation of UART Register address space. This selection reflects the goal of backward compatibility with the UART 16550 commonly used for serial communications. 

**Table 1-1: UART Register Table** 

|Register|Register Name|Reset Value|Description|
|---|---|---|---|
|0x000|Receiver Buffer Register||Receive Data (Read Only)<br>_Note: Divisor Latch Access_<br>_Bit (DLAB) = “0”_|
|0x000|Transmit Buffer Register||Transmit Data (Write<br>Only)<br>_Note: Divisor Latch Access_<br>_Bit (DLAB) = “0”_|
|0x000|Divisor Latch (LSB)||Reference Clock divisor’s<br>LSB<br>_Note: Divisor Latch Access_<br>_Bit (DLAB) = “1”_|
|0x004|Interrupt Enable Register||Enables various interrupt<br>conditions.<br>_Note: Divisor Latch Access_<br>_Bit (DLAB) = “0”_|
|0x004|Divisor Latch (MSB)||Reference Clock divisor’s<br>MSB<br>_Note: Divisor Latch Access_<br>_Bit (DLAB) = “1”_|
|0x008|Interrupt Identification<br>Register||(Read Only)|
|0x008|FIFO Control Register||(Write Only)|
|0x00C|Line Control Register|||
|0x010|Modem Control Register|||



UART IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 3_** 

|Register|Register Name|Reset Value|Description|
|---|---|---|---|
|0x014|Line Status Register|||
|0x018|Modem Status Register|||
|0x01C|Scratch Register|0x00||
|0x020 –<br>0x7FF|Reserved|0x00||



#### **1.2 Description of Registers** 

The following sections will detail the registers for each address space. 

##### **1.2.1 Conventions** 

|**Access Tag**|**Name**|**Meaning**|
|---|---|---|
|R|Read|field may be read by the user/sw|
|W|Write|field may be written by the user/sw|
|U|Update|field may be updated by hardware|
|S|Set|field may be set by the user|
|C|Clear|field may be cleared by the user|
|RO|Read Only|field can only be read by the user/sw|



##### **1.2.2 UART Registers** 

##### **_1.2.2.1 Receive Buffer Register / Transmitter Holding Register_** 

Data received by the UART’s Rx logic may be read from this location. Data for transmission by the UART’s Tx logic should be written to this location. 

Note: These registers are only available if the “ _Divisor Latch Access Bit_ ” ( _DLAB_ ) of the Line Control Register (Ref. 0x00C) is set to “0”. 

Register Address location: 0x000 

Reset Value: 0x00 

**Table 3-4.1: Receive Buffer/Transmission Holding Register** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
|Receive Buffer|[7:0]|R|Receive Data from the Rx logic|
|Transmitter Holding|[7:0]|W|Data for transmission by the Tx logic.|
|Reserved|[31:8]|R|Returns “0”|



##### **_1.2.2.2 Divisor Latch (LSB) Register_** 

The Divisor Latch (LSB) register holds the lower byte of the reference clock divisor. 

Note: These registers are only available if the “ _Divisor Latch Access Bit_ ” ( _DLAB_ ) of the Line Control Register (Ref. 0x00C) is set to “1”. 

Register Address location: 0x000 

Reset Value: 0x00 

**Table 3-4.2: Divisor Latch (LSB) Register** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
|Divisor Latch (LSB)|[7:0]|R/W|Reference Clock divisor LSB byte.|
|Reserved|[31:8]|R|Returns “0”|



Baud rate calculation: 

The Divisor Latch Register (LSB, at offset 0x000) and Divisor Latch Register (MSB, at offset 0x004) are combined (concatenated) to form a single Divisor Latch value. This value is used to divide the system clock that drives the FPGA and the UART IP module, and therefore sets the UART’s operating speed. The baud rate is calculated using the following equation: 

Baud_Rate = Sys_Freq / [16 * (Divisor_Latch + 1)] 

Or, given a system clock frequency, the Divisor Latch value may be calculated as: 

Divisor_Latch = [Sys_Freq / (16 * Baud_Rate)] – 1 

In order to achieve a standard baud rate, it is advisable that the system frequency be a multiple of 1.8432 MHz. 

Example: In order to achieve a baud rate of 115,200 with a system clock rate of 7.3728 MHz, the Divisor Latch should be set to a value of 3, as follows: 

UART IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 5_** 

115200 = 7372800 / [16 * (3 + 1)] = 7372800 / 64 = 115200 

##### **_1.2.2.3 Interrupt Enable Register_** 

This register enables/disables various interrupt conditions. 

Note: These registers are only available if the “ _Divisor Latch Access Bit_ ” ( _DLAB_ ) of the Line Control Register (Ref. 0x00C) is set to “0”. 

Register Address location: 0x004 

Reset Value: 0x00 

**Table 3-4.3: Interrupt Enable Register** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
|Received Data|[0]|R/W|Enable Received Data Available Interrupt|
|Transmit Data|[1]|R/W|Enable Transmitter Holding Register Empty Interrupt|
|Receiver Line Status|[2]|R/W|Enable Receiver Line Status Interrupt|
|Modem Status|[3]|R/W|Enable Modem Status Interrupt|
|Reserved|[31:4]|R|Returns “0”|



##### **_1.2.2.4 Divisor Latch (MSB) Register_** 

The Divisor Latch (MSB) register holds the upper byte of the reference clock divisor. A description of how the Divisor Latch Register is used to calculate the UART baud rate, see the description of the Divisor Latch (LSB) Register, above. 

Note: These registers are only available if the “ _Divisor Latch Access Bit_ ” ( _DLAB_ ) of the Line Control Register (Ref. 0x00C) is set to “1”. 

Register Address location: 0x004 

Reset Value: 0x00 

**Table 3-4.4: Divisor Latch (MSB) Register** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
|Divisor Latch (MSB)|[7:0]|R/W|Reference Clock divisor MSB byte.|
|Reserved|[31:8]|R|Returns “0”|



##### **_1.2.2.5 Interrupt Identification Register_** 

The Interrupt Identification register returns the status of various interrupt sources. More specifically, this register provides the user with four interrupt status bits. Performing a read cycle on the Interrupt Identification register will provide the user with the highest pending interrupt level to be serviced. No other interrupts are acknowledged until the pending interrupt is serviced. Whenever the interrupt status register is read, the interrupt status is cleared. However, it should be noted that only the currently pending interrupt is cleared by the read. A lower level interrupt may be seen after re-reading the interrupt status bits. Table  shows the data values (bits [3:0] of the Interrupt Identification Register) for the four prioritized interrupt levels and the interrupt sources associated with each of these interrupt levels. 

**Table 3-4.5: Interrupt Sources** 

|**Priority**|**Bit [3]**|**Bit [2]**|**Bit [1]**|**Bit [0]**|**Source of Interrupt**|
|---|---|---|---|---|---|
|-|0|0|0|1|None|
|1|0|1|1|0|Receiver Line Status Register|
|2|0|1|0|0|Received Data Ready|
|2|1|1|0|0|Received Data Time-Out|
|3|0|0|1|0|Transmitter Holding Register Empty|
|4|0|0|0|0|Modem Status Register|



Register Address location: 0x008 

Reset Value: 0x00 

**Table 3-4.5a: Interrupt Identification Register** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
|Interrupt Pending|[0]|R|“0” when an interrupt is pending (i.e. Bit[0] inTable)|
|Interrupt ID|[3:1]|R|Selects interrupt sources (i.e. Bit [3:1] inTable)|
|Reserved|[4]|R|Returns “0”|
|512 Byte FIFO<br>Enabled|[5]|R|Enable Modem Status Interrupt|
|FIFOs Enabled|[7:6]|R||
|Reserved|[31:8]|R|Returns “0”|



UART IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 7_** 

##### **_1.2.2.6 FIFO Control Register_** 

The FIFO Control register enables the FIFO operation of the UART. 

Register Address location: 0x008 

Reset Value: 0x00 

**Table 3-4.6: Interrupt Identification Register** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
|FIFO Enable|[0]|W|Enables FIFO operations<br>0 – FIFOs Disabled<br>1–FIFOs Enabled|
|Receive FIFO Reset|[1]|W|Selects interrupt sources|
|Transmit FIFO Reset|[2]|W|Returns “0”|
|DMA Mode Select|[3]|W|Enable the use of the Tx Ready and Rx Ready signals in<br>conjunction with the each FIFO operation.|
|Reserved|[4]|W||
|512 FIFO Enabled|[5]|W|Enables extended FIFO operation<br>0 – 16-Byte Mode<br>1–512 Byte Mode|
|Receive Trigger|[7:6]|W|Selects the FIFO level for trigging an interrupt<br>Refer toTable.|
|Reserved|[31:8]|R|Returns “0”|



**Table 3-4.6a: RX FIFO Trigger Level Selection** 

|**FCR[7]**|**LCR[6]**|**RX FIFO Trigg**<br>**16-Byte Operation**|**er Levels (Bytes)**<br>**512-Byte Operation**|
|---|---|---|---|
|0|0|1|1|
|0|1|4|128|
|1|0|8|256|
|1|1|14|496|



##### **_1.2.2.7 Line Control Register_** 

Register Address location: 0x00C Reset Value: 0x00 

**Table3-4.7: Line Control Register** 

|**Name**<br>Word Length Select|**Bit(s)**<br>[1:0]|**Type**<br>R/W|**Description**<br>Word Length|
|---|---|---|---|



||||These two bits specify the word length to be transmitted or<br>received. (Refer toTable)|
|---|---|---|---|
||||<br>Stop Bit(s)|
|Number of Stop Bits|[2]|R/W|The length of Stop bits is specified by this bit in<br>conjunction with the word length. (Refer toTable)<br>|
|Parity Enable|[3]|R/W|Parity Enable<br>0 – No Parity<br>1 – A parity bit is generated during the transmission,<br>receiver checks the data and parity for transmission<br>errors.|
||||Even parity.<br>If the parity bit is enabled with LCR[3] set to a logic 1,<br>LCR[4] selects the even or odd parity format. (Refer to<br>Table)|
|Even Parity Select|[4]|R/W|0 – Odd parity is generated by forcing an odd number<br>of logic 1s in the transmitted data. The receiver<br>must be programmed to check the same format<br>(normal default condition).<br>1 – Even parity is generated by forcing an even number<br>of<br>logic 1s in the transmitted data. The receiver must be<br>programmed to check the same format.|
|Stick Parity|[5]|R/W|Set parity.<br>If the parity bit is enabled, LCR[5] selects the forced parity<br>format. (Refer toTable)<br>Programs the parity conditions as follows:<br>0 – parity is not forced (normal default condition)<br>LCR[5] – logic 1 and LCR[4] = logic 0: parity bit is forced<br>to a logic 1 for the transmit and receive data<br>LCR[5] – logic 1 and LCR[4] = logic 1: parity bit is forced<br>to a logic 0 for the transmit and receive data|
|Break Control|[6]|R/W|Set Break.<br>When enabled, the Break control bit causes a break<br>condition to be transmitted (the TX output is forced to a<br>logic 0 state). This condition exists until disabled by setting<br>LCR[6] to a logic 0.<br>0 – no TX break condition (normal default condition)<br>1 – forces the transmitter output (TX) to a logic 0 for<br>alerting the remote receiver to a line break condition|
||||Divisor latch enable.|
|Divisor Latch Access<br>Bit|[7]|R/W|The internal baud rate counter latch and Enhanced<br>Feature mode enable.<br>0 – Divisor latch disabled (normal default condition)<br>1–Divisor latch and enhanced feature register enabled|
|Reserved|[31:8]|R|Returns “0”|



UART IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 9_** 

**Table 3-4.7a: Parity Selection** 

|**LCR[5]**|**LCR[4]**|**LCR[3]**|**Parity Selection**|
|---|---|---|---|
|X|X|0|No Parity|
|0|0|1|Odd Parity|
|0|1|1|Even Parity|
|1|0|1|Force Parity “1”|
|1|1|1|Force Parity “0”|



**Table 3-4.7b: Stop Bit Length** 

|**LCR[2]**|**Word Length (Bits)**|**Stop Bit Length (Bit Times)**|
|---|---|---|
|0|5, 6, 7, 8|1|
|1|5|1 ½|
|1|6, 7, 8|2|



**Table 3-4.7c: Word Length** 

|**LCR[1]**|**LCR[0]**|**Word Length (Bits)**|
|---|---|---|
|0|0|5|
|0|1|6|
|1|0|7|
|1|1|8|



##### **_1.2.2.8 Modem Control Register_** 

Register Address location: 0x010 

Reset Value: 0x00 

**Table 3-4.8: Modem Control Register** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
||||DTRn|
|Data Terminal Ready|[0]|R/W|0 – Force DTR output to a logic 1 (normal default<br>condition)<br>1–Force DTR output to a logic 0|
||||RTSn|
|Request To Send|[1]|R/W|0 – Force RTS output to a logic 1 (normal default<br>condition)<br>1–Force RTS output to a logic 0|
||||OUTn [1].|
|Out[1]|[2]|R/W|This bit is used in the Loopback mode only. In the<br>Loopback mode, this bit is used to write the state of the<br>modem RIn interface signal via OUTn [1].|
|Out[2]|[3]|R/W|OUTn[2], INT enable.<br>Used to control the modem DCD signal in the Loopback<br>mode.<br>0 – Set OUTn[2] to HIGH. In the Loopback mode, sets<br>OUTn[2] (DCDn) internally to a logic 1.<br>1 – Set OUTn[2] to LOW. In the Loopback mode, sets<br>OUTn[2] (DCDn) internally to a logic 0.|
|Loop|[4]|R/W|Loopback.<br>Enable the local Loopback mode (diagnostics). In this<br>mode the transmitter output (ROUT) and the receiver input<br>(RIN), CTSn, DSRn, DCDn, and RIn are disconnected<br>from the UART’s I/O pins. Internally the modem data and<br>control pins are connected into a loopback data<br>configuration. In this mode, the receiver and transmitter<br>interrupts remain fully operational. The Modem Control<br>Interrupts are also operational, but the interrupts’ sources<br>are switched to the lower four bits of the Modem Control.<br>Interrupts continue to be controlled by the IER register.<br>0 – Disable Loopback mode (normal default condition)<br>1–Enable local Loopback mode (diagnostics)|
||||AFE.|
|Flow Control Enable|[5]|R/W|This bit is the auto flow control enable. When this bit is set,<br>the auto flow control is enabled. Refer toTable|
|Reserved|[31:6]|R|Returns “0”|



UART IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 11_** 

**Table 3-4.8a: Flow Control Configuration** 

|**MCR[5] (AFE)**|**MCR[1] (RTSn)**|**Flow Configuration**|
|---|---|---|
|1|1|auto RTSn and CTSn enabled|
|1|0|auto CTSn only enabled|
|0|X|auto RTSn and CTSn disabled|



##### **_1.2.2.9 Line Status Register_** 

Register Address location: 0x014 Reset Value: 0x00 

**Table 3-4.9: Line Status Register** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
|Data Ready|[0]|R/W|Receive data ready.<br>0 – no data in receive holding register or FIFO (normal<br>default condition)<br>1 – data has been received and is saved in the receive<br>holding register or FIFO|
||||Overrun error.<br>0 – No overrun error (normal default condition)<br>1 – Overrun error.|
|Overrun Error|[1]|R/W|A data overrun error occurred in the receive shift register.<br>This happens when additional data arrives while the FIFO<br>is full. In this case, the previous data in the shift register is<br>overwritten. Note that under this condition, the data byte in<br>the receive shift register is not transferred into the FIFO,<br>therefore the data in the FIFO is not corrupted by the error.|
||||Parity error.<br>0 – No parity error (normal default condition)|
|Parity Error|[2]|R/W|1 – Parity error.<br>The receive character does not have correct parity<br>information and is suspect. In the FIFO mode, this error is<br>associated with the character at the top of the FIFO.|
||||Framing error.<br>0 – No framing error (normal default condition)|
|Framing Error|[3]|R/W|1 – Framing error.<br>The receive character did not have a valid stop bit(s). In<br>the FIFO mode, this error is associated with the character<br>at the top of the FIFO.|
|Break Interrupt|[4]|R/W|Break interrupt.<br>logic 0– No breakcondition(normaldefault condition)|



||||logic 1 – Break Condition<br>The receiver received a break signal (RX was a logic 0 for<br>one character frame time). In the FIFO mode, only one<br>break character is loaded into the FIFO.|
|---|---|---|---|
|Transmitter Holding<br>Register|[5]|R/W|THR empty.<br>This bit is the Transmit Holding Register Empty indicator.<br>This bit indicates that the UART is ready to accept a new<br>character for transmission. In addition, this bit causes the<br>UART to issue an interrupt to CPU when the THR interrupt<br>enable is set. The THR bit is set to a logic 1 when a<br>character is transferred from the transmit holding register<br>into the transmitter shift register. The bit is reset to a logic<br>0 concurrently with the loading of the transmitter holding<br>register by the CPU. In the FIFO mode, this bit is set when<br>the transmit FIFO is empty; it is cleared when at least 1<br>byte is written to the transmit FIFO.|
|Transmitter Empty|[6]|R/W|THR and TSR empty. This bit is the Transmit Empty<br>indicator. This bit is set to a logic 1 whenever the transmit<br>holding register and the transmit shift register are both<br>empty. It is reset to logic 0 whenever either the THR or<br>TSR contains a data character. In the FIFO mode, this bit<br>is set to logic 1 whenever the transmit FIFO and transmit<br>shift register are both empty.|
||||FIFO data error.<br>0 – No error (normal default condition)|
|Error in Receiver<br>FIFO.|[7]|R/W|1 – FIFO Data Error<br>At least one parity error, framing error or break indication<br>is in the current FIFO data. This bit is cleared when LSR<br>register is read.|
|Reserved|[31:8]|R|Returns “0”|



##### **_1.2.2.10 Modem Status Register_** 

Register Address location: 0x018 Reset Value: 0x00 

**Table 3-4.10: Modem Status Register** 

|**Name**|**Bit(s)**|**Type**|**Description**|
|---|---|---|---|
|Delta Clear To Send|[0]|R/W|ΔCTSn<br>logic 0 – no CTSn change (normal default condition)<br>logic 1 – the CTSn input to the UART has changed state<br>since the last time it was read. A modem Status<br>Interrupt will be generated.|
|Delta Data Set<br>Ready|[1]|R/W|ΔDSRn<br>logic 0 – no DSRn change (normal default condition)<br>logic 1–the DSRn input to the UART has changed state|



UART IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 13_** 

||||since the last time it was read. A modem Status<br>Interrupt will be generated.|
|---|---|---|---|
||||ΔRIn|
|Trailing Edge Ring<br>Indicator|[2]|R/W|0 – No RIn change (normal default condition)<br>1 – The RIn input to the UART has changed from a logic<br>0<br>to a logic 1. A modem Status Interrupt will be<br>generated.|
||||ΔDCDn<br>0 – No DCDn change (normal default condition)|
|Delta Data Carrier<br>Detect|[3]|R/W|1 – The DCDn input to the UART has changed state<br>since<br>the last time it was read. A modem Status Interrupt<br>will<br>be generated.|
||||Clear To Send. CTS.<br>CTSn functions as hardware flow control signal input if it is<br>enabled via MCR[5]. Flow control (when enabled) allows<br>starting and stopping the transmissions based on the|
|Clear To Send|[4]|R/W|external modem CTSn signal. A logic 1 at the CTSn pin<br>will stop UART transmissions as soon as the current<br>character has finished transmission. Normally, MSR[4] is<br>the complement of the CTSn input. However, in the<br>Loopback mode, this bit is equivalent to the RTSn bit in<br>the MCR register.|
||||Data Set Ready. DSR (active HIGH, logic 1).|
|Data Set Ready|[5]|R/W|Normally, this bit is the complement of the DSRn input. In<br>Loopback mode this bit is equivalent to the DTR bit in the<br>MCR register.|
||||Ring Indicator. RI (active HIGH, logic 1).|
|Ring Indicator|[6]|R/W|Normally, this bit is the complement of the RIn input. In the<br>Loopback mode, this bit is equivalent to the OUT [1] bit in<br>the MCR register.|
||||Data Carrier Detect. DCD (active HIGH, logic 1).|
|Data Carrier Detect|[7]|R/W|Normally this bit is the complement of the DCDn input. In<br>the Loopback mode this bit is equivalent to the OUT [2] bit<br>in the MCR register.|
|Reserved|[31:8]|R|Returns “0”|



### **2 Revision History** 

|**Date**|**Revision**|**Author**||**Description**|
|---|---|---|---|---|
|23 Sep 2020|1.00|Randy O|Initial Release||



UART IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 15_** 

- **3 Copyright and Trademark Information** 

_All trademarks and / or trade names are property of their respective owners._ 

_The information in this specification has been carefully reviewed for technical accuracy. However, QuickLogic does not take the responsibility for the accuracy of the included information. Quicklogic will not be held  liable for damages which result from relying on the accuracy of the information contained in this specification. This specification is subject to change without notification._ 

_If you find any errors or require additional explanation, please inform Quicklogic.  All trademarks and / or trade names are property of their respective owners._ 

_Copyright © 2020 QuickLogic_ 

_All rights reserved._ 

_QuickLogic Corporation 2220 Lundy Ave. San Jose CA. 95131, USA_ 

UART IP for EOS 3B 

**_www.quicklogic.com_** 

**_Page 17_** 

