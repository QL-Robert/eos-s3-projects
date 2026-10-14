---
title: "QuickLogic S3 Boot Loader"
source_file: "QL S3 Boot Loader Application Note 134.pdf"
pages: 12
sha256: cfa0f16d481eabc465a49675c063c14b94379c0214e85f64f53251fde6b46791
---

# QuickLogic S3 Boot Loader

## **QuickLogic**<sup>**®**</sup> **S3 Boot Loader** 

- **• • • • • QuickLogic**<sup>**®**</sup> **Application Note 134** 

### **1.0 Overview** 

When S3 acts as Host, the boot loader initializes the system. The QuickLogic S3 boot loader loads M4, Flexible Fusion Engine (FFE) and Fabric (FPGA) images, and provides the support to flash these images through the UART interface. 

This document explains how to add support for a new board and flash in the S3 boot loader. 

**NOTE:** Chandlar is the internal code name for the QuickLogic S3 Reference Design Board (RDB). 

### **2.0 Hardware Interface** 

**Figure 1** illustrates the hardware interface. 

Figure 1: Hardware Interface 



<!-- Start of picture text -->
QuickLogic Flash Tool<br>UART/JTAG<br>  S3<br>Host<br>MOSI         MISO           SS           CLK<br>Flash Memory<br><!-- End of picture text -->

SPI Pins: 

- MOSI – Master Out Slave In 

- MISO – Master In Slave Out 

- SS – Slave Select 

- CLK – Clock 

# **<mark>PRELIMINARY</mark>** 

••• ••• 

© 2017 QuickLogic Corporation 

<u>www.quicklogic.com</u> **1** 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Boot Loader Rev. 1.0_** 

### **3.0 Adding Support for a New Board with S3** 

This section provides example configuration and settings for the S3 RDB. 

#### **3.1 Adding Configs** 

Define and configure S3 boot loader features in the Autoconfig.h file, located in the directory Sources/Board/Inc/. 

#ifndef __AUTO_CONFIG_H #define __AUTO_CONFIG_H #define DEBUG #define DEFINED_SPI_FLASH_MACRONIX #define FFE_LOAD #define FABRIC_LOAD #define FREE_SRAM_AREA (0x2000A000) #define FREE_SRAM_AREA_SIZE (400 * 1024) #define APP_RAM_START_ADDR (0x20000000) #define FFE_CFG_ADDR (0x2007F800) #endif // __AUTO_CONFIG_H 

**Table 1** describes the features and configs defined in the Autoconfig.h file. 

Table 1: Autoconfig.h File Contents 

|**Parameter**|**Description**|
|---|---|
|DEBUG|Enables boot loader debug logs.|
|DEFINED_SPI_FLASH_MACRONIX|Enables MACRONIX flash driver.|
|FFE_LOAD|Enables boot loader to load the FFE binary into memory.|
|FABRIC_LOAD|Enables boot loader to load the Fabric binary into memory.|
|FREE_SRAM_AREA|Defines buffer start address where the image is to be copied on SRAM.|
|FREE_SRAM_AREA_SIZE|Defines maximum size of the image that can be flashed.|
|APP_RAM_START_ADDR|Defines M4 execution address.|
|FFE_CFG_ADDR|Defines FFE configuration address.|



**2** <u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Boot Loader Rev. 1.0_** 

#### **3.2 Configuring S3** 

To configure S3, edit the board_chandlar.c file, located in the directory Sources/Boards/Src/Chandlar as follows: 

**1.** Configure the pads (pinmux). 

**2.** Create a Flash Partition table for S3. 

**3.** Initialize user-specific hardware, such as the display in board_init(). 

**4.** Configure SPI and UART. 

The following subsection provides more detailed information on these steps. 

##### **3.2.1 Configuring the Pads** 

Configure pads in the GPIOInitTab array. Following is a snippet of UART pin configuration for S3. 

PadConfig GPIOInitTab[]= {… …. 

{ PAD_44, PAD44_FUNC_SEL_UART_TXD, PAD_CTRL_SRC_A0, PAD_MODE_OUTPUT_EN, PAD_NOPULL, PAD_DRV_STRENGHT_4MA, PAD_SLEW_RATE_SLOW, PAD_SMT_TRIG_DIS}, ///* PAD_45 - MCU_UART_RXD */ 

{ PAD_45, PAD45_FUNC_SEL_UART_RXD, PAD_CTRL_SRC_A0, PAD_MODE_INPUT_EN, PAD_PULLUP, PAD_DRV_STRENGHT_4MA, PAD_SLEW_RATE_SLOW, PAD_SMT_TRIG_DIS}, }; 

<u>www.quicklogic.com</u> **3** • • • ••• 

© 2017 QuickLogic Corporation 

**<mark>PRELIMINARY</mark>** 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Boot Loader Rev. 1.0_** 

##### **3.2.2 Configuring a Flash Partition Table** 

Configure a Flash Partition table for S3 in the board file using the Flash Partition table data structure (i.e., struct tag) in the pit.h file, located in directory /Sources/Core/Inc/. 

struct tag { char imageName[MAX_IMG_NAME]; /* fill this from PIT */ unsigned int flash_offset; /* fill this from PIT */ unsigned int max_img_size; /* fill this from PIT */ unsigned int sram_load_address; /* fill this from load table */ unsigned int actual_size; /* fill this from load table */ }; 

Partition table defined for chandlar: struct tag tags[MAX_TAGS] = { {TAG_NAME_BL_IMG, 0x000000, 0x8000  /* 32K */ ,  0, 0,          }, {TAG_NAME_FABRIC_IMG, 0x040000, 0x20000 /* 128K */,  0, 0,          }, {TAG_NAME_FFE_IMG, 0x020000, 0x20000 /* 128K */,  0, 0,          }, {TAG_NAME_M4_APP_IMG, 0x060000, 0x80000 /* 512K */,  0, 400 * 1024, }, {TAG_NAME_PIT_IMG, PIT_FLASH_OFFSET, PIT_MAX_SIZE /* 4K*/, 0, 0, }, }; 

##### **3.2.3 Adding Board-Specific Functions** 

Add board-specific functions in board_init(). 

//Customer Specific H/W init for Board Chandlar. void board_init() { } 

**4** <u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Boot Loader Rev. 1.0_** 

##### **3.2.4 Configuring UART** 

Configure the UART parameters (such as Baud rate, parity, etc.) in the uartSetup() function. 

uint32_t uartSetup() { UartHandler uartObj; uartObj.baud        = BAUD_460800; uartObj.wl          = WORDLEN_8B; uartObj.parity      = PARITY_NONE; uartObj.stop        = STOPBITS_1; uartObj.mode        = TX_RX_MODE; uartObj.hwCtrl      = HW_FLOW_CTRL_DISABLE; uartObj.intrMode    = UART_INTR_ENABLE; uartHandlerUpdate(&uartObj); uartInit(&uartObj); return 0; } 

##### **3.2.5 Configuring the SPI Master** 

Configure the SPI Master in the SPIM_Setup(void) function. 

void SPIM_Setup(void) { //SPI master init for SPI flash SpiHandle.Init.ucFreq       = SPI_BAUDRATE_10MHZ; SpiHandle.Init.ucSPIInf     = SPI_4_WIRE_MODE; SpiHandle.Init.ucSPIMode    = SPI_MODE_0; SpiHandle.Init.ucSSn        = SPI_SLAVE_1_SELECT; SpiHandle.Init.ulCLKPhase   = SPI_PHASE_1EDGE; SpiHandle.Init.ulCLKPolarity = SPI_POLARITY_LOW; SpiHandle.Init.ulDataSize   = SPI_DATASIZE_8BIT; SpiHandle.Init.ulFirstBit   = SPI_FIRSTBIT_MSB; SpiHandle.ucSPIx            = SPI1_MASTER_SEL; } 

<u>www.quicklogic.com</u> **5** • • • ••• 

© 2017 QuickLogic Corporation 

**<mark>PRELIMINARY</mark>** 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Boot Loader Rev. 1.0_** 

### **4.0 Adding a Flash Driver** 

To add a flash driver: 

**1.** Use the data structure defined for flash and FlashTable. 

struct eoss3_spi_flash { const char *name; UINT32_t page_size; UINT32_t (*read)( UINT32_t offset, size_t len, void *buf, void (*ptrFunc)(void )); UINT32_t (*write)(UINT32_t offset, size_t len, void *buf, void (*ptrFunc)(void )); UINT32_t (*erase)( UINT32_t offset, size_t len); UINT32_t (*erase_op_status)(); UINT32_t (*write_op_status)(); }; static const struct { const UINT8_t idcode;  //Identification code of Flash memory UINT32_t (*probe) ( UINT8_t *idcode); //Probe function of specific flash memory. }FlashTable[]; 

**2.** The new flash driver-specific read, write and erase must be mapped to a generic read, write and erase SPI interface. 

**Table 2** provides a description of the flash driver and SPI interface files. 

Table 2: Flash Driver and SPI Interface Files 

|**Filename**|**Directory**|**Description**|
|---|---|---|
|Spi_flash.h|Sources/Core/Inc/|Header for Spi_flash.c.|
|Spi_flash.c|Sources/Core/Src/|SPI Flash generic interface to call any flash-specific read, write and<br>erase functionality.|
|Eoss3_hal_spi.c|Sources/HAL/Src/|HAL API for SPI interface.|
|Eoss3_hal_spi.h|Sources/HAL/Inc/|Header for Eoss3_hal_spi.h.|
|Eoss3_mcx_spiflash.h|Sources/Boards/Flash/Inc/|Header for Eoss3_hal_mcx_spiflash.c.|
|Eoss3_mcx_spiflash.c|Sources/ Boards/Flash /Src/|Functionality of Macronix flash driver read, write and erase.|



**6** <u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Boot Loader Rev. 1.0_** 

**3.** Add the following entry of the Macronix flash used for the S3 RDB in the flashtable array. The following config is enabled for the S3 RDB. 

#define DEFINED_SPI_FLASH_MACRONIX    //Macronix flash used 

//Add an entry for flash in flashtable array defined in spi_flash.c 

flashtable[] = { 

**#ifdef DEFINED_SPI_FLASH_MACRONIX** 

**{0xc2, spi_flash_probe_macronix},** 

**#endif** #ifdef DEFINED_SPI_FLASH_GIGA {0xc8, spi_flash_probe_macronix}, #endif {0, NULL,}, }; 

**4.** Add the Macronix Flash driver. The following files consist of the Macronix driver. 

   - Eoss3_mcx_spiflash.h 

   - Eoss3_mcx_spiflash.c 

**5.** Add the user-specific functionality of read, write and erase in the flash driver, and map them to a generic SPI flash interface in the Macronix probe function. 

When adding new flash device support, include driver files. The Macronix flash driver is an example. 

<u>www.quicklogic.com</u> **7** • • • ••• 

© 2017 QuickLogic Corporation 

**<mark>PRELIMINARY</mark>** 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Boot Loader Rev. 1.0_** 

#### **4.1 Flash Probe Functionality** 

SPI_flash_Probe invokes the driver probe of the specific flash defined for the S3 RDB. 

spi_flash_probe_macronix is invoked for board_chandlar and it maps the driver-specific read, write and erase functionality to a generic SPI read, write and erase interface. 

UINT32_t spi_flash_probe_macronix(UINT8_t *idcode) { unsigned int i; unsigned int flash_size; unsigned long sector_size; int ret = FlashNotFound; UINT16_t id = (idcode[2] | (idcode[1] << 8)); …………. …………. …………. **flash.name = params->name; flash.page_size=params->page_size; flash.read=macronix_read_fast; flash.write=macronix_write; flash.erase=macronix_erase; flash.erase_op_status=macronix_erase_status; flash.write_op_status=macronix_write_status;** ……. …… return ret; } 

Refer to EOSS3_mcx_spiflash.c for Macronix flash-specific read, write and erase operations. 

**8** <u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Boot Loader Rev. 1.0_** 

### **5.0 Flash Operation Application Programming Interfaces (APIs)** 

UINT32_t spi_flash_read(UINT32_t offset, size_t len, void *buf, void (*ptrFunc)(void )); 

|This API is|called to read from f|lash memory|
|---|---|---|
|Param|offset|Flash Offset|
|Param|len|number of bytes to be read|
|Param|buf|pointer to buffer|
|Param|void (*ptrFunc)(void )|If param is NULL, then it is a blocking|
|||call. Else the pass callback is used to|
|||notify about the completion of read|
|||operation.|
|Return|int|Returns Flashstatus|



UINT32_t spi_flash_write(UINT32_t offset, size_t len, void *buf, void (*ptrFunc)(void )); 

|This API is|called to write to the|flash memory|
|---|---|---|
|Param|offset|Flash Offset|
|Param|len|number of bytes to be written|
|Param|buf|pointer to buffer|
|Param|void (*ptrFunc)(void )|If param is NULL, then it is a blocking|
|||call. Else the pass callback is used to|
|||notify about the completion of write|
|||operation.|
|Return|int|Returns Flashstatus|



UINT32_t spi_flash_erase(UINT32_t offset, size_t len); 

|This API is|called|to erase to the|flash memory|
|---|---|---|---|
|Param|offset||Flash Offset|
|Param|len||number of bytes to be erased|
|Return|int||Returns Flashstatus|



<u>www.quicklogic.com</u> **9** • • • ••• 

© 2017 QuickLogic Corporation 

**<mark>PRELIMINARY</mark>** 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Boot Loader Rev. 1.0_** 

UINT32_t spi_flash_erase_op_status(); 

This API is called to check status of erase operation issued to flash memory Return int Returns Flashstatus 

UINT32_t spi_flash_write_op_status() 

This API is called to check status of write operation issued to flash memory Return int Returns Flashstatus 

Refer to these APIs in file spi_flash.c. 

The following are the flash status: 

typedef enum { FlashOperationSuccess=1, FlashWriteRegFailed, FlashTimeOut, FlashIsBusy, FlashQuadNotEnable, FlashAddressInvalid, FlashInvalidParams, FlashCmdFailed, FlashMatchFound, 

FlashNotFound, }ReturnMsg; 

###### **NOTE:** 

- S3 uses the Read call as a blocking call, and the Write call as a nonblocking call. 

- Boot loader and M4 UART Baud rate settings are different. When M4 boots up, change the Baud rate to 115200 to see M4 logs. 

**10** <u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Boot Loader Rev. 1.0_** 

### **6.0 Contact Information** 

Phone: (408) 990-4000 (US) +(44) 1932-21-3160 (Europe) +(886) 26-603-8950 (Taiwan) +(86) 21-2116-0532 (China) +(81) 3-5875-0547 (Japan) +(82) 31-601-4225 (Korea) 

E-mail: <u>info@quicklogic.com</u> Sales: <u>America-sales@quicklogic.com Europe-sales@quicklogic.com Asia-sales@quicklogic.com Japan-sales@quicklogic.com Korea-sales@quicklogic.com</u> 

Support: <u>www.quicklogic.com/support</u> 

Internet: <u>www.quicklogic.com</u> 

### **7.0 Revision History** 

|**Revision**|**Date**|**Originator and Comments**|
|---|---|---|
|1.0|August 2017|Preliminaryrelease.|



### **8.0 Notice of Disclaimer** 

QuickLogic is providing this design, product or intellectual property "as is." By providing the design, product or intellectual property as one possible implementation of your desired system-level feature, application, or standard, QuickLogic makes no representation that this implementation is free from any claims of infringement and any implied warranties of merchantability or fitness for a particular purpose. You are responsible for obtaining any rights you may require for your system implementation. QuickLogic shall not be liable for any damages arising out of or in connection with the use of the design, product or intellectual property including liability for lost profit, business interruption, or any other damages whatsoever. QuickLogic products are not designed for use in life-support equipment or applications that would cause a life-threatening situation if any such products failed. Do not use QuickLogic products in these types of equipment or applications. 

QuickLogic does not assume any liability for errors which may appear in this document. However, QuickLogic attempts to notify customers of such errors. QuickLogic retains the right to make changes to either the documentation, specification, or product without notice. Verify with QuickLogic that you have the latest specifications before finalizing a product design. 

<u>www.quicklogic.com</u> **11** • • • ••• 

© 2017 QuickLogic Corporation 

**<mark>PRELIMINARY</mark>** 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Boot Loader Rev. 1.0_** 

### **9.0 Copyright and Trademark Information** 

Copyright © 2017 QuickLogic Corporation. All Rights Reserved. 

The information contained in this document is protected by copyright. All rights are reserved by QuickLogic Corporation. QuickLogic Corporation reserves the right to modify this document without any obligation to notify any person or entity of such revision. Copying, duplicating, selling, or otherwise distributing any part of this product without the prior written consent of an authorized representative of QuickLogic is prohibited. 

QuickLogic is a registered trademark and the QuickLogic logo is a trademark of QuickLogic. Other trademarks are the property of their respective companies. 

•• •••• 

**12** <u>www.quicklogic.com</u> **<mark>PRELIMINARY</mark>** •• •••• 

© 2017 QuickLogic Corporation 

