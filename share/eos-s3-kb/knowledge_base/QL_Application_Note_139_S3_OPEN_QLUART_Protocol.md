---
title: "QuickLogic Application Note 139 - QuickLogic\u00ae S3 OPEN \u2013 QLUART Protocol"
source_file: "QL Application Note 139 \u2013 S3 OPEN QLUART Protocol.pdf"
pages: 19
sha256: b3eafdd40dc17ab9d80f033530ee97551e3a9c2aabe8be28648cc9bb3de32c4f
---

# QuickLogic Application Note 139 - QuickLogic® S3 OPEN – QLUART Protocol

# **QuickLogic**<sup>**®**</sup> **S3 OPEN – QLUART Protocol** 

**• • • • • • QuickLogic Application Note 139** 

## **Introduction** 

This document describes Universal Asynchronous Receive Transmit (UART) communication using QuickLogic UART (QLUART) protocol between the S3 and Host device. It provides information about QLUART porting on the reference design board (RDB) with S3 and the other hardware platforms. It also explains the functionality of Receive and Transmit in QLUART. 

## **QLUART Protocol** 

QLUART is Quick Logic’s robust communication protocol based on UART. It can be used for Host-to-Host communication connected via the UART bus. QLUART has the following features: 

- Generic implementation which can be ported to other hardware platforms and operating systems 

- Supports error detection. 

- Allows retransmission and timeout 

- Application independent 

- Supports sleep/wakeup mechanism 

<u>www.quicklogic.com</u> **1** ••• ••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – QLUART Protocol –  Rev. 1.0_** 

### **QLUART Interaction with Software and Hardware Components** 

**Figure 1** shows the software and hardware layers involved in QLUART. 

Figure 1: QLUART Interaction with Software and Hardware Components 



<!-- Start of picture text -->
i<br>Voice Other<br>| Client/s<br>\<br>Software Layers<br>QLUART<br>Platform UART<br>Driver<br>a<br>UART<br>controller<br>wake | UARTpata | UARTData WakeGpif o m Hardware Pins.<br>host ™ RK BT host<br><!-- End of picture text -->

**2** <u>www.quicklogic.com</u> •• •••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – QLUART Protocol –  Rev. 1.0_** 

### **QLUART Communication** 

**Figure 2** details how the host sends a command to the S3 device. 

Figure 2: QLUART Communication 



<!-- Start of picture text -->
QLUART Host QLUART HOST:<br>1. Wake up the<br>QLUART Host 2 INTR<br>9, Wait for Rio READY TO RECIEVE<br>MessageOLVART fiom HOST? RX. x<br>COMMAND<br>3_ 1x RX<br>Packet<br>packet 5.receivedAfter SendingcommandAckwil packet thebe sent to<br>Sequence to<br>senda,a 6.QLUARTWake vpHost the 1<br>Packet to READY TO RECIEVE 7. Wait for RioR.<br>another Host ix RY — Message from<br>For ex:- This OLUARTto pet ready. HOSTI<br>Gm be aatacs ON ee<br>command RY COMMAND TX 8.CommandSend<br>packer<br>1x ACK RX9.message.Wait for the Ack.<br>Sequence to send a<br>QLUART Packet<br>to another Host<br>For ex: This can be<br>a voice<br>Response/Event<br>from voice client<br>on host 2<br><!-- End of picture text -->

##### **NOTE:** 

- R2R – Ready to Receive 

- ACK – Acknowledgment 

- INTR – Interrupt 

<u>www.quicklogic.com</u> **3** • • • ••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – QLUART Protocol –  Rev. 1.0_** 

### **QLUART/Client Interaction** 

**Figure 3** shows the QLUART/Client interaction. QLUART is based on commands and responses/events protocol. 

Figure 3: QLUART/Client Interaction 



<!-- Start of picture text -->
Host 1<br>G >)<br>Client |<br>Responses/<br>Commands Events<br>QLUART<br><!-- End of picture text -->

The Client transfers command packets through QLUART and receives responses/events that are sent by the respective components on the other Host. For example, a Voice Client sends a voice command to a voice system on another Host and waits for a response and/or event from that Host. 

QLUART does not determine if client packets are commands or responses. It simply transmits the data packets and invokes a callback upon data packet reception. For a transmit operation QLUART sends internal ACK packets to ensure that the data is received by receiver. 

#### **QLUART Packet Types** 

QLUART packet types include: 

- Data Packet – This packet consists of the command sent from the Host to S3, or the event/response from the S3 to the Host. 

- Control Packets – These packets are sent internally by the QLUART to ensure that the communication between two QLUART Hosts has data integrity and is reliable. 

   - ACK Packet – This packet is sent to the sender to acknowledge that the data packet has been received properly. 

   - NACK Packet – This packet indicates that there is an issue with the data packet received, and the sender will the retransmit the data packet. 

   - Ready to Receive (R2R) Packet – This packet is sent in response to the wake-up GPIO rising edge. It confirms that the Host on the other side is awake and ready for further transactions. 

Figure 4: Data Packet Structure 

|Byte1|Byte2|Byte3|Byte4|Byte5 to (n-3)|n-2|n-1|Byte n|
|---|---|---|---|---|---|---|---|
||||||CRC|CRC||
|SOF|TYPE|R_CNT|LEN|PAYLOAD|Lower<br>Byte|Upper<br>Byte|EOF|



© 2017 QuickLogic Corporation 

**4** <u>www.quicklogic.com</u> •• •••• 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – QLUART Protocol –  Rev. 1.0_** 

Figure 5: Control Packet Structure: 

|Byte1|Byte2|Byte3|Byte 4|
|---|---|---|---|
|SOF|TYPE|R_CNT|EOF|



**Table 1** describes each byte in the Data and Control packets. 

Table 1: QLUART Packet Types 

|**Field**|**Value**|**Description**|
|---|---|---|
|SOF|0x7E|Start of frame.|
|TYPE|Depends on type|Defines a QLUART packet type:<br>1 – Data packet<br>2 – ACK packet<br>3 – NACK<br>4 – R2R|
|R_CNT|Varies|Retry count of the data packet.<br>The range is 1 to MAX_RETRY_COUNT.|
|LEN|Varies|Length of the payload (1 Byte to 255 Bytes)|
|PAYLOAD|Varies|Payload data. Has LEN number of bytes.|
|CRC|Varies|Checksum calculated for PAYLOAD.<br>Byte n-2 is the Lower byte of the 2-Byte CRC.|
|EOF|0x7D|End of frame.|



## **Porting S3 QLUART** 

This section discusses in detail the following steps that are involved in porting: 

**1. Enable QLUART** on page 5. 

**2. Configure UART PADs** on page 6. 

**3. Configure the Wake-Up GPIO and UART Settings** on page 7. 

**4. Configure QLUART Parameters** on page 8. 

### **Enable QLUART** 

Enable the QLUART feature in the Fw_global_config.h file in directory Sources/App. 

#define QLUART_ENABLE #define VOICE_OVER_QLUART #define QLU_TESTING #define QLUART_DBG 

<u>www.quicklogic.com</u> **5** • • • ••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – QLUART Protocol –  Rev. 1.0_** 

**Table 2** describes the Configs defined in the Fw_global_config.h. 

Table 2: 

|**Configs**|**Description**|
|---|---|
|QLUART_ENABLE|Enables the QLUART protocol functionality|
|VOICE_OVER_QLUART|Enables voice communication over QLUART|
|QLU_TESTING|Enables Qlauart_test from command line|
|QLUART_DBG|Enables the QLUART debug logs|



### **Configure UART PADs** 

Configure the PADs for UART Rx/Tx in the uart_config_pad () function based on the PADs used. The following snippet is from the S3 RDB code base. 

TX pin configuration #ifdef QLUART_ENABLE xPadConf.ucPin = PAD_44; xPadConf.ucFunc = PAD44_FUNC_SEL_UART_TXD; xPadConf.ucCtrl = PAD_CTRL_SRC_A0; xPadConf.ucMode = PAD_MODE_OUTPUT_EN; xPadConf.ucPull = PAD_NOPULL; xPadConf.ucDrv = PAD_DRV_STRENGHT_4MA; xPadConf.ucSpeed = PAD_SLEW_RATE_SLOW; 

RX pin Configuration #ifdef QLUART_ENABLE xPadConf.ucPin = PAD_45; xPadConf.ucFunc = PAD45_FUNC_SEL_UART_RXD; xPadConf.ucCtrl = PAD_CTRL_SRC_A0; xPadConf.ucMode = PAD_MODE_INPUT_EN; xPadConf.ucPull = PAD_NOPULL; xPadConf.ucDrv = PAD_DRV_STRENGHT_4MA; xPadConf.ucSpeed = PAD_SLEW_RATE_SLOW; xPadConf.ucSmtTrg = PAD_SMT_TRIG_DIS; 

**6** <u>www.quicklogic.com</u> •• •••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – QLUART Protocol –  Rev. 1.0_** 

### **Configure the Wake-Up GPIO and UART Settings** 

QLUART_init () invokes the qluart_pfm_config function, and passes the wake-up send and receive PADs information to this function. PAD12 is configured for receiving a wake-up interrupt on the rising edge on the RDB, which can be changed according the design. 

/* Output Wakeup GPIO configuration */ xPadConf.ucPin   = info->out_gpio; xPadConf.ucFunc   = PAD9_FUNC_SEL_GPIO_1; xPadConf.ucCtrl   = PAD_CTRL_SRC_A0; xPadConf.ucMode   = PAD_MODE_OUTPUT_EN; xPadConf.ucPull   = PAD_PULLUP; xPadConf.ucDrv   = PAD_DRV_STRENGHT_4MA; xPadConf.ucSpeed  = PAD_SLEW_RATE_SLOW; xPadConf.ucSmtTrg = PAD_SMT_TRIG_DIS; info->out_gpio=GPIO_1; HAL_PAD_Config(&xPadConf); HAL_GPIO_Write(GPIO_1,0); /* Input Wakeup GPIO configuration */ xGpioCfg.usPadNum  = info->in_gpio; xGpioCfg.ucGpioNum  = GPIO_6; xGpioCfg.ucFunc  = PAD12_FUNC_SEL_SENS_INT_6; xGpioCfg.intr_type = EDGE_TRIGGERED; xGpioCfg.pol_type  = RISE_HIGH; xGpioCfg.ucPull  = PAD_PULLDOWN; //Input GPIO configuration as interrupt HAL_GPIO_IntrCfg(&xGpioCfg); 

<u>www.quicklogic.com</u> **7** • • • ••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – QLUART Protocol –  Rev. 1.0_** 

### **Configure QLUART Parameters** 

Configurable parameters are defined in file ql_uart_config.h in the directory /App/QLUART/inc. 

/* Maximum retry count for data packet */ #define    MAX_RETRY_COUNT  (3) /* Timeout for control packets (in ms) */ #define    MAX_TIME_FOR_ACK (5000) /* This defines number of QLUART clients to support */ #define    MAX_QLUART_CLIENTS  (1) /* Maximum payload to support for this platform (1-255) */ #define    MAX_PAYLOAD_LEN  (4) #define    QLUART_BAUD_RATE (9600) #define    QLUART_RX_BUF_PKTS    (2) /* No of data packets to hold in QLUART RX task's queue */ #define    QLUART_RXTASK_MSG_QUEUE_LENGTH  (20) 

## **Porting QLUART on Other Hardware Platforms** 

This section discusses in detail the following steps that are involved in porting to QLUART on other hardware platforms: 

**1. Configure the Wake-Up GPIOs** on page 9 

**2. Initialize QLUART** on page 9 

**3. Map the Operating System-Specific Code** on page 10 

**4. Map the QLUART Wake-Up Function** on page 10 

**5. Reuse the Transmit and Receive Functions** on page 11 

**8** <u>www.quicklogic.com</u> •• •••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – QLUART Protocol –  Rev. 1.0_** 

### **Source Information** 

The following files are located in M4\QL\APP\qluart\ directory. 

- Src 

   - ql_uart.c – Main source file with QLUART implementation 

   - ql_uart_os.c – Operating system-specific implementation of QLUART 

- Inc 

   - ql_uart_config.h – Configuration file for QLUART 

   - ql_uart.h – Header for ql_uart.c 

   - ql_uart_os.h – Header for ql_uart_os.c 

### **Configure the Wake-Up GPIOs** 

- Wake-up GPIOs configuration: 

   - One GPIO is required as an output for waking the other peer QLUART Host 

   - One GPIO is required to wake-up an interrupt from other Host. This GPIO is latched at the rising edge. 

The qluart_pfm_config() function performs the GPIO configuration and must be mapped to a Hostspecific platform. 

### **Initialize QLUART** 

QLUART_Init() invokes the qluart_pfm_config() function and performs platform-specific configuration for GPIO and UART. QLUART_Init() also creates operating system-specific resources such as tasks, locks, and message queue for QLUART usage. 

QLUART_Init() should be done before using QLUART transmit and receive functionality 

The init function uses the QuickLogic Operating System Abstraction Layer (QL_OSAL). 

<u>www.quicklogic.com</u> **9** • • • ••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – QLUART Protocol –  Rev. 1.0_** 

### **Map the Operating System-Specific Code** 

Map the operating system-specific code to the corresponding Host operating system. 

For the S3 platform, which uses FreeRTOS, the QLUART operating system-specific functionality is in the ql_uart_os.c file. For example, QL_OSAL_Mutex_Create is mapped to FreeRTOS mutex APIs. 

QLUART_Status QL_OSAL_Mutex_Create(QL_OSAL_Mutex_t *mutexObj) { struct osal_mutex   *tMutexObj; QL_ASSERT(mutexObj != NULL); tMutexObj = (struct osal_mutex *) QL_OSAL_Malloc(sizeof(struct osal_mutex)); if(tMutexObj == NULL) { return QLUART_STATUS_ERROR; } tMutexObj->object = xSemaphoreCreateMutex(); if(tMutexObj->object == NULL) { QL_OSAL_Free(tMutexObj); return QLUART_STATUS_ERROR; } *mutexObj = tMutexObj; return QLUART_STATUS_OK; } 

Similarly, for the Host operating system-specific Mutex creation call can be mapped to QL_OSAL. 

Another option is to rewrite the init function according to the Host platform and operating system used. 

### **Map the QLUART Wake-Up Function** 

The QLUART_Wakeup_ISR() function is invoked when S3 triggers an Interrupt to the Host platform and it sends an R2R packet to S3. The Interrupt Service Routine (ISR) must be registered to that GPIO/line. 

**10** <u>www.quicklogic.com</u> •• •••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – QLUART Protocol –  Rev. 1.0_** 

### **Reuse the Transmit and Receive Functions** 

Reuse the QL_Transmit function map the UART transmit function to a specific Host platform. For S3, it is mapped to the uart_tx_data() function. Similarly, it can be done for the Host platform 

#define os_uart_tx_data(buf,len) uart_tx_data(buf,len) 

The UART receive function can be reused to map the UART receive function to a specific Host platform. 

The S3 UART Rx ISR invokes the QLUART_Fill_Rx_Buf() function which identifies the packet type. 

- For a Control Packet, it sends an event to the Transmit task waiting. 

- For a Data Packet, it sends the packet to the Rx Msg Queue and a Rx task handler processes the packet and invokes the receive callback function. 

The platform UART Rx ISR handler can reuse the QLUART_Fill_Rx_Buf. 

<u>www.quicklogic.com</u> **11** • • • ••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – QLUART Protocol –  Rev. 1.0_** 

## **Transmit and Receive Flows** 

This section describes the Transmit and Receive flows. 

### **Transmit** 

**Figure 6** shows the Transmit flow. 

Figure 6: Transmit Flowchart 



<!-- Start of picture text -->
Send wake up<br>Interrupt<br>Wait for R2R event<br>Not received R2Revent<br>receieved?<br>R2R received<br>Prepare Data packet<br>and Send it<br>No Wait forevent ACK packet<br>Yes Retry count NACK/Timeout<br>exceeded?<br>ACK received<br>Return Success status<br><!-- End of picture text -->

**12** <u>www.quicklogic.com</u> •• •••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – QLUART Protocol –  Rev. 1.0_** 

### **Receive Interrupt Handler** 

**Figure 7** shows the Receive Interrupt Handler flow. It illustrates how bytes of data are read when the Rx interrupt is triggered, and identifies the packet type (i.e., Control or Data). For a Data Packet, it sends the packet to the Receive Task which is waiting on an Rx queue for data. 

Figure 7: Receive Interrupt Handler Flowchart 



<!-- Start of picture text -->
Data<br>Received<br>‘on RX<br>interrupt<br>No SOF<br>Received?<br>Yes<br>Fill the RX ring<br>Butter<br>Data size in Rx<br>Buffer >= Size of<br>control packet?<br>No<br>Yes<br>packetIdentifyType teevelid bufferResetand theCountersSOF Rx<br>Received.<br>cra<br>A<br>Data<br>Copy the Packet ~~<br>from Ring Buffer} Legare icles<br>to RxMsg Queue =<br>Butfer<br>| No<br>Send the Packet Yes Completea in Rx ButlerData<br>to QLUARTRx<br>Msg Queue *<br>Exit<br><!-- End of picture text -->

<u>www.quicklogic.com</u> **13** • • • ••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – QLUART Protocol –  Rev. 1.0_** 

#### **Control Packet** 

**Figure 8** shows the flow for each type of Control Packet. The Receive handler identifies the type of Control Packet and sends the corresponding event to the waiting task. 

Figure 8: Control Packet Flowchart 



<!-- Start of picture text -->
A<br>Control Packet ?<br>jeer | —<br>Retry Count Yes Yes Retry Count No<br>exceeded ? exceeded? vith<br>No No Yes<br>Send R2R event<br>SendEOFNACKfound?: event No ‘ACK EOFpacketfound?&received No<br>for current Packet<br>Transmitted?<br>Yes<br>Send ACK event<br>exit<br><!-- End of picture text -->

**14** <u>www.quicklogic.com</u> •• •••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – QLUART Protocol –  Rev. 1.0_** 

#### **Receive Task Handler** 

**Figure 9** shows the flow when the Receive Task Handler receives a Data Packet attempts to validates it. Based on the results, it sends a NACK/ACK Control Packet to acknowledge to the other Host about the data reception. 

Figure 9: Receive Task Handler Flowchart 



<!-- Start of picture text -->
RXHandler<br>Task receives<br>‘the Packet<br>from MSG<br>‘QUEUE<br>nape Retry Count ‘Check Payload Valid Verify<br>eae FOR, exceeded? len Checksum{DATA)<br>Yes Invalid Notequal Compare<br>>:~S|<br>Yes<br>Invokecallback the Receive function i Copythe the LocalPayloadbuffer to<br><!-- End of picture text -->

<u>www.quicklogic.com</u> **15** • • • ••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – QLUART Protocol –  Rev. 1.0_** 

## **QLUART Operation APIs** 

This section defines the QLUART Datatypes and Enums and QLUART data structures. 

### **QLUART Datatypes and Enums** 

#### **QLUART_STATUS** 

typedef enum { QLUART_STATUS_OK = 0, /*0 Success */ QLUART_STATUS_ERROR, /*1 Error*/ QLUART_STATUS_ERROR_BAD_PARAMETER, /*2 Bad parameter passed*/ QLUART_STATUS_ERROR_TIMEOUT, /*3 Timeout occurred*/ } QLUART_Status; 

#### **QLUART_Callback** 

The QLUART receive callback function prototype. 

|**Structure**|typedef QLUART_Status (*QLUART_Callback)(uint8_t*data,uint8_t len, void * cookie);|
|---|---|
||data<br>Payload pointer.|
|**Parameters**|len<br>Length of payload|
||cookie<br>Token passed by client to identify multiple instances of the<br>same callback|
|**Description**|This function is called when a valid data packet is received by QLUART.|
|**Returns**|On Success – QLUART_STATUS_OK.<br>On Failure – One of the failure statues, QLUART_STATUS_ERRORx.|



#### **QLUART_PLATFORM_INFO** 

This structure holds platform-specific information required by QLUART. 

|**Structure**|typedef struct {<br>uint8_t out_gpio;<br>uint8_t_ in_gpio;<br>} QLUART_PLATFORM_INFO||
|---|---|---|
|**Pt**|out_gpio|For waking up the QLUART Host on the other side.|
|**arameers**|in_gpio|For the other QLUART Host to wake up this Host.|
|**Description**|This holds the information of wake-|up GPIOs.|



**16** <u>www.quicklogic.com</u> •• •••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – QLUART Protocol –  Rev. 1.0_** 

### **QLUART APIs** 

|**API Signature**|QLUART_Status QLUART_Init(QLUART_PLATFORM_INFO *info);|
|---|---|
|**Parameters**|Info<br>Platform-specific information required by QLUART.|
|**Description**|This initializes the QLUART protocol layer and configures the GPIOs required for wake-up<br>mechanism.|
|**Returns**|On Success – QLUART_STATUS_OK.<br>On Failure – One of the failure statues, QLUART_STATUS_ERRORx.|



|**API Signature**|QLUART_Status QLUART_DeInit(void);|
|---|---|
|**Parameters**|void<br>No parameters.|
|**Description**|This de-initializes the QLUART by freeing all the resources|
|**Returns**|On Success – QLUART_STATUS_OK.<br>On Failure – One of the failure statues, QLUART_STATUS_ERRORx.|
|**API Signature**|QLUART_Status QLUART_Transmit(int8_t* buf, unit8_t len);|
|**Parameters**|buf<br>Payload data.|
||len<br>Length in bytes.|
|**Description**|This API is used to transmit the data reliably to the other QLUART Host. It creates a QLUART data<br>packet and ensures that it is received by the other Host.|
|**Returns**|On Success – QLUART_STATUS_OK.<br>On Failure – One of the failure statues, QLUART_STATUS_ERRORx.|



|**API Signature**|QLUART_Status QLUART_Register_Receive_CallBack(QLUART_Callback cb, void*cookie);|
|---|---|
|**Parameters**|cb<br>Callback pointer.|
||*cookie<br>Variable to identify multiple instances to the same callback.|
|**Description**|This API is called to register a receive data callback function. The callback is invoked when a<br>QLUART data packet is received.|
|**Returns**|On Success – QLUART_STATUS_OK.<br>On Failure – One of the failure statues, QLUART_STATUS_ERRORx.|



<u>www.quicklogic.com</u> **17** • • • ••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – QLUART Protocol –  Rev. 1.0_** 

## **Contact Information** 

Phone: (408) 990-4000 (US) +(44) 1932-21-3160 (Europe) +(886) 26-603-8950 (Taiwan) +(86) 139-0517-5302 (China) +(81) 3-5875-0547 (Japan) +(82) 31-601-4225 (Korea) 

E-mail: <u>info@quicklogic.com</u> Sales: <u>America-sales@quicklogic.com Europe-sales@quicklogic.com Asia-sales@quicklogic.com Japan-sales@quicklogic.com Korea-sales@quicklogic.com</u> 

Support: <u>www.quicklogic.com/support</u> 

Internet: <u>www.quicklogic.com</u> 

## **Revision History** 

|**Revision**|**Date**|**Originator and Comments**|
|---|---|---|
|1.0|September 2017|Nilanjan Roychowdhury and Kathleen Bylsma<br>Initial release.|



## **Notice of Disclaimer** 

QuickLogic is providing this design, product or intellectual property "as is." By providing the design, product or intellectual property as one possible implementation of your desired system-level feature, application, or standard, QuickLogic makes no representation that this implementation is free from any claims of infringement and any implied warranties of merchantability or fitness for a particular purpose. You are responsible for obtaining any rights you may require for your system implementation. QuickLogic shall not be liable for any damages arising out of or in connection with the use of the design, product or intellectual property including liability for lost profit, business interruption, or any other damages whatsoever. QuickLogic products are not designed for use in life-support equipment or applications that would cause a life-threatening situation if any such products failed. Do not use QuickLogic products in these types of equipment or applications. 

QuickLogic does not assume any liability for errors which may appear in this document. However, QuickLogic attempts to notify customers of such errors. QuickLogic retains the right to make changes to either the documentation, specification, or product without notice. Verify with QuickLogic that you have the latest specifications before finalizing a product design. 

**18** <u>www.quicklogic.com</u> •• •••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 OPEN – QLUART Protocol –  Rev. 1.0_** 

## **Copyright and Trademark Information** 

Copyright © 2017 QuickLogic Corporation. All Rights Reserved. 

The information contained in this document is protected by copyright. All rights are reserved by QuickLogic Corporation. QuickLogic Corporation reserves the right to modify this document without any obligation to notify any person or entity of such revision. Copying, duplicating, selling, or otherwise distributing any part of this product without the prior written consent of an authorized representative of QuickLogic is prohibited. 

QuickLogic is a registered trademark, and the QuickLogic logo is a trademark of QuickLogic. Other trademarks are the property of their respective companies. 

<u>www.quicklogic.com</u> **19** • • • ••• 

© 2017 QuickLogic Corporation 

