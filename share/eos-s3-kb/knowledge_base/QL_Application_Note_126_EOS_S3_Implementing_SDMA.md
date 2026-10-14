---
title: "QuickLogic EOS S3 Application Note 126: Implementing SDMA"
source_file: "QL Application Note 126 EOS S3 Implementing SDMA.pdf"
pages: 17
sha256: d3b9395ce537e78ad409448c018d03323576081279afe7bcbe4190cfff7a8863
---

# QuickLogic EOS S3 Application Note 126: Implementing SDMA

**EOS**<sup>**TM**</sup> **S3: Implementing SDMA Application Note 126** 7 **Revision 1.1** . =QuickLogic’ 

## **Ordering Information** 

There are numerous part numbers available depending on different factors. Contact your QuickLogic Field Application Engineer (FAE) for the appropriate part number for your use case. 

## **Contact Information** 

Phone: (408) 990-4000 (US) +(44) 1932-21-3160 (Europe) +(886) 26-603-8948 (Taiwan) +(86) 139-0517-5302 (China) +(81) 3-5875-0547 (Japan) +(82) 31-601-4225 (Korea) E-mail: <u>info@quicklogic.com</u> Sales: <u>America-sales@quicklogic.com Europe-sales@quicklogic.com Asia-sales@quicklogic.com Japan-sales@quicklogic.com Korea-sales@quicklogic.com</u> Support:www.quicklogic.com/support Internet:www.quicklogic.com 

## **Revision History** 

|**Revision**|**Date**|**Originator and Comments**|
|---|---|---|
|1.0|May 2016|Initial release:<br>San Wongand Bruce Wylie|
|1.1|June 2016|Review Comments Incorporated|



## **Notice of Disclaimer** 

QuickLogic is providing this design, product or intellectual property "as is." By providing the design, product or intellectual property as one possible implementation of your desired system-level feature, application, or standard, QuickLogic makes no representation that this implementation is free from any claims of infringement and any implied warranties of merchantability or fitness for a particular purpose. 

You are responsible for obtaining any rights you may require for your system implementation. QuickLogic shall not be liable for any damages arising out of or in connection with the use of the design, product or intellectual property including liability for lost profit, business interruption, or any other damages whatsoever. QuickLogic products are not designed for use in life-support equipment or applications that would cause a life-threatening situation if any such products failed. Do not use QuickLogic products in these types of equipment or applications. 

•••••• 

© 2016 QuickLogic Corporation 

<u>www.quicklogic.com</u> 

QuickLogic does not assume any liability for errors which may appear in this document. However, QuickLogic attempts to notify customers of such errors. QuickLogic retains the right to make changes to either the documentation, specification, or product without notice. Verify with QuickLogic that you have the latest specifications before finalizing a product design. 

## **Copyright and Trademark Information** 

Copyright © 2016 QuickLogic Corporation. All Rights Reserved. 

The information contained in this document is protected by copyright. All rights are reserved by QuickLogic Corporation. QuickLogic Corporation reserves the right to modify this document without any obligation to notify any person or entity of such revision. Copying, duplicating, selling, or otherwise distributing any part of this product without the prior written consent of an authorized representative of QuickLogic is prohibited. 

QuickLogic is a registered trademark and the QuickLogic logo is a trademark of QuickLogic. Other trademarks are the property of their respective companies. 

•••••• 

© 2016 QuickLogic Corporation 

<u>www.quicklogic.com</u> 

# **Contents** 

## **• • • • • •** 

|Ordering Information ......................................................................................................................... ii|
|---|
|Contact Information............................................................................................................................ ii|
|Revision History................................................................................................................................. ii|
|Notice of Disclaimer........................................................................................................................... ii|
|Copyright and Trademark Information ............................................................................................... iii|
|Preface............................................................................................................................................... 1|
|Introduction ...................................................................................................................................1|
|Intended Audience ........................................................................................................................1|
|Document Organization ................................................................................................................2|
|Contacting QuickLogic ..................................................................................................................2|
|Overview of DMAs in the EOS S3 ..................................................................................................... 2|
|EOS S3 DMAs ..............................................................................................................................3|
|System DMA Features..................................................................................................................4|
|SDMA Functional Description............................................................................................................ 5|
|SDMA Power Island Management................................................................................................... 10|
|Wakeup from Power Collapse ....................................................................................................10|
|SDMA Wakeup by FFE.........................................................................................................10|
|SDMA Wakeup By FFE.........................................................................................................10|
|SDMA Wakeup By FPGA......................................................................................................10|
|Power Collapse...........................................................................................................................10|
|Hardware Power Collapse ....................................................................................................10|
|Software Power Collapse......................................................................................................11|
|Implementing Methods..................................................................................................................... 11|
|Using QuickLogic API Board Support Package ..........................................................................11|
|Direct Register Configuration......................................................................................................11|



••• <mark>•</mark> •• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation **iv** 

<u>www.quicklogic.com</u> 

# **Figures** 

## **• • • • • •** 

Figure 1:EOS S3 DMA Locations ...................................................................................................... 4 Figure 2:SDMA Functional Block Diagram ........................................................................................ 6 Figure 3:System DMA Controller Block Diagram............................................................................... 7 Figure 4:System DMA Interface......................................................................................................... 7 

••• <mark>•</mark> •• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation **v** 

<u>www.quicklogic.com</u> 

# **Tables** 

**• • • • • •** 

Table 1: System DMA Channels and Assignments........................................................................... 9 

••• <mark>•</mark> •• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation **vi** 

<u>www.quicklogic.com</u> 

# **QuickLogic EOS S3 Implementing SDMA** 

## **• • • • • • QuickLogic Application Note 126** 

## **Preface** 

This preface provides a brief overview, defines the audience, outlines the organization of this application note, and provides information about contacting QuickLogic for additional assistance in the following sections: 

- **Introduction** on page 1 

- **Intended Audience** on page 1 

- **Document Organization** on page 2 

- **Contacting QuickLogic** on page 2 

### **Introduction** 

The QuickLogic<sup>®</sup> EOS<sup>TM</sup> S3 system is a multi-core, ultra-low power sensor processing system designed for mobile market applications including smartphones, wearables, and Internet of Things (IoT) devices. 

The EOS S3 multi-core architecture enables smartphone application processors to offload real-time, always-on sensor computational requirements to EOS S3 system. The multi-core approach and multiple power islands allow the EOS S3 system to process sensor data and run sensor fusion algorithms in the most processing and power efficient manner possible. 

The primary goal of this application note is to provide information that enables an experienced and knowledgeable end-user to more easily understand the System Direct Memory Access (SDMA) used in the EOS S3 system. This application note consists of the following major chapters: 

- **Overview of DMAs in the EOS S3** on page 2 

- **SDMA Functional Description** on page 5 

- **SDMA Power Island Management** on page 10 

- **Implementing Methods** on page 11 

### **Intended Audience** 

This application note is written for hardware and software validation or evaluation engineers who are familiar with implementing SDMA architecture into a SoC design like the EOS S3. 

•••••• 

© 2016 QuickLogic Corporation 

> www.quicklogic.com **1** 

**<mark>PRELIMINARY</mark>** 

**_QuickLogic EOS S3 Application Note 126: Implementing SDMA_** 

### **Document Organization** 

This application note is organized into the following chapters: 

- **Preface** on page 1: 

   - Provides a brief introduction to the EOS S3 system. 

   - Describes the intended audience. 

   - Describes the document organization. 

   - Provides a best practice for contacting your QuickLogic FAE for assistance. 

- **Overview of DMAs in the EOS S3** on page 2: 

   - Provides an overview of the DMAs used in the EOS S3 system. 

- **SDMA Functional Description** on page 5: 

   - Provides a basic functional description of the SDMA in the EOS S3 system. 

- **SDMA Power Island Management** on page 10: 

   - Describes the EOS S3 SDMA power island management. 

- **Implementing Methods** on page 11: 

   - Describes the two methods for implementing the EOS S3 SDMA. 

### **Contacting QuickLogic** 

To obtain information, technical support, or to inquire about any support-related issue for a QuickLogic product, contact your local Field Application Engineer (FAE) for assistance. 

## **Overview of DMAs in the EOS S3** 

In general, DMAs provide the capability to move data from one resource to another without requiring the use of dedicated Application Processor (or any other processor) resources. Once the data transfer operation starts, it keeps reading or writing from the source to the destination until the operation completes. 

System direct memory access (SDMA) is a key feature of the EOS S3 system that allows its subsystem circuitry to access system memory and transfer data independently of any continued processor overhead. SDMA is a more complicated form of DMA. 

Without the use of a SDMA, processors in the S3 that use programmed I/O would typically be occupied for the entire duration of any read or write operation, use processor resources and power, and make it unavailable to perform any other duties. 

The benefits of an SDMA are that processors in the S3 only need to initiate the data transfer operation; they are then free to perform other operations or go into sleep mode and conserve resources and power while the data transfer is in progress. 

•••••• 

© 2016 QuickLogic Corporation 

> www.quicklogic.com **2** 

**<mark>PRELIMINARY</mark>** 

**_QuickLogic EOS S3 Application Note 126: Implementing SDMA_** 

The processor receives an interrupt from the SDMA once the operation is completed, and among the featured benefits that the SDMA provides are: 

- Performing memory to memory, memory to peripheral, or peripheral to memory copying or movement of data with memory. 

- Off-loading processors from expensive memory operations or requiring a processor to keep up with any specific data transfer rate. 

- Allowing processors to perform other operations without having to wait for a relatively slow IO data transfer, or to conserve processor power consumption. 

- Reducing processor overhead that is normally associated with transferring data to and from memory devices or resources. 

### **EOS S3 DMAs** 

The EOS S3 contains the following four instances of a DMA in its design (see **Figure 1** on page 4, where these four locations are highlighted): 

- SDMA (System DMA): 

   - The SDMA is a 16-channel DMA that can be configured to transfer data among M4 SRAM, the Field Programmable Gate Array (FPGA), the Flexible Fusion Engine (FFE), and I<sup>2</sup> S Slave. 

- DMA resides in the Top-Level Controller (TLC) circuitry: 

   - This DMA transfers data from the Application Processor through the Serial Peripheral Interface (SPI) Slave port to SRAM, and this is a dedicated DMA. 

- DMA resides in the CfgDMA circuitry: 

   - This DMA performs the dedicated function of transferring data from external flash memory to the SRAM via the SPI Master and Pin Mux circuitry. This DMA functions to move data from the SPI Master (essentially from flash to SRAM). 

- DMA resides in the Voice subsystem circuitry: 

   - This DMA performs the dedicated function of transferring data from the microphones associated with the Voice subsystem from the Pulse Code Modulation (PCM) to the M4 SRAM via the M4-AHB bus. 

•••••• 

© 2016 QuickLogic Corporation 

> www.quicklogic.com **3** 

**<mark>PRELIMINARY</mark>** 

**_QuickLogic EOS S3 Application Note 126: Implementing SDMA_** 

Figure 1: EOS S3 DMA Locations 



<!-- Start of picture text -->
CuK<br>& RST | [10 Mux |<br>[oe]ADC | |[PM] PMU| |wc] wic[le MPU+FPUsBtBand+FPBre<br>—_ PKT<br>as m4 |<br>es PONARE | “_o<br>L eo | | stave Voice[oma]ss i(a<br>[eseSPI JL |<br>Master Ta]<br><!-- End of picture text -->

### **System DMA Features** 

The SDMA is the more complex and versatile among the DMAs within the EOS S3 system, which includes the following features: 

- Uses the AHB-Lite bus to perform the DMA transfer operations 

- Uses the Advanced Peripheral Bus (APB) to program the registers 

- Uses a single AHB-Lite master to transfer data using a 32-bit address bus and 32-bit data bus 

- Supports up to 16 DMA channels 

- Provides dedicated handshake signals for each DMA channel 

- Provides programmable priority level for each DMA channel 

- Each priority level arbitrates using a fixed priority that is determined by the DMA channel number 

- Supports the following data transfer types: 

   - Memory-to-Memory 

   - Memory-to-Peripheral 

   - Peripheral-to-Memory 

- Supports multiple DMA cycle types 

- Supports multiple DMA transfer data widths 

- Each DMA channel can access a primary and an alternate channel control data structure 

- All channel control data is stored in system memory using the little-endian format 

- Performs all DMA transfers using a single AHB-Lite bus burst type mechanism 

•••••• 

© 2016 QuickLogic Corporation 

> www.quicklogic.com **4** 

**<mark>PRELIMINARY</mark>** 

**_QuickLogic EOS S3 Application Note 126: Implementing SDMA_** 

**NOTE:** For addition information, descriptions, and other reference material about the SDMA in the EOS S3 system, refer to the _QuickLogic EOS S3 Sensor Processing Platform Data Sheet, Revision 1.3_ . 

## **SDMA Functional Description** 

The SDMA functions to offload data transfer tasks from the M4 processor, and by doing so, it allows the M4 processor to enter its sleep mode that makes it possible to save power and processor resources. 

The SDMA uses an AHB-Lite master port for reading DMA descriptors from the SDMA128x32-bit SRAM and transferring data from source to destination. 

The SDMA AHB Master port is connected to the Always-ON AHB bus matrix so that it can transfer data even when M4 power domain is in a Deep Sleep (DS) or Shut Down (SD) mode. The AON-AHB bus is the bus interface between the source and destination memory locations. 

**Figure 2** on page 6 is a simplified schematic diagram example that illustrates the working principle of the SDMA with one channel. In this one-channel example, the SDMA is controlled by the M4 processor, and the process is as follows: 

- M4 first configures the DMA Controller by writing to its internal register. The source, destination, starting address, and length of data transfer are written as descriptors in the SDMA SRAM. 

- M4 toggles the DMA_REQ signal to send an interrupt to the DMA Controller to initiate the data transfer. At this point, M4 can go into sleep mode. 

- The DMA Controller loads the descriptor from the SDMA SRAM, reads from the source and writes to the destination byte-by-byte until the data transfer is completed. Once completed, the DMA Controller interrupts M4 through the DMA_DONE signal. During the data transfer, DMA_ACTIVE is asserted. 

**NOTE:** The intent of this simplified schematic diagram one-channel example is to show the SDMA controlled by the M4 processor. In general use, the DMA_REQ signal to send an interrupt to the DMA Controller might instead originate from a peripheral (for example, the I2S Slave or the FPGA) or from the SDMA Bridge. 

•••••• 

© 2016 QuickLogic Corporation 

> www.quicklogic.com **5** 

**<mark>PRELIMINARY</mark>** 

**_QuickLogic EOS S3 Application Note 126: Implementing SDMA_** 

Figure 2: Simplified SDMA Functional Block Diagram 



**Figure 3** on page 7 illustrates the functional sections within the SDMA: 

- The _APB Memory Mapped Registers_ block contains the SDMA control and status registers. 

- The _AHB-Lite Master Interface_ reads data from the source and writes this data to the designated destination memory locations. 

- The _DMA Control Block_ arbitrates the incoming requests, performs DMA transfers, and indicates the DMA transfer status. 

**Figure 4** on page 7 illustrates the relationship between the SDMA Bridge and the System DMA Controller within the System DMA interface: 

- The _SDMA Bridge_ muxes the interrupt and status signals of the SDMA to the controlling agents such as M4, FPGA, and FFE. 

•••••• 

© 2016 QuickLogic Corporation 

> www.quicklogic.com **6** 

**<mark>PRELIMINARY</mark>** 

**_QuickLogic EOS S3 Application Note 126: Implementing SDMA_** 

Figure 3: System DMA Controller Block Diagram 



<!-- Start of picture text -->
Configuration DMA Data<br>Control APB Memory AHB-Lite Master Transfer<br>Mapped Registers Interface<br>APB Block AHB Block<br>DMA Active<br>Requests Channel<br>DMA Channel<br>Stall Done<br>DMA Channel<br>Modes Errors<br>DMA Control Block<br><!-- End of picture text -->

Figure 4: System DMA Interface 



<!-- Start of picture text -->
SRAM<br>128x32KB<br>AHB2SRAM<br>From 12S Slave A *0l0 Slave Port| |AON-AHB<br>To M4 VIC DMA_DONE[13:0] DMAC Interconnect<br>Master Port<br>DMA_REQ{15:12] Slave Port,<br>FPGA DMA_SREQ[15:12]<br>Interface DMA_DONEI15:12] AHB2APB<br>DMA_ACTIVE[15:12)<br>Master Port<br>DMA REay7:t}, [11:8]<br>DMA_SREQI7:11, [11:8] SDMA<br>Dma_Active(7:1}, [11:8] Bridge<br>DMA STALL[15:9)<br>APB-Bus-1<br><!-- End of picture text -->

**<mark>PRELIMINARY</mark>** 

> www.quicklogic.com **7** •••••• 

© 2016 QuickLogic Corporation 

**_QuickLogic EOS S3 Application Note 126: Implementing SDMA_** 

**Figure 4** illustrates the schematics of the 16-channel SDMA. The 16 channels are organized in different groups for different types of services. Some flexibility is allowed in each group, and each channel has it own set of status and control signals that include: 

- DMA_REQ[0:15] – signal that initiates the DMA transfer. 

- DMA_SREQ[1:15] – signal that initiates a single-word DMA transfer. 

- DMA_DONE[0:15] – status signal that indicates the completion of the DMA transfer. 

- DMA_ACTIVE[1:15] – status signal that indicates that the DMA transfer is executing. 

- DMA_STALL[0:15] – signal that stalls the DMA transfer. 

Channel0 belongs to the first group, which is dedicated to data transfers from SRAM to the I<sup>2</sup> S Slave port. Audio data is moved from SRAM to the I<sup>2</sup> S Slave port that connects to an Application Processor (AP) or other external I<sup>2</sup> S Master. The transfer _initiation_ signal comes directly from the I<sup>2</sup> S Slave port. The transfer _complete_ signal is connected to the M4 Vector Interrupt Controller (VIC). The transfer _active_ signal is not used. 

Channel1 to Channel7 are primarily controlled by M4, although the FFE can also fill the descriptor for transfer. The transfer _initiation_ , _complete_ , and _active_ signals are routed to M4 through the SDMA Bridge. 

Channel8 to Channel11 are primarily controlled by the FFE, although M4 can also fill the descriptor for transfer. The transfer _initiation_ and _active_ signals are connected to the FFE or M4 through the SDMA Bridge. The _complete_ signals are routed to M4 through the SDMA Bridge. 

Channel12 to Channel15 are dedicated to the FPGA Fabric logic. M4 or the FFE can fill the transfer descriptors. The transfer _initiation_ , _complete_ , and _active_ signals are connected to the FPGA directly. 

**Table1** on page 9 summarizes the configurability of the 16 channels described above. The following types of SDMA data transfers for the 16 DMA channels that can be completed include: 

- Voice data from the M4 SRAM to the I<sup>2</sup> S Slave 

- Data from the M4 SRAM to the FFE Code Manager (CM) 

- Data from the M4 SRAM to the FFE Data Manager (DM) 

- Data from the FFE DM to the M4 SRAM 

- Data from the M4 SRAM to the FPGA Fabric 

- Data from the FPGA Fabric to the M4 SRAM 

•••••• 

© 2016 QuickLogic Corporation 

> www.quicklogic.com **8** 

**<mark>PRELIMINARY</mark>** 

**_QuickLogic EOS S3 Application Note 126: Implementing SDMA_** 

Table 1: System DMA Channels and Assignments 

|**Channel**<br>**Number**|**Primary**<br>**Channel**|**Alternate**<br>**Channel**|**Channel**<br>**Trigger**|**Channel**<br>**Acknowledge**|**Description**<br>**or Comment**|
|---|---|---|---|---|---|
|0|M4|FFE|I<sup>2</sup>S|M4|Masking under software<br>control is possible for<br>Channel 0.|
|1-7|M4|FFE|SDMA Bridge|SDMA Bridge<br>and M4|Channels 1-7 are under the<br>direct control or reserved for<br>use by M4.|
|8-11|FFE|M4|SDMA Bridge|SDMA Bridge<br>and M4|Channels 8-11 can be<br>controlled by either FFE or<br>M4. The DMA_DONE signals<br>associated with these<br>channels are connected to<br>the VIC in M4.|
|12-15|M4|FFE|FPGA|FPGA||



In **Table 1** , note that there are _Primary Channel_ and _Alternate Channel_ settings that you can configure on a per channel-basis for each of the 16 DMA channels (0-15), and these assignments are based on software convention. The _Channel Trigger_ in the table identifies the location from which the request is originating, and the VIC associated with DMA channels 8-11 is part of the M4 subsystem. Configuring SDMA transfers includes the following three elements: 

- DMA descriptors – Each DMA channel has two associated channel descriptor structures that are normally located in SDMA SRAM. These include the source and destination address for the channel as well as information like the number of elements to transfer, data size, transfer type. 

**NOTE:** When a channel is triggered, the DMA reads the associated descriptor from SRAM, which includes instructions on what actions the DMA should take. When the channel has finished completing the defined actions, the updated descriptors are written back to the SRAM. 

**NOTE:** For details and to better understand DMA descriptors and the DMA Controller in the EOS S3, refer to the following ARM<sup>®</sup> document specification at the following location: 

http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.ddi0417a/index.html 

- DMA registers – Common configurations for the DMA, as well as DMA-generated interrupts and trigger sources for the various channels are configured in the DMA registers. The location of the DMA descriptors in SRAM is also configured here. 

- Registers in trigger peripheral – The DMA request signals from the peripherals get generated by various events in the peripherals; hence, it is important to configure the peripherals correctly to generate the desired DMA requests. 

Each channel’s transfer descriptor consists of four words and these descriptors are hosted in a 128x32-bit SRAM connected to the AON-AHB. Channel Descriptor Data Structure SRAM (CDDS-SRAM) is accessible by both M4 and the FFE, where both of these AHB-Lite masters can update descriptors. 

As shown in **Table 1** , each channel has a primary and an alternate master that can program this channel. For example, Channel0 CDDS is primarily expected to be programed by M4, but it is also possible for the FFE to update CDDS for Channel0 . The master that does the update is based on software convention and is not under hardware control. 

•••••• 

© 2016 QuickLogic Corporation 

> www.quicklogic.com **9** 

**<mark>PRELIMINARY</mark>** 

**_QuickLogic EOS S3 Application Note 126: Implementing SDMA_** 

## **SDMA Power Island Management** 

This section describes the power island management for the SDMA power island. 

### **Wakeup from Power Collapse** 

When M4, the FFE, or FPGA wants to perform an SDMA transfer, they initiate by checking the power state of the SDMA. In cases where the SDMA is powered down, M4 sends a request to the Power Management Unit (PMU) to turn _on_ SDMA. Upon completion of the power up sequence, in case of M4 and FFE, the SDMA transfer is initiated by writing to the appropriate register in the SDMA Bridge. When the FPGA wants to perform an SDMA transfer, it toggles the DMA_REQ pins associated with Channel12 through Channel15 . 

#### **SDMA Wakeup by FFE** 

The FFE wakes up SDMA from power collapse by sending an interrupt to M4. This interrupt is sent to M4 over 1 of 8 FFE interrupt pins. These pins are connected to Wakeup Interrupt Controller (WIC), which wakes up M4, in cases where it was not awake. 

Once M4 observes this interrupt, M4 requests the PMU to wake up SDMA. M4 can poll appropriate flags inside PMU to check for the completion of SDMA power up sequence. Upon completion of this sequence, M4 can send a message to FFE using existing messaging mechanism to notify the FFE to start the SDMA transfer. 

#### **SDMA Wakeup By FFE** 

The FFE wakes up SDMA from power collapse by sending an interrupt to M4. This interrupt is sent to M4 over 1 of the 8 FFE interrupt pins. These pins are connected to Wakeup Interrupt Controller (WIC), which wakes up M4 when it was not awake. Once M4 observes this interrupt, M4 requests the PMU to wake up the SDMA. M4 can poll the appropriate flag inside PMU to check for the completion of the SDMA power up sequence. Upon completion of this sequence, M4 can send a message to the FFE using the existing messaging mechanism to notify the FFE to start the SDMA transfer. 

#### **SDMA Wakeup By FPGA** 

The FPGA SDMA wakeup sequence is similar to the FFE SDMA wakeup sequence. Once the SDMA has been powered up, M4 can send a notification by writing to the state inside FPGA by using its master port. 

### **Power Collapse** 

When it is not in use, the SDMA is power collapsed to minimize its static power profile. Power to the SDMA can be collapsed by using either a hardware or software method. 

#### **Hardware Power Collapse** 

The SDMA-PM logic constantly tracks the requests for SDMA transfers made using the DMA_REQ or DMA_SREQ pins and the SDMA bridge, and the DMA_DONE signals associated with all channels. 

As shown in **Table 1** , transfer requests to SDMA Channel0 and Channel12 through Channel15 are made using pins, whereas requests for Channel1 through Channel11 are made using the SDMA bridge. 

•••••• 

© 2016 QuickLogic Corporation 

> www.quicklogic.com **10** 

**<mark>PRELIMINARY</mark>** 

**_QuickLogic EOS S3 Application Note 126: Implementing SDMA_** 

Once the SDMA-PM detects no pending SDMA transfers, the SDMA-PM sends a request to the PMU requesting the power down of the SDMA power island. The PMU uses this incoming request from the SDMA-PM along with the state of SDMA_Hardware_PowerDown_Request flag to decide whether to keep the SDMA power island _on_ or turn it _off_ . 

In cases where the software has set the SDMA_Hardware_PowerDown_Request flag requesting that the PMU ignore the SDMA-PM power down request, the PMU will not power collapse the SDMA power island. Software can allow the PMU to honor the power down request from the SDMA-PM by deasserting the SDMA_Hardware_PowerDown_Request flag. 

#### **Software Power Collapse** 

The PMU provides explicit SDMA power island management to the software. 

## **Implementing Methods** 

There are two methods you can use to implement SDMA to meet your specific product needs: 

- QuickLogic-provided Application Programming Interface (API) 

- Direct register configuration 

**NOTE:** QuickLogic recommends that customers use the first method for implementation. 

### **Using QuickLogic API Board Support Package** 

Contact QuickLogic or your local QuickLogic FAE to obtain the _QuickLogic EOS S3 Board Support Package_ . The EOS S3 Board Support Package (BSP) contains APIs and instructions for the customers to install and use when implementing SDMA. 

### **Direct Register Configuration** 

It is not the intent of this application note to document how to configure hardware registers for the EOS S3, nor is this method recommended for the great majority of customers. This requires a high level of experience and detailed knowledge of the registers and circuitry of the EOS S3 system. 

•••••• 

© 2016 QuickLogic Corporation 

> www.quicklogic.com **11** 

**<mark>PRELIMINARY</mark>** 

