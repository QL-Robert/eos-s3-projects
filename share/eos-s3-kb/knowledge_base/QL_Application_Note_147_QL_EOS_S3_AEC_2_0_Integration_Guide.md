---
title: "Technical Writer"
source_file: "QL Application Note 147 \u2013 QL EOS S3 AEC 2.0 Integration Guide.pdf"
pages: 5
sha256: d93a608c342473d67cfe24b7c70b418077a699763758735acfc1985977d44e71
---

# Technical Writer

# **QuickLogic**<sup>**®**</sup> **EOS S3 AEC 2.0 Integration Guide** 

**• • • • • • QuickLogic Application Note 147** 

## **Overview** 

In an embedded device that has the capability of voice recognition and music playback, the music playback can interfere with voice recognition. In these types of devices, Acoustic Echo Cancellation (AEC) can help in canceling/suppressing the music playback signal so that the voice signal is clear and ideal for Key Phrase Detection. 

QuickLogic provides a solution for low power, always-on voice recognition. QuickLogic EOS S3 supports the AEC feature using Consilient Technology<sup>®</sup> Acoustic Echo Cancellation software. 

## **AEC in EOS S3 Architecture** 

**Figure 1** shows the various blocks involved in AEC. Clock synchronization is employed to synchronize the reference and microphone signals by adjusting the EOS S3 HSOSC clock. 

The AEC software has a 64 msec tail and is intended for music playback suppression/cancellation, rather than phone calls. To get the reference signal from the speaker, the I<sup>2</sup> S lines of the speaker are tapped and sent to the EOS S3. Audio datapaths internal to the EOS S3 run at 16 kHz. If the incoming signal is at 48 kHz, it can be decimated to 16 kHz by the EOS S3 FPGA Fabric. 

Figure 1: AEC in EOS S3 Architecture 



<!-- Start of picture text -->
PDM MIC  DMA audio  EOS S3 with AEC<br>data to SRAM<br>AEC library to process  AEC processed audio  Sensory<br>near- and far-end signal data to Sensory  detec�on detection<br>s<br>Speaker 48 kHz to 16 kHz  DMA audio<br>(Reference<br>Signal) decima�on data to SRAM FABRIC<br>MIC mono channel  I2S mono channel<br>15 ms data @16 kHz AEC processed data 15 ms audio data @16 kHz Third-party library<br><!-- End of picture text -->

**<mark>PRELIMINARY</mark>** 

<u>www.quicklogic.com</u> **1** ••• ••• 

© 2018 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 AEC 2.0 Integration Guide Rev. 1.0_** 

## **AEC Configurations** 

The following configurations are required to enable AEC. **Table 1** lists the configurations that must be defined in the Fw_global_config.h file. 

Table 1: AEC Configuration 

|**Parameter**|**Description**|
|---|---|
|AEC_ENABLED|Enables the AEC.|
|AEC_2_0|Enables AEC 2_0 feature (which has decimation in the Fabric).|
|ENABLE_I2S_SLAVE_FB_RX|Enables receiving data via the I<sup>2</sup>S Slave using the Fabric.|
|FB_ENABLE_CLK_SYNC|Enables clock synchronization between the microphone and I<sup>2</sup>S (reference)<br>signal.|



**Table 2** lists the main files for AEC configuration. 

Table 2: AEC Main Files 

|**Filename**|**Description**|
|---|---|
|ql_AecTask.c|This file has the AEC Task used to begin the AEC process.|
|eoss3_hal_fabric_i2s_slave.c|This file has the code for configuring I<sup>2</sup>S lines and SDMA for receiving the<br>reference signal. The audio data is sent to AEC Task for further processing.|
|Eoss3_hal_audio.c|This file configures the microphone to receive the microphone data, which is<br>then passed the AEC Task for further processing.|
|eoss3_hal_fabric_clk_sync.c|This file has the code for synchronizing I<sup>2</sup>S and microphone samples using a<br>clock synchronization method.|



**2** <u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2018 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 AEC 2.0 Integration Guide Rev. 1.0_** 

## **I**<sup>**2**</sup> **S PAD Configurations** 

The following lines must be configured as shown below to receive a reference signal over I<sup>2</sup> S. These lines can be changed according to the Fabric design. 

PadConfig padcfg; /* AP I2S WD CLK IN */ padcfg.ucPin = **PAD_6** ; padcfg.ucFunc = PAD6_FUNC_SEL_FBIO_6; padcfg.ucCtrl = PAD_CTRL_SRC_FABRIC; padcfg.ucMode = PAD_MODE_INPUT_EN; padcfg.ucPull = PAD_NOPULL; padcfg.ucDrv = PAD_DRV_STRENGHT_4MA; padcfg.ucSpeed = PAD_SLEW_RATE_SLOW; padcfg.ucSmtTrg = PAD_SMT_TRIG_DIS; HAL_PAD_Config(&padcfg); /* AP I2S DOUT */ padcfg.ucPin = **PAD_10** ; padcfg.ucFunc = PAD10_FUNC_SEL_FBIO_10; padcfg.ucCtrl = PAD_CTRL_SRC_FABRIC; padcfg.ucMode = PAD_MODE_INPUT_EN; padcfg.ucPull = PAD_NOPULL; padcfg.ucDrv = PAD_DRV_STRENGHT_4MA; padcfg.ucSpeed = PAD_SLEW_RATE_SLOW; padcfg.ucSmtTrg = PAD_SMT_TRIG_DIS; HAL_PAD_Config(&padcfg); /* AP I2S CLK IN */ padcfg.ucPin = **PAD_8** ; padcfg.ucFunc = PAD8_FUNC_SEL_FBIO_8; padcfg.ucCtrl = PAD_CTRL_SRC_FABRIC; padcfg.ucMode = PAD_MODE_INPUT_EN; padcfg.ucPull = PAD_NOPULL; padcfg.ucDrv = PAD_DRV_STRENGHT_4MA; padcfg.ucSpeed = PAD_SLEW_RATE_SLOW; padcfg.ucSmtTrg = PAD_SMT_TRIG_DIS; HAL_PAD_Config(&padcfg); 

• • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2018 QuickLogic Corporation 

<u>www.quicklogic.com</u> **3** 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 AEC 2.0 Integration Guide Rev. 1.0_** 

When not in AEC mode configure the I2S CLK IN pin in Interrupt mode, which serves as an interrupt pin and configures the system in to AEC mode when there is an incoming music signal. 

GPIOCfgTypeDef  xGpioCfg; xGpioCfg.usPadNum = PAD_8; xGpioCfg.ucGpioNum = GPIO_2; xGpioCfg.ucPull = PAD_PULLDOWN; xGpioCfg.ucFunc = PAD8_FUNC_SEL_SENS_INT_2; 

xGpioCfg.intr_type = EDGE_TRIGGERED;//EDGE_TRIGGERED or LEVEL_TRIGGERED; xGpioCfg.pol_type = RISE_HIGH;//flip the trigger level HAL_GPIO_IntrCfg(&xGpioCfg); 

## **Adjusting the AEC Parameter** 

The tunable parameter for AEC is the BulkDelay, which is the difference between the reference and microphone signals. This must be calculated by setting the following parameter accordingly in the file ql_aecTask.c in function aecTaskHandler (). 

AECCtrlParams.BulkDelay = 35; 

BulkDelay can be calculated by taking a dump of the reference and microphone samples, then calculating by how many milliseconds the reference signal leads the microphone signal. 

## **Contact Information** 

Phone: (408) 990-4000 (US) +(44) 1932-21-3160 (Europe) +(886) 2-6603-8947 (Taiwan) +(86) 139-0517-5302 (China) +(81) 3-5875-0547 (Japan) +(82) 31-601-4225 (Korea) E-mail: <u>info@quicklogic.com</u> Sales: <u>America-sales@quicklogic.com Europe-sales@quicklogic.com Asia-sales@quicklogic.com Japan-sales@quicklogic.com Korea-sales@quicklogic.com</u> Support: <u>www.quicklogic.com/support</u> Internet: <u>www.quicklogic.com</u> 

**4** <u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2018 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 AEC 2.0 Integration Guide Rev. 1.0_** 

## **Revision History** 

|**Revision**|**Date**|**Originator and Comments**|
|---|---|---|
|1.0|April 2018|Jayachandra Gowda and Kathleen Bylsma|



## **Notice of Disclaimer** 

QuickLogic is providing this design, product or intellectual property "as is." By providing the design, product or intellectual property as one possible implementation of your desired system-level feature, application, or standard, QuickLogic makes no representation that this implementation is free from any claims of infringement and any implied warranties of merchantability or fitness for a particular purpose. 

You are responsible for obtaining any rights you may require for your system implementation. QuickLogic shall not be liable for any damages arising out of or in connection with the use of the design, product or intellectual property including liability for lost profit, business interruption, or any other damages whatsoever. QuickLogic products are not designed for use in life-support equipment or applications that would cause a life-threatening situation if any such products failed. Do not use QuickLogic products in these types of equipment or applications. 

QuickLogic does not assume any liability for errors which may appear in this document. However, QuickLogic attempts to notify customers of such errors. QuickLogic retains the right to make changes to either the documentation, specification, or product without notice. Verify with QuickLogic that you have the latest specifications before finalizing a product design. 

## **Copyright and Trademark Information** 

Copyright © 2018 QuickLogic Corporation. All Rights Reserved. 

The information contained in this document is protected by copyright. All rights are reserved by QuickLogic Corporation. QuickLogic Corporation reserves the right to modify this document without any obligation to notify any person or entity of such revision. Copying, duplicating, selling, or otherwise distributing any part of this product without the prior written consent of an authorized representative of QuickLogic is prohibited. 

QuickLogic is a registered trademark, and Aurora, ArcticPro, and the QuickLogic logo are trademarks of QuickLogic. Other trademarks are the property of their respective companies. 

<u>www.quicklogic.com</u> **5** • • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2018 QuickLogic Corporation 

