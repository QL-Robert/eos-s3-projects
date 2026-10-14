---
title: "Technical Writer"
source_file: "QL Application Note 148 QL S3 DSPC Noise Suppression and Beamforming Integration Guide.pdf"
pages: 9
sha256: 094923bfbf44f96bacfa616b432203cd775ce6e6019a95cfcb5fee8daf4ec07c
---

# Technical Writer

# **QuickLogic**<sup>**®**</sup> **EOS S3 – DSP** — QuickLogic’” **Concepts, Inc. Noise Suppression and Beamforming Integration Guide** <mark>NS</mark> 

**• • • • • • QuickLogic Application Note 148** 

## **Introduction** 

This document explains the implementation and integration of the DSP Concepts, Inc. (DSPC) audio processing technologies in QuickLogic’s OPEN 2018.1 RC1 release. This release has successfully integrated the 2-microphone beamforming (BF) and noise suppression (NS) solution in the Open Platform™ firmware stack. The audio data processed by DSPC’s AWE Core™ can be used in multiple high-end applications that handle processed audio data, but the AWE Core does not do the audio processing. Integration with the QuickLogic/Sensory<sup>®</sup> framework improves the detection rate of a key phrase in noisy environments. 

**Table 1** describes some of the terminology used in this document. 

Table 1: Terminology 

|**Name**|**Description**|
|---|---|
|AWE Core|DSPC’s embedded, dynamically-configured audio-processing engine|
|Audio Weaver|DSPC’s audio processing technology|
|Audio Weaver Binary (AWB) File|DSPC’s schematics, the building blocks of DSPC’s audio processing|
|Beamforming<br>~~a~~|An audio processing technology<br>~~(|~~|
|DSP Concepts (DSPC)<br>|Third-party partner of QuickLogic<br>|
|EOS S3|QuickLogic’s EOS S3 sensor processing platform|
|FreeRTOS|A real-time operating system kernel for embedded devices|
|Noise Tech.<br>~~a~~|DSPC’s composition of DSP algorithms<br>~~(|~~|
|Noise Suppression<br>|An audio preprocessing scheme to remove background noise from the<br>captured audio data<br>|
|OPEN 2018.1 RC1|QuickLogic’s Integrated 2-microphone beamforming and noise suppression<br>solution|
|Open Platform|The developer platform used in QuickLogic’s EOS S3 multi-platform firmware<br>stack|
|Sensory, Inc.<br>~~a~~|Third-party partner of QuickLogic<br>~~(|~~|
|Sensory VR Engine/Sensory VR<br>|Sensory’s library, voice recognition software<br>|



## **DSPC AWE Core** 

DSPC’s Audio Weaver<sup>®</sup> tools and AWE Core™ voice user interface (UI) libraries provide audio processing technologies such as multi-microphone beamforming, noise suppression and noise cancellation. The combined audio processing technologies extend QuickLogic’s low power sound detector (LPSD) audio engine capabilities to multiple voice-based applications with reliable audio data. 

<u>www.quicklogic.com</u> **1** ••• ••• 

© 2018 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 – DSP Concepts, Inc. Noise Suppression and Beamforming Integration Guide Rev. 1.3_** 

## **Beamforming and Noise Suppression Integration** 

BF and NS are integrated into an existing QuickLogic audio framework that also includes QuickLogic’s LPSD IP and Sensory’s voice recognition (VR) engine. The raw audio data of 16-bit samples at 16 kHz from QuickLogic’s voice IP engine is processed by DSPC libraries to provide BF and NS audio data. This processed data is sent to the QuickLogic/Sensory framework to perform key phrase detection (KPD) in Sensory’s VR engine. 

### **QuickLogic’s Voice Subsystem** 

The existing QuickLogic voice subsystem provides KPD in Sensory’s library (also known as Sensory’s VR engine), where the pulse-code modulation data is captured from the LPSD hardware (HW) and provided to Sensory’s VR engine for KPD. Sensory’s voice processing output is sent to the voice applications. 

Figure 1: QuickLogic Voice Subsystem 



<!-- Start of picture text -->
QL Voice Subsystem<br>QL Voice Framework<br>Voice IP  QL Audio  Voice<br>and  Framework  Sensory Lib  Applications<br>LPSD HW<br><!-- End of picture text -->

#### **LPSD HW** 

QuickLogic’s EOS S3 LPSD HW supports low power acoustic activity detection along with QuickLogic’s voice IP. The IP performs pulse-density modulation (PDM) to pulse-code modulation (PCM) conversion in mono and stereo modes. The raw audio data is sent to QuickLogic’s audio framework for further processing. 

#### **QuickLogic Audio Framework** 

QuickLogic’s audio framework is comprised of various components. This includes capturing audio data from the voice IP, processing the captured audio data, and interfacing with different voice applications using an application programming interface (API). 

#### **Sensory Library** 

Sensory’s voice processing engine performs KPD from the provided audio stream. 

#### **Voice Applications** 

Voice applications refer to various FreeRTOS applications that use QuickLogic’s voice framework to utilize the processed audio data and other voice-related functionalities provided. 

**2** <u>www.quicklogic.com</u> •• •••• 

© 2018 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 – DSP Concepts, Inc. Noise Suppression and Beamforming Integration Guide Rev. 1.3_** 

### **DSPC Noise Suppression and Beamforming** 

DSPC’s AWE Core is the third-party audio processing engine that supports audio processing using a composition of DSPC algorithms to deliver highly effective voice command features to voice-based applications. QuickLogic’s OPEN 2018.1 RC1 release integrates DSPC’s AWE Core and voice UI with support for 2-microphone NS and BF. 

DSPC’s AWE Core is integrated into QuickLogic’s voice subsystem to process the raw audio data from the voice IP. The composition of DSPC’s algorithms, (here after referred to as Noise Tech.), is applied on the captured PCM samples to provide fine-tuned and highly reliable voice commands to voice applications. 

#### **Integrating Noise Tech. into QuickLogic's Voice Subsystem** 

Noise Tech. supports a 2-microphone solution in stereo mode on QuickLogic’s EOS S3 sensor processing platform with NS and BF. The audio data captured from the Voice IP is sent for Noise Tech. DSP processing. The processed data can be used for various other voice processing. 

**Figure 2** shows an example of KPD using Sensory’s VR engine. 

Figure 2: Example: Key Phrase Detection Using Sensory’s VR Engine 



<!-- Start of picture text -->
Voice IP  QL Audio   DSPC AWE<br>LPSD HW   Framework   Core  Sensory Lib<br>QL Voice Framework<br> Voice<br>Applications<br>QL Voice Sub System<br><!-- End of picture text -->

#### **Noise Tech. Components** 

The Noise Tech. integration comprises of the following modules: 

- AWB schematics – the Init commands 

- Audio data conversion – 16-bit to 32-bit and vice versa 

- AWE Core processing – the Noise Tech. DSP processing 

##### **AWB Schematics** 

The Audio Weaver binary (AWB) file, (also known as schematics), are the building blocks of DSPC’s audio processing. The schematics are generated from the Audio Weaver tool. See Audio Weaver documentation for tool usage and schematic generation. 

<u>www.quicklogic.com</u> **3** • • • ••• 

© 2018 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 – DSP Concepts, Inc. Noise Suppression and Beamforming Integration Guide Rev. 1.3_** 

The AWB schematic contains the configuration commands to the DSPC libraries in the system. These are provided as initialized commands to the DSPC libraries when the system starts. QuickLogic’s OPEN 2018.1 RC1 release supports precompiled AWB schematics only for NS and BF. 

##### **Audio Data Conversion** 

The AWE processing is performed with 32-bit audio data. Since EOS S3 voice IP provides 16-bit PCM samples, the captured samples must be converted to 32-bit PCM samples for AWE processing. The AWE processed data is converted back to 16-bit PCM samples for further processing. 

##### **AWE Processing** 

The AWE processing is performed with a sample size of 80, which is 5 ms audio data. The voice IP is configured to provide 2-microphone PCM data in stereo mode. This data is continuously captured by the audio framework and provided to AWE processing every 5 ms. The data from the audio framework is 16-bit stereo, which is converted to stereo mode 32-bit PCM data. The AWE processing takes the converted 5 ms data in the INPUT_CHANNEL and provides Noise Tech. processed output data in the OUTPUT_CHANNEL. For every audio sample given in the INPUT_CHANNEL, a processed audio sample is expected from the OUTPUT_CHANNEL. The processed output data is in the mono mode 32-bit PCM data. This data is again converted into 16-bit PCM data for further processing. The mono mode 16-bit PCM is further used for Sensory’s VR engine processing in the current design. 

**Figure 3** depicts the audio data flow from the PDM microphones to the AWE Core audio processing engine. 

Figure 3: Audio Data Flow from the PDM Microphones to the AWE Core Audio Processing Engine. 



<!-- Start of picture text -->
S3 Reference Design Board<br>LPSD<br>‘ FIFOs DMA pay FW BE) (NE) | VR<br>:<br>PDM2PCM L i AW<br>e ‘ H \ i 32 bit fract<br>s SO \ 32 bit float<br>AS. “| 32 bit float stereo float @16k<br>ws. 16bit PCM stereo samples @ 16000Hz<br>PDM sigma-delta bits @1MHz (= 64x16000kHz)<br><!-- End of picture text -->

##### **Noise Suppression** 

NS is an audio preprocessing scheme to remove background noise from the captured audio data. Where noise refers to all the sound sources in that environment other than the intended source audio data capture. 

##### **Beamforming** 

BF is an audio processing technology from the voice UI powered by Audio Weaver, which uses multiple microphones to focus on sounds coming from the user’s direction and ignores other sounds. 

**4** <u>www.quicklogic.com</u> •• •••• 

© 2018 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 – DSP Concepts, Inc. Noise Suppression and Beamforming Integration Guide Rev. 1.3_** 

### **M4 Firmware Update** 

The M4 firmware update for AWE Core integration is incorporated in the OPEN 2018.1 RC1 release. The project update to M4 firmware is depicted in **Figure 4** . 

Figure 4: M4 Firmware Update 



<!-- Start of picture text -->
Debug v<br>Files aoe<br>©) @Qlt_OpenPlatform_DsPc - D... ¥<br>HH mialgoLib<br>1 lllApp e<br>MicMSIS AWB Schematics files for Noise<br>Wi FReeRTOSv8_2_2 e Suppression and Beam forming<br>MAL e<br>Miqisrc e<br>el Mischematics<br>| He mibt_snr<br>bf_test<br>i bf_thf_bypass e<br>| “a Simic_test<br>| ©|iliVendorisPES<br>Gre outpu DSPC core platform files , DSPC<br>Configuration and Processing<br>QL_OpenPlatform_DSPC<br><!-- End of picture text -->

#### **Audio Framework Updates** 

The major updates to the audio framework and buffer handling are: 

- Audio frame size is 80 frames for Noise Tech. processing 

- Voice IP is enabled for PDM 2-microphone stereo support in dual-buffer mode 

#### **Configuration in Open Platform** 

The current release OPEN 2018.1 RC1 supports DSPC Noise Tech. in the Host Voice and Hearable firmware stacks of Open Platform. 

To enable DSPC support in the M4 firmware source, refer to the Open Platform user guide documents. 

- _Build_Configuration_Information.xls_ 

- _AWE_SW_Configuration.docx_ 

<u>www.quicklogic.com</u> **5** • • • ••• 

© 2018 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 – DSP Concepts, Inc. Noise Suppression and Beamforming Integration Guide Rev. 1.3_** 

#### **Setting Up the Hardware** 

The solution implemented supports two microphones, NS and BF. 

To use the Noise Tech. feature: 

**1.** Connect two external microphones to the S3 Reference Design Board. 

**2.** Connect the external microphone array as shown in **Figure 5** . 

**3.** Remove jumper P13 to use the external microphone array board on S3 Reference Design Board. 

Figure 5: Setting Up the Hardware 



<!-- Start of picture text -->
Protection  jumper<br><!-- End of picture text -->

### **Power Consumption and MIPS Measurements** 

The power consumption and million instructions per second (MIPS) are measured in Host Voice mode configuration with Sensory’s 64 KB combined model file and with the 32 KB Alexa model, as shown in **Table 2** through **Table 5** . Refer to _DSPC_MIPS_MEMORY_Power_Measurement.xlsx_ . 

Table 2: MIPS Measurement for 2-Microphone Beamforming with DSPC Noise Tech. 

|**Build Configuration**|**Sensory Model File**|**Sensor**|**MIPS**<br>**DSPC BF**<br>**and NS**|**Total MIPS**|
|---|---|---|---|---|
|Host Voice + DSPC Noise Tech. enabled|64 KB combined,<br>Alexa + VG|23.5|20.5|44|
|Host Voice + DSPC Noise Tech. enabled|32 KB,<br>Alexa|15.5|20.5|36|



**6** <u>www.quicklogic.com</u> •• •••• 

© 2018 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 – DSP Concepts, Inc. Noise Suppression and Beamforming Integration Guide Rev. 1.3_** 

Table 3: Power Measurement for 2-Microphone Beamforming with DSPC Noise Tech. @ 1.0V 

|**Build Configuration**|**Sensory Model File**|**LPSD**|**KPD**|
|---|---|---|---|
|Host Voice + DSPC Noise Tech. enabled|64 KB combined,<br>Alexa + VG|220 µA|3.56 mA|
|Host Voice + DSPC Noise Tech. enabled|32 KB,<br>Alexa|220 µA|2.56 mA|



Table 4: Host Voice Memory Footprint for 2-Microphone Beamforming with DSPC Noise Tech. 

|**Build Configuration**|**Command**<br>**Set**<sup>**a**</sup>|**Code**|**Memory**<br>**Data**|**(in Bytes)**<br>**Total Used**|**Free**|
|---|---|---|---|---|---|
|Host Voice + DSPC Noise Tech.<br>(64 KB combined model, Alexa + VG)|Not Enabled|325272|176088|501360|22928|
|Host Voice + DSPC Noise Tech.<br>(32 KB model, Alexa)|Not Enabled|295316|176032|471348|52940|
|Host Voice + DSPC Noise Tech<br>(64 KB combined model, Alexa + VG +<br>EnglishFullMusic01 CMD)|Enabled|327224|176027|503251|21037|
|Host Voice + DSPC Noise Tech<br>(64 KB combined model, Alexa + VG +<br>Bluetooth CMD)|Enabled|318216|176027|494243|30045|



a. When the Command Set is enabled the Command Controller is also loaded, this accounts for the difference in the memory footprint. 

Table 5: Hearable Memory Footprint for 2-Microphone Beamforming with DSPC Noise Tech. 

|**Build Configuration**|**Command**<br><sup>**a**</sup>||**Memory**|**(in Bytes)**||
|---|---|---|---|---|---|
||**Set**|**Code**|**Data**|**Total Used**|**Free**|
|Hearable + DSPC Noise Tech.<br>(64 KB combined model, Alexa + VG)|Enabled|325100|176108|501208|23080|
|Hearable + DSPC Noise Tech.<br>(32 KB model, Alexa)|Not Enabled|293512|176108|469620|54668|
|Hearable + DSPC Noise Tech<br>(64 KB combined model, Alexa + VG +<br>EnglishFullMusic01 CMD)|Enabled|325112|176108|501220|23068|
|Hearable + DSPC Noise Tech<br>(64 KB combined model, Alexa + VG +<br>Bluetooth CMD)|Enabled|316104|176108|492212|32076|



a. When the Command Set is enabled the Command Controller is also loaded, this accounts for the difference in the memory footprint. 

<u>www.quicklogic.com</u> **7** • • • ••• 

© 2018 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 – DSP Concepts, Inc. Noise Suppression and Beamforming Integration Guide Rev. 1.3_** 

## **Contact Information** 

Phone: (408) 990-4000 (US) +(44) 1932-21-3160 (Europe) +(886) 2-6603-8947 (Taiwan) +(86) 139-0517-5302 (China) +(81) 3-5875-0547 (Japan) +(82) 31-601-4225 (Korea) 

E-mail: <u>info@quicklogic.com</u> Sales: <u>America-sales@quicklogic.com Europe-sales@quicklogic.com Asia-sales@quicklogic.com Japan-sales@quicklogic.com Korea-sales@quicklogic.com</u> 

Support: <u>www.quicklogic.com/support</u> 

Internet: <u>www.quicklogic.com</u> 

## **Revision History** 

|**Revision**|**Date**|**Originator and Comments**|
|---|---|---|
|1.0|April 2018|Aravindhan Ashok and Kathleen Bylsma|
|1.1|May2018|Aravindhan Ashok and Kathleen Bylsma|
|1.2|May2018|Marc Miller and Kathleen Bylsma|
|1.3|May 2018|Marc Miller and Kathleen Bylsma<br>Added Table 5.|



## **Notice of Disclaimer** 

QuickLogic is providing this design, product or intellectual property "as is." By providing the design, product or intellectual property as one possible implementation of your desired system-level feature, application, or standard, QuickLogic makes no representation that this implementation is free from any claims of infringement and any implied warranties of merchantability or fitness for a particular purpose. You are responsible for obtaining any rights you may require for your system implementation. QuickLogic shall not be liable for any damages arising out of or in connection with the use of the design, product or intellectual property including liability for lost profit, business interruption, or any other damages whatsoever. QuickLogic products are not designed for use in life-support equipment or applications that would cause a life-threatening situation if any such products failed. Do not use QuickLogic products in these types of equipment or applications. 

QuickLogic does not assume any liability for errors which may appear in this document. However, QuickLogic attempts to notify customers of such errors. QuickLogic retains the right to make changes to either the documentation, specification, or product without notice. Verify with QuickLogic that you have the latest specifications before finalizing a product design. 

**8** <u>www.quicklogic.com</u> •• •••• 

© 2018 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 – DSP Concepts, Inc. Noise Suppression and Beamforming Integration Guide Rev. 1.3_** 

## **Copyright and Trademark Information** 

Copyright © 2018 QuickLogic Corporation. All Rights Reserved. 

The information contained in this document is protected by copyright. All rights are reserved by QuickLogic Corporation. QuickLogic Corporation reserves the right to modify this document without any obligation to notify any person or entity of such revision. Copying, duplicating, selling, or otherwise distributing any part of this product without the prior written consent of an authorized representative of QuickLogic is prohibited. 

QuickLogic is a registered trademark, and Aurora, ArcticPro, and the QuickLogic logo are trademarks of QuickLogic. Other trademarks are the property of their respective companies. 

<u>www.quicklogic.com</u> **9** • • • ••• 

© 2018 QuickLogic Corporation 

