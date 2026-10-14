---
title: "QuickLogic\u00ae S3 OPEN \u2013 Batching in Companion Mode"
source_file: "QL S3 OPEN - Batching in Companion Mode Application Note 133.pdf"
pages: 13
sha256: 7a41b286c9ed6a2f9ead80b3025a4553e8027cbaa1177fb91da72f31d7215ddf
---

# QuickLogic® S3 OPEN – Batching in Companion Mode

# **QuickLogic**<sup>**®**</sup> **S3 OPEN – Batching in Companion Mode** <mark>SS</mark> 

**• • • • • • QuickLogic Application Note 133** 

## **Overview** 

The S3 subsystem is a low power sensor processing platform designed to process sensor data collected from different sensors and run algorithms on that data. QuickLogic’s specialized fusion algorithms such as Pedometer, Gesture and Double Tap or the original equipment manufacturer’s (OEM’s) own algorithms can be run on the ARM M4F, or for greater power savings, on the Flexible Fusion Engine (FFE). 

Batching refers to storing sensor events in embedded RAM before reporting them to the algorithm processing unit, instead of reporting them immediately. Batching enables significant power savings by preventing the algorithm processing unit from waking up to receive each event. Instead, the events can be grouped and processed together. Thus, the processing unit can spend most of the time in low power mode, which provides a significant power savings. 

In the case of the S3, the batching process collects the different sensor data in the background without waking the M4. The FFE gets sensor data from the sensor manager (SM) and informs the M4 or an external application processor (AP) after the batching period finishes. 

## **S3 Functional and Module Description** 

### **Hardware** 

Batching in the S3 subsystem consists of the following hardware functional blocks: 

- AP 

- M4 

- FFE 

- SRAM 

- Packet FIFO 

- SPI Master/I<sup>2</sup> C Bus 

<u>www.quicklogic.com</u> **1** ••• ••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Batching in Companion Mode Rev. 1.1_** 

**Figure 1** shows a block diagram of the hardware for the S3 subsystem. 

Figure 1: S3 Block Diagram 



<!-- Start of picture text -->
S3<br>SRAM<br>Sensors<br>Application<br>Processor<br>Packet FIFO<br>Accelero-<br>SPI<br>M4 meter<br>FFE<br>I2C/SPI<br>M4 Subsystem<br>Gyro<br>Interrupt<br>Magneto-<br>meter<br><!-- End of picture text -->

##### **AP** 

The AP is connected to the S3 through the SPI Interface. In Companion mode, the AP is the Master and the S3 is the Slave. The algorithm is initiated by the AP to S3. The Host AP and the M4 processor communicate through a SPI interface. 

##### **M4** 

The M4 interfaces between the AP and the FFE for the batching process by providing following information to FFE: 

- The sampling frequency of the sensor 

- The memory location in SRAM where FFE should batch the sensor data 

- Number of samples that the FFE must batch (this is equal to = Sensor sampling freq * batching time in seconds) 

After providing this information M4 goes to sleep. When the FFE accumulates enough samples it sends an interrupt to wake up M4. 

##### **FFE** 

The FFE gathers and manages external sensor data with the I<sup>2</sup> C/SPI interface and stores the sensor data in a predefined packet format on the SRAM. Once the batching period expires or batching is explicitly terminated by M4, the FFE interrupts M4 and passes control information about the batched data in a predefined hardwarebased packet FIFO. 

**2** <u>www.quicklogic.com</u> •• •••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Batching in Companion Mode Rev. 1.1_** 

##### **SRAM** 

The SRAM acts as a storage area where the FFE stores packets and informs M4 for use later. For batching purposes, use the 128K SRAM always-on bank. The FFE assumes the buffer batching in SRAM is circular. The data format in SRAM depends on the particular sensor. 

For example, the accelerometer sensor format is as follows: 

||0<br>8<br>1|6<br>24<br>32|
|---|---|---|
||<br><br>|<br><br>|
|MemoryAddress|Data||
|buf_mem0|0|TimeStamp|
|buf_mem0 + 4|Packet Length|Accelerometer X-Component<br>(Ax_0)|
|buf_mem0 + 8|Accelerometer Y-Component (Ay_0)|Accelerometer Z-Component<br>(Az_0)|
|buf_mem0 + 12|0|TimeStamp|
|buf_mem0 + 16|Packet Length|Accelerometer X-Component<br>(Ax_1)|
|buf_mem0 + 20|Accelerometer Y-Component (Ay_1)|Accelerometer Z-Component<br>(Az_1)|
|buf_mem0 + 24|0|TimeStamp|
|buf_mem0 + 28|Packet Length|Accelerometer X-Component<br>(Ax_2)|
|buf_mem0 + 32|Accelerometer Y-Component (Ay_2)|Accelerometer Z-Component<br>(Az_2)|



##### **Packet FIFO** 

The FFE uses the Packet FIFO hardware interface to communicate event data to the M4 with a control packet. The FFE uses interrupts to generate an event to M4. On receipt of the interrupt, M4 goes into the packet FIFO to parse the packet. The packet format is defined as follows: 

|Word0(32Bits)|Word1(32Bits)|
|---|---|
|Sensor ID|*ptr SRAM Buffer|
|Number of Packets||



The data packet information is written from FFE to Always-On RAM as follows: 

||Timestamp (24bit)|
|---|---|
|Length|Accelerometer X-Component(Ax)|
|Accelerometer Y-Component(Ay)|Accelerometer Z-Component(Az)|



<u>www.quicklogic.com</u> **3** • • • ••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Batching in Companion Mode Rev. 1.1_** 

##### **SPI Master/I**<sup>**2**</sup> **C Bus** 

The FFE subsystem uses the S3 serial interface to communicate to the external sensor and collect data. The FFE programs the bus speed based on the sensor device capability. 

#### **AP and M4 Communication** 

The AP and M4 communicate through Mailbox1 and Mailbox 2. 

- In Case 1, the AP triggers the application by writing the required information to the Mailbox 1 and raises an interrupt through the SPI bus to M4. M4 reads the information in Mailbox 1, and process the data/algorithm in M4 or FFE. 

- In Case 2, the processed data from the sensors writes the information to Mailbox 2 and sends an interrupt to the AP to read the data in Mailbox 2. 

##### **Case 1:** 

**Figure 2** shows the method for storing batched data on a continuous allocated SRAM (i.e., batch size of 2 seconds). 

Figure 2: Storing Batched Data on a Continuous Allocated SRAM 



<!-- Start of picture text -->
Batch Start<br>Address<br>8<br>Batch Size<br>4 Sensors<br>Batch End<br>Application  Address<br>Accelero-<br>Processor<br>meter<br>1<br>Accelero-<br>2 Mailbox 1 3 FFE meter<br>M4<br>7 Subsystem<br>Mailbox 2 6 Packet FIFO 5<br><!-- End of picture text -->

**4** <u>www.quicklogic.com</u> •• •••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Batching in Companion Mode Rev. 1.1_** 

##### **Case 2:** 

**Figure 3** shows the method for storing batched data on a segmented SRAM (i.e., batch size of 2 seconds). 

Figure 3: Storing Batched Data on a Segmented SRAM 



<!-- Start of picture text -->
Batch End<br>Address<br>Batch Start<br>Address<br>8<br>Batch Size<br>4 Sensors<br>Application<br>Accelero-<br>Processor<br>meter<br>1<br>Accelero-<br>2 Mailbox 1 3 FFE meter<br>M4<br>7 Subsystem<br>Mailbox 2 6 Packet FIFO 5<br><!-- End of picture text -->

#### **Batching Actions and SRAM** 

##### **Batch On** 

The Batch On procedure for S3 is as follows: 

**1.** The AP loads the M4 Library and FFE Library for communication and acts as the Master. 

**2.** The AP sends a Batch On request to M4 instructs the FFE to start batching the sensor data by sending the batch size value (for example, 2 seconds). 

**3.** FFE receives the request and starts reading the required amount of real-time sensor data of the batch size specified by M4 into the Always-On SRAM. 

**4.** FFE prepares the event packet in the hardware Packet FIFO and sends an interrupt to M4. 

**5.** M4 reads the controlled information from the Packet FIFO and writes the control packet information into Mailbox 2. 

**6.** Mailbox 2 triggers an interrupt to the Host AP. 

**7.** The AP reads the controlled information from Mailbox 2 and starts reading the data from the SRAM in a circular buffer fashion. 

**NOTE:** The communication between the AP and S3 is through the SPI interface. 

• • • ••• 

© 2017 QuickLogic Corporation 

<u>www.quicklogic.com</u> **5** 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Batching in Companion Mode Rev. 1.1_** 

##### **Batch Off** 

The Batch Off procedure for S3 is similar to Batch On with the batch size = 1: 

**1.** M4 instructs the FFE to Batch Off the sensor data by sending the batch size value = 1 

**2.** FFE receives the Batch Off request and prepares the event packet and flushes the collected data packets from SRAM to M4. 

**3.** Then for every subsequent sensor read, the FFE prepares the control and data packet, sends an interrupt to M4 and writes this information to Mailbox 2, and raises an interrupt to AP. 

**4.** The AP reads the pack control size and number of packets in SRAM Mailbox 2 through the SPI read operation. 

#### **Batch Flush** 

The user can send the data flush command any time during batching to the FFE. When the Batch Flush command is received by the FFE, the data collected up to this point is flushed (i.e., the FFE generates a control packet to the packet FIFO and interrupts M4. Then the FFE continues with the batching process. 

The communication between M4 and the FFE is similar to the Batch On process, except in the Batch Flush case the data collected during intervals of batch size are flushed, and the new memory start address is reset to the new address for Batch On and continues to collect the data for the next Batch On sequence (see **Figure 4** ). 

Figure 4: SRAM Batch Flush Procedure 



<!-- Start of picture text -->
SRAM Memory SRAM Memory<br>Start Address M4/AP Starts Reading<br>of Sensor Data this Data<br>Sensor Data Sensor Data<br>Data Flush Batch Size New Start<br>Command Address Set<br>from M4/AP<br>Empty Real Sensor Data<br>from Sensors<br>SRAM Memory Information  SRAM Memory Information<br>During the Batch  While Consuming the<br>Flush Command Data Flushed by M4/AP<br><!-- End of picture text -->

**6** <u>www.quicklogic.com</u> •• •••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Batching in Companion Mode Rev. 1.1_** 

### **Software** 

This section describes the batching process implementation and the purpose of the different layers in the S3 subsystem. In the S3 subsystem the sensor fusion algorithms can be run in Host mode or Companion mode by selecting SPI Slave or SPI Master. 

Batching in the S3 subsystem consists of the following software functional blocks: 

- Application Layer 

- Sensor Framework 

- Sensor Driver 

- HAL 

- FFE Library 

The Sensor Framework is the interface layer between the Application Layer and the Sensor Driver. This framework interface is independent from the sensor driver implementation that various algorithms use to communicate with different sensors. This sensor framework contains the Sensor Abstraction Layer (SAL) to provide a uniform functionality to the application layer and Sensor Driver Framework (SDF) for a consistent interface with the real hardware, for further details refer to the _“QuickLogic S3 OPEN Sensor Framework Interface User Manual.”_ 

#### **Buffering the Sensor Data in the SRAM and Communicating to M4** 

While the M4 microcontroller unit (MCU) is in Sleep mode, and before it is interrupted, the buffering sensor data is stored according to a _userCompaniondefined_ period of time. The FFE is configured with the number of packets for buffering the sensor data, and based on that information the FFE stores the data to memory. The sensor data buffering is implemented in the SRAM in a circular buffer and the control data packets from FFE to M4 are routed using the packet FIFO of size two words. 

The AP passes the start address and total size of the SRAM, and M4 provides the AP information about the Packet FIFO in which the AP needs to read the sensor data from the SRAM (i.e., _*buf_ ). 

<u>www.quicklogic.com</u> **7** • • • ••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Batching in Companion Mode Rev. 1.1_** 

#### **Batch On/Off Sequence with Sensor Framework Application Programming Interfaces (APIs)** 

**Figure 5** illustrates the Batch On process sequence. 



<!-- Start of picture text -->
Figure 5: Batch On Process Sequence<br>EAB | dois<br>}——ese negtster_terine_trom<br>siave_iar)— Det<br>—seart_soubietsp_in_siave()——_pe!<br>(as 1_ine(sispt_ptae} >!<br>“QLMCU_Fw_Downioad(&siave_fw_image_infojm)<br>OLS? Lwete_so_Mam|sw_Ms_1_A098,‘Sensgsuriol<br>L wigge_inv_t0_s3_mev ><br>sas pecerceenttnenann, = =<br>SS ea te ae RE I aes eae parece oe sme)<br>M4 MCU into sleep Mode<br>Date Buffering to SRAM<br>with specific batch Size<br>‘Thefrommatmox packet contro!=  infowilbe reed as- Write-eo SRAMthe ColibackSensormemory ID,detaiisinterruptNo ofinpacketto PackesM4~ —andFIFO*Per = = |<br>Lets GeneseeBese55_weriassress,jecate, 3) "i<br>Hl<br>= cise_Reag_ss_Mamiacsress (wints_t*) |<br>&shared_Mem, sizeof (Shared_Mem)) Bt<br>GetsShe numbethe currentof packets batch adressmn the Baten ang H'1<br>PTs ae Ress, !<br>i<br>4 LSP _Write_s3_Mem 3<br>(address, (uints_t *}acata, a)<br>Ciews<br>me software Mailbox2 11<br>1<br><> = = = cear_int_trom_siavet) — —<br><!-- End of picture text -->



<!-- Start of picture text -->
8 www.quicklogic.com<br>•• ••••<br><!-- End of picture text -->

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Batching in Companion Mode Rev. 1.1_** 

#### **Initializing the SPI as a Master in the AP** 

**1.** Initialize the SPI as a Master in the AP by calling _QLSPI_init()._ 

**2.** Load the M4 and FFE firmware through a SPI write that provides the firmware information. 

**3.** Provide the shared memory start address and size to M4 through Mailbox 1. 

**4.** Start the double tap application request to M4 and raise the interrupt to S3 MCU. 

#### **Initializing the Sensor Framework** 

Initialize the sensor framework by calling the _QL_SensorFramework_Init()_ function which probes the sensor driver internally to get the sensor ID and check the number of sensors that are connected on the I<sup>2</sup> C/SPI bus. 

M4 to FFE communication is routed through the FFE interprocessor communication (IPC) library. This library is used by the Sensor Framework to communicate with the sensors/algorithms (composite sensors) connected/implemented to/in the FFE. 

#### **Processing the Request from AP by M4 and FFE** 

The FFE reads the real-time sensor data in a specific format, writes it to the SRAM, prepares the control packet events, and generates the event to M4 on Mailbox 2. M4 triggers the AP to get the SRAM information and reads it through _SPI_read()_ . 

<u>www.quicklogic.com</u> **9** • • • ••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Batching in Companion Mode Rev. 1.1_** 

**Table 1** shows an example algorithm (double tap) that uses the Sensor Framework API to get batched sensor data from the FFE. 

Table 1: Example Double Tap Algorithm 

|**QuickLogic Sensor**<br>**Framework API**|**Description**|
|---|---|
|QL_SensorFramework_Init()|This API initializes the Sensor Framework (i.e., it probes all of the available<br>sensors).|
|QL_SAL_SensorOpen(QL_SAL_Sen<br>sorHandle_t *handle, unsigned int id)|This API opens an instance of a sensor with a specified id. It returns handles<br>to the sensor instance. This handle is used for subsequent communication<br>with the sensor.|
||This API issues various commands to the Sensor Framework.<br>Typical commands include setting the sampling rate, registering call backs,<br>configuring memory for sensor data collection, setting the mode of data<br>collection (batch or normal mode), etc. For more information refer to the<br>_QuickLogic S3 OPEN Sensor Framework API_.|
|QL_SAL_SensorIoctl(QL_SAL_Sens<br>orHandle_t handle,unsigned int cmd,<br>void *arg);|The following commands are supported:<br>QL_SAL_IOCTL_REQ_EVENTS<br>QL_SAL_IOCTL_SET_SAMPLE_RATE<br>QL_SAL_IOCTL_ALLOC_DATA_BUF<br>QL_SAL_IOCTL_SET_DATA_BUF<br>QL_SAL_IOCTL_BATCH_ON<br>QL_SAL_IOCTL_START_DATA<br>QL_SAL_IOCTL_BATCH_FLUSH<br>QL_SAL_IOCTL_BATCH_OFF|
|QL_SAL_SensorRead(QL_SAL_Sen<br>sorHandle_t handle, void *buf, int<br>size);|This API sends a request to the Sensor Framework to get data<br>corresponding to a sensor.|
|QL_SAL_SensorClose(QL_SAL_Sen<br>sorHandle_t handle);|This API sends a request to the Sensor Framework to return a reference to<br>a sensor.|
|QLSPI_Init(&spi_plat)|This API initializes the SPI.|
|QLSPI_Register_Isr(intr_from_slave_<br>isr)|This API registers the ISR for the interrupt occurring from the slave side.|
|QLSPI_Write_S3_Mem(SW_MB_1_<br>ADDR,&msgBuf[0],4)|This API writes the message to the Mailbox 1.|
|QLSPI_Read_S3_Mem(address,<br>(uint8_t *)&data, 4)|This API reads the message from Mailbox 2.|



**10** <u>www.quicklogic.com</u> •• •••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Batching in Companion Mode Rev. 1.1_** 

**Figure 6** illustrates the Batch Off process sequence. 

Figure 6: Batch Off Process Sequence 



<!-- Start of picture text -->
bee Lice eed<br>[ase<br>—srect_soubietan_in_eave)|negister_teGines_from_siave_e}—Bet H<br>pe! H<br>[aise| cuncu_pw_Sownioas(Gelnve_fu_imese 1_insntsispi_ptany- peliofe)p! t'<br>| _ _ usp 1_write_s3_mem{sw_me_s_apor, H<br>— Sas '<br>' —— — -M4 MCU into sleep Mode - "|<br>' Date Suffering to SRAM<br>’ with specific batch Size<br>; t_SAL_Sensoriocti(handie, Gl_SAL_IOCTL_SATCH_OFriveKs *)WU eae ee<br>|; | Tippeciae comerot nto wstberne (So;  oT Sewo  Eeesnake memory rNdevasis an Paoke FaoSee ;<br>'(eb ese inca sp memtassresset<br>(Snes ejeeare, =) <= i<br>(SScise Gisharea_Mem,need23_memise e ot(sheres_Mten))seress, (eines t*)_ |1 H'<br>a QL |_Read_=3_Mem (address, , eeeeeeeseoeeeeeen=<br>t t :<br>:eR(GUS Lwrite_s3_Memce al: t<br><!-- End of picture text -->

<u>www.quicklogic.com</u> **11** • • • ••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Batching in Companion Mode Rev. 1.1_** 

## **Contact Information** 

Phone: (408) 990-4000 (US) +(44) 1932-21-3160 (Europe) +(886) 26-603-8950 (Taiwan) +(86) 139-0517-5302 (China) +(81) 3-5875-0547 (Japan) +(82) 31-601-4225 (Korea) 

E-mail: <u>info@quicklogic.com</u> 

Sales: <u>America-sales@quicklogic.com Europe-sales@quicklogic.com Asia-sales@quicklogic.com Japan-sales@quicklogic.com Korea-sales@quicklogic.com</u> 

Support: <u>www.quicklogic.com/support</u> 

Internet: <u>www.quicklogic.com</u> 

## **Revision History** 

|**Revision**|**Date**|**Originator and Comments**|
|---|---|---|
|1.0|May2017|Initial Release|
|1.1|June 2017|Marc Miller and Kathleen Bylsma|



## **Notice of Disclaimer** 

QuickLogic is providing this design, product or intellectual property "as is." By providing the design, product or intellectual property as one possible implementation of your desired system-level feature, application, or standard, QuickLogic makes no representation that this implementation is free from any claims of infringement and any implied warranties of merchantability or fitness for a particular purpose. 

You are responsible for obtaining any rights you may require for your system implementation. QuickLogic shall not be liable for any damages arising out of or in connection with the use of the design, product or intellectual property including liability for lost profit, business interruption, or any other damages whatsoever. QuickLogic products are not designed for use in life-support equipment or applications that would cause a life-threatening situation if any such products failed. Do not use QuickLogic products in these types of equipment or applications. 

QuickLogic does not assume any liability for errors which may appear in this document. However, QuickLogic attempts to notify customers of such errors. QuickLogic retains the right to make changes to either the documentation, specification, or product without notice. Verify with QuickLogic that you have the latest specifications before finalizing a product design. 

**12** <u>www.quicklogic.com</u> •• •••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – Batching in Companion Mode Rev. 1.1_** 

## **Copyright and Trademark Information** 

Copyright © 2017 QuickLogic Corporation. All Rights Reserved. 

The information contained in this document is protected by copyright. All rights are reserved by QuickLogic Corporation. QuickLogic Corporation reserves the right to modify this document without any obligation to notify any person or entity of such revision. Copying, duplicating, selling, or otherwise distributing any part of this product without the prior written consent of an authorized representative of QuickLogic is prohibited. 

QuickLogic is a registered trademark, and the QuickLogic logo is a trademark of QuickLogic. Other trademarks are the property of their respective companies. 

<u>www.quicklogic.com</u> **13** • • • ••• 

© 2017 QuickLogic Corporation 

