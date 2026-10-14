---
title: "QuickLogic\u00ae EOS S3 Real-Time Operating System (RTOS) Porting Guide"
source_file: "QL Application Note 135 \u2013 RTOS Porting Guide.pdf"
pages: 9
sha256: 52eabb32d066565f4fc4f3c40497afa0e69fba71d5ca18db911400a1a75f7f36
---

# QuickLogic® EOS S3 Real-Time Operating System (RTOS) Porting Guide

# **QuickLogic**<sup>**®**</sup> **EOS S3 Real-Time Operating System (RTOS) Porting Guide** <mark>SS</mark> 

**• • • • • • QuickLogic**<sup>**®**</sup> **Application Note 135** 

## **1.0 Introduction** 

This document provides information and instruction for porting an RTOS on an EOS S3 sensor processing platform. This guide describes the porting process, tools, development environment setup and required modifications. 

## **2.0 Prerequisites and Setup** 

This section describes the prerequisites for porting RTOS activity. 

### **2.1 RTOS Source Code** 

The base software development kit (SDK), RTOS source code, which includes support for the Cortex M4F CPU core. 

### **2.2 Target Board** 

The EOS S3 sensor processing platform employs an Ultra-Low Power Sensor Hub (ULPSH), Flexible Fusion Engine (FFE) for Always-On tasks, a Cortex M4 floating-point processor for resource-intensive tasks, and a Programmable Fabric for the implementation of additional technologies. 

The EOS S3 provides: 

- Operating speeds that range from 2 MHz to 80 MHz 

- 512 KBytes SRAM supporting multiple power modes including deep sleep 

- Programmable logic equivalent to 2,400 effective logic cells 

- Flexible Fusion Engine (FFE) which is ideal for always-on, real-time sensor fusion algorithms (such as pedometer, activity classification and others). 

- Interfaces that include: 

   - SPI Master, SPI Slave, I<sup>2</sup> S Master, I<sup>2</sup> S Slave and I<sup>2</sup> C 

   - Pulse Density Modulation (PDM) to Pulse Code Modulation (PCM) conversion and Low Power Sound Detect (LPSD) voice support 

   - Audio support for PDM or I<sup>2</sup> S microphones 

   - Sensor Interrupts 

   - GPIO 

   - UART 

••• ••• 

**<mark>PRELIMINARY</mark>** 

© 2017 QuickLogic Corporation 

<u>www.quicklogic.com</u> **1** 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 Real-Time Operating System (RTOS) Porting Guide Rev. 1.0_** 

The Target board connects to the Host computer, and provides connectivity using the following connections: 

- JTAG connect with serial wire debug (SWD) – For debugging and programming the flash memory. 

- UART– A console to view trace messages for a program in execution and for debugging. 

The EOS S3 platform supports the following environment: 

- Host computer with Windows<sup>®</sup> OS 

- IAR Systems<sup>®</sup> ARM<sup>®</sup> toolchain supporting Cortex<sup>®</sup> M4F processor (target) 

### **2.3 Setting Up the Cross Development Platform** 

**Figure 1** illustrates the cross development platform setup. 

Figure 1: Cross Development Platform Setup 



<!-- Start of picture text -->
STAG CONNECTION USING SWD<br>HOST<br>TARGET<br>BOARD<br>UART CABLE<br><!-- End of picture text -->

The Host system installation prerequisites are: 

- Cross compilation tool set up for Cortex M4F 

- J-Link tool support drivers 

- Prolific<sup>®</sup> USB to serial driver 

- Tera Term to view the UART console logs 

The Target board installation prerequisites are: 

- EOS S3 

The Host system to Target board connection prerequisites are: 

- UART cable 

- SEGGER J-Link hardware and J-Link software for debugging 

**<mark>PRELIMINARY</mark>** 

**2** <u>www.quicklogic.com</u> •• •••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 Real-Time Operating System (RTOS) Porting Guide Rev. 1.0_** 

### **2.4 Porting the RTOS on EOS S3** 

#### **2.4.1 Overview** 

The basic steps of the porting process are as follows: 

**1.** Download and install the RTOS SDK that supports the Cortex M4F processor on the EOS S3. 

**2.** Download the ARM toolchain for Cortex M4F architecture. 

**3.** Configure the RTOS as per the Target board and EOS S3. 

**4.** Compile the RTOS source. 

**5.** Flash the binary on the Target board. 

#### **2.4.2 Porting the RTOS** 

To build a portable RTOS: 

**1.** Download the toolchain to compile code for the EOS S3. 

**2.** Configure the RTOS for EOS S3. 

   - **a.** Make changes in the port files. 

   - **b.** Make GPIO configurations according to the board schematics. 

**3.** Compile the RTOS kernel using the cross compiler. 

**4.** Once the code has been successfully compiled, flash the binary using the QuickLogic Flash Image tool. 

##### **2.4.2.1 Features** 

The main features implemented for EOS S3 are: 

- Clock domain initialization. 

- Peripheral drivers (GPIO, UART, timers, SPI, I<sup>2</sup> C, etc.). 

- Interrupt vector table definition. 

- C library functions such as fgetc() and fputc() to use UART console. 

##### **2.4.2.2 Porting Activity Requirements** 

To port the RTOS on the EOS S3: 

**1.** Determine the system architecture, and compiler-related porting of the assembly file from the RTOS code base according to the build IDE used. 

**2.** Determine what files needs to be changed or mapped. 

**3.** Configure the board support package (BSP) according to the board schematics. (This is independent of the RTOS.) 

**4.** Test the code. 

• • • ••• 

© 2017 QuickLogic Corporation 

<u>www.quicklogic.com</u> **3** 

**<mark>PRELIMINARY</mark>** 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 Real-Time Operating System (RTOS) Porting Guide Rev. 1.0_** 

##### **2.4.2.2.1 Determine the Architecture** 

The purpose of determining the system architecture requirements is to identify software components that need to be modified to get the RTOS working. 

The EOS S3 has a Cortex M4F CPU core, the RTOS code base must be downloaded and the relevant port of M4F used for the RTOS. 

##### **2.4.2.2.2 Identify the Changes that Need to be Mapped** 

Identify the changes to be mapped: 

- Map the interrupt vector table definition. 

- Map the .icf file (linker). 

- Customize the idle loop according to EOS S3. 

- Map the C library printf function to UART. 

##### **2.4.2.2.3 Make the Changes that Need to be Mapped** 

Perform the following steps: 

**1.** Interrupt Vector Table: 

The CMSIS-compliant file EOSS3B_startup.s contains an interrupt vector table (also called the exception vector table) starting usually at address 0x00000000, typically in ROM. The vector table contains the initialization value for the main stack pointer on reset, and the entry point addresses for all exception handlers. The exception number defines the order of entries in the vector table. 

**4** <u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 Real-Time Operating System (RTOS) Porting Guide Rev. 1.0_** 

The ARM Cortex-M architecture requires the user to place the initial Main Stack pointer and the addresses of all exception handlers and interrupt service routines (ISRs) into the Interrupt Vector Table allocated typically in ROM. In the IAR compiler, the interrupt descriptor table (IDT) is initialized in the EOSS3B_startup.s. The following is the snippet from the file EOSS3B_startup.s. 

MODULE ?cstartup ;; Forward declaration of sections. SECTION CSTACK:DATA:NOROOT(3) SECTION .intvec:CODE;NOROOT(2) EXTERN __iar_program_start EXTERN SystemInit PUBLIC __vector_table DATA __vector_table DCD sfe(CSTACK) PUBLIC __reset_vector __reset_vector: DCD Reset_Handler /* Reset Handler */ DCD NMI_Handler /* NMI Handler */ DCD HardFault_Handler /* Hard Fault Handler */ DCD MemManage_Handler /* MPU Fault Handler */ DCD BusFault_Handler /* Bus Fault Handler */ DCD UsageFault_Handler /* Usage Fault Handler */ DCD 0 /* Reserved */ DCD 0 /* Reserved */ DCD 0 /* Reserved */ DCD 0 /* Reserved */ DCD SCV_Handler /* SVCall Handler */ DCD DebugMon_Handler /* Debug Monitor Handler*/ DCD 0 /* Reserved */ DCD PendSV_Handler /* PendSV Handler*/ DCD SysTick_Handler /* SysTick Handler*/ 

The EOSS3B_startup.s file contains all the vector definitions. The reset handler is defined as follows: 

|Reset_Handler||
|---|---|
|LDR<br>RO|, =SystemInit|
|BLX<br>RO||
|LDR<br>RO|, =__iar_program_start|
|BX<br>RO||



During system startup, an initialization sequence is performed before the main function is entered. 

When the M4F CPU is reset, it jumps to reset the vector and starts executing the reset handler, which in turns starts executing at the label __iar_program_start. After performing the initialization it calls the main function. The following shows the flow of how main function is called. 

• • • ••• 

© 2017 QuickLogic Corporation 

<u>www.quicklogic.com</u> **5** 

**<mark>PRELIMINARY</mark>** 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 Real-Time Operating System (RTOS) Porting Guide Rev. 1.0_** 



<!-- Start of picture text -->
__iar_program_start<br>__cmain<br>main<br><!-- End of picture text -->

Similarly, for the IDE which is used for porting the RTOS on EOS S3, map the reset handler accordingly to invoke the main function. 

The entire file must be mapped according to the tool chain IDE used for the new RTOS. 

**2.** Map the .icf File (Linker File): 

Map the .icf file to the tool chain IDE used for the new RTOS. 

This file typically contains the information about the where each memory region (such as code, data and stack) are placed in the SRAM. 

**3.** Define the macro __NVIC_PRIO_BITS: 

The Cortex Microcontroller Software Interface Standard (CMSIS) provides the macro, __NVIC_PRIO_BITS, which specifies the number of NVIC priority bits defined in a given ARM CortexM implementation. 

For EOS S3 this is defined as 3 in eoss3_dev.h file as shown in the following: 

#define __NVIC_PRIO_BITS 3 /*!< Tamar uses 3 Bits for the Priority Levels */ 

**4.** Set the Interrupt Priority: 

The CMSIS provides the NVIC_SetPriority() function to set the priority of an interrupt. 

The following macro is used in NVIC_SetPriority by some peripherals for defining the interrupt priority: 

#define configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY 5 

For example, in the eoss3_hal_audio.c file, the NVIC_SetPriority function is used to set the priority of an LPSD interrupt. 

NVIC_SetPriority(Lpsd_IRQn, configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY); 

This macro is specific to the FreeRTOS only, but still must be defined for porting on the new RTOS as some of the peripheral drivers are using it. 

**5.** Configuration: 

Configure the BSP according to the board schematics. 

**6.** C Library Changes: 

Map the C library printf function to direct output to the UART console. 

**6** <u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 Real-Time Operating System (RTOS) Porting Guide Rev. 1.0_** 

The changes for this have been done in the C_lib_retarget.c file. 

FILE __stdout; FILE __stdin; int **fgetc** (FILE * file) { return uartrx(); } int **fputc** (int ch, FILE * file) { uartrx(ch); return ch; } 

The following is the call flow of the library function printf in IAR which is mapped to the uarttx function. 

uarttx fputc [_Prout + 0xb] [_PrintfSmallNoMb + [printf + 0x19] 

Similarly, it must be mapped to the uarttx function according to the IDE used for development. 

**7.** Test: 

Once the above changes are compiled, check the executables by running on a board to verify that basic functionalities (such as the UART) are working. 

Create some test code to test the port to check the RTOS functionality. 

<u>www.quicklogic.com</u> **7** • • • ••• 

© 2017 QuickLogic Corporation 

**<mark>PRELIMINARY</mark>** 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 Real-Time Operating System (RTOS) Porting Guide Rev. 1.0_** 

## **3.0 Contact Information** 

Phone: (408) 990-4000 (US) +(44) 1932-21-3160 (Europe) +(886) 26-603-8950 (Taiwan) +(86) 21-2116-0532 (China) +(81) 3-5875-0547 (Japan) +(82) 31-601-4225 (Korea) 

E-mail: <u>info@quicklogic.com</u> Sales: <u>America-sales@quicklogic.com Europe-sales@quicklogic.com Asia-sales@quicklogic.com Japan-sales@quicklogic.com Korea-sales@quicklogic.com</u> 

Support: <u>www.quicklogic.com/support</u> 

Internet: <u>www.quicklogic.com</u> 

## **4.0 Revision History** 

|**Revision**|**Date**|**Originator and Comments**|
|---|---|---|
|1.0|August 2017|Preliminaryrelease.|



## **5.0 Notice of Disclaimer** 

QuickLogic is providing this design, product or intellectual property "as is." By providing the design, product or intellectual property as one possible implementation of your desired system-level feature, application, or standard, QuickLogic makes no representation that this implementation is free from any claims of infringement and any implied warranties of merchantability or fitness for a particular purpose. You are responsible for obtaining any rights you may require for your system implementation. QuickLogic shall not be liable for any damages arising out of or in connection with the use of the design, product or intellectual property including liability for lost profit, business interruption, or any other damages whatsoever. QuickLogic products are not designed for use in life-support equipment or applications that would cause a life-threatening situation if any such products failed. Do not use QuickLogic products in these types of equipment or applications. 

QuickLogic does not assume any liability for errors which may appear in this document. However, QuickLogic attempts to notify customers of such errors. QuickLogic retains the right to make changes to either the documentation, specification, or product without notice. Verify with QuickLogic that you have the latest specifications before finalizing a product design. 

**8** <u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 Real-Time Operating System (RTOS) Porting Guide Rev. 1.0_** 

## **6.0 Copyright and Trademark Information** 

Copyright © 2017 QuickLogic Corporation. All Rights Reserved. 

The information contained in this document is protected by copyright. All rights are reserved by QuickLogic Corporation. QuickLogic Corporation reserves the right to modify this document without any obligation to notify any person or entity of such revision. Copying, duplicating, selling, or otherwise distributing any part of this product without the prior written consent of an authorized representative of QuickLogic is prohibited. 

QuickLogic is a registered trademark and the QuickLogic logo is a trademark of QuickLogic. Other trademarks are the property of their respective companies. 

<u>www.quicklogic.com</u> **9** • • • ••• 

© 2017 QuickLogic Corporation 

**<mark>PRELIMINARY</mark>** 

