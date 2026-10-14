---
title: "Technical Writer"
source_file: "QL S3 Android M ASSP - Always On Keyphrase Detection Performance and Validation Methods AN 131.pdf"
pages: 12
sha256: 67f0823f4a0f15f195d8f5c466794e3d3dde72132b89a04c17bd3d8a2766ddf5
---

# Technical Writer

**QuickLogic**<sup>**®**</sup> **S3 Android M ASSP Always-On Keyphrase Detection Performance and Validation Methods** <mark>SS</mark> 

**• • • • • • Application Note 131** 

## **Introduction** 

The QuickLogic S3 Android M Application-Specific Standard Product (ASSP) is an always-on solution that enables original equipment manufacturers (OEMs) to bring the lowest power and highest accuracy Keyphrase Detection (KPD) to the mobile phone industry. This turnkey solution includes: 

- S3 Android M ASSP. 

- Linux drivers. 

- Android hardware abstraction layer (HAL). 

- Example Android application package (APK). 

The following technologies have been integrated to achieve this solution: 

- Heterogeneous processing – includes a power-optimized M4 processor core and granular power management of clock rates, subsystems, and memory blocks. Granular control of memories allow OEMs to optimize the number of seconds of audio buffering after the keyphrase. 

- Pulse-density modulation (PDM) – allows two channels of PDM microphones. This module was designed to support multi-mode low power digital microphones running at 512 kHz for low power operation. 

- Digital hardware bypass (with no software required) – automatically switches between always-on Keyphrase Detection (KPD) mode, and voice communication use cases where the clock is driven by the Audio CODEC. 

- Hardware low power sound detection (LPSD) – detects sound in the environment allowing the M4 to shut down when there is no keyphrase detected. A profiling application feature of the evaluation APK allows for data logging and real-time visualization of the LPSD versus KPD states. 

- Sensory Inc. – TrulyHandsFree™ trigger has over 95% accuracy without false fires even in high noise and speech. The trigger is supported in multiple languages. Software configuration and model options allow OEMs to easily make power versus performance trade-offs. 

••• ••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

<u>www.quicklogic.com</u> **1** 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Android M ASSP Always-On Keyphrase Detection Performance and Validation Methods – Rev. 1.0_** 

## **Keyphrase Detection Fundamentals** 

### **Keyphrase Detection Algorithm Types** 

The QuickLogic S3 Android M ASSP with Sensory’s TrulyHandsFree supports several types of KPD algorithms. these include: 

- Fixed Trigger (FT) 

- Enrollment Fixed Trigger (EFT) 

- User Defined Trigger (UDT) 

- TrulySecure™ Speech Verification (TSSV) 

- TrulySecure™ 

Each algorithm gives the OEM a choice of different functionality and has differing performance assessment methods such as a trigger phrase or user-defined trigger phrase, as well as the amount of authentication needed. 

**Figure 1** shows the difference in authentication and user involvement for the KPD algorithms. 

Figure 1: Keyphrase Detection Algorithm Types 



<!-- Start of picture text -->
TrulySecure™<br>- Host authentication for speech<br>- Host authentication for face*<br>*Camera cequired<br>Authentication<br>TrulySecure™ Speech Verification TrulySecure<br>- Host authentication for speech<br>- User or OEM choice of keyword<br>User-Defined Trigger TSSV<br>- User choice of keyword<br>Enrollment Fixed Trigger - Embedded speaker verification<br>- User trailing required - Performance Varies (keyword, person)<br>- Speaker verification<br>- OEM choice of keyword<br>EFT UDT<br>Easier for user and  Higher user involvement<br>lower processing and processing<br>FT<br>Fixed Trigger<br>- No user trailing required<br>- OEM choice of keyword<br>- Works for any talker<br>Any User<br><!-- End of picture text -->



<!-- Start of picture text -->
PRELIMINARY<br><!-- End of picture text -->

**2** <u>www.quicklogic.com</u> •• •••• 

© 2016 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Android M ASSP Always-On Keyphrase Detection Performance and Validation Methods – Rev. 1.0_** 

### **Keyphrase Algorithm Performance** 

With multiple vendors providing KPD performance information in different formats, it is important for OEMs to use the same the performance metrics and test methods to measure the solutions in-house with the same method. This provides comparable information and allows the OEM to select the best solution. KPD performance consists of two fundamental aspects; power consumption and algorithm accuracy. 

#### **Power Consumption Calculation** 

The power consumption impact of KPD calculations must be performed in “real-world” conditions, using a measured percentage mix of LPSD and KPD states. These measurements must be converted to a current at the battery, which includes the DC/DC regulator loses, to understand the impact on the standby current of the phone. Microphone power depends on the selected microphone, and also contributes to the total current of the KPD solution. **Table 1** defines the generic power measurement characteristics for always-on KPD. 

Table 1: KPD Power Consumption Characteristics 

|**Symbol**|**Description**|
|---|---|
|VIC|Processor supply voltage (V)|
|LPSDDuty|Percent of time in LPSD mode|
|KPDDuty|Percentage of time in KPD mode|
|ILSPD|LPSD mode current at the processor (mA at VIC)|
|IKPD|KPD mode current at the processor (mA at VIC)|
|VBAT|Battery supply voltage (V)|
|DCDC|Switching regular efficiency converting VBATto VIC|
|IBAT|Battery current consumption (mA at VBAT)|



<u>www.quicklogic.com</u> **3** • • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Android M ASSP Always-On Keyphrase Detection Performance and Validation Methods – Rev. 1.0_** 

#### **Power Measurement Calculation Parameters** 

The power measurement calculation for the battery current is: 

IBAT = (VIC x ((LPSDDuty x ILPSD) + (KPDDuty x IKPD))/DCDC)/VBAT 

For the QuickLogic S3 Android M ASSP, the evaluation platform can be used to measure the ILPSD and IKPD to verify the values in **Table 2** . The LPSDDuty and KPDDuty values can be measured by selecting _Voice Session Logging_ from the _S3 voice evaluation app._ 

**Table 2** defines the actual S3 Android M ASSP power measurement for always-on KPD. 

Figure 2: S3 Android M ASSP Power Characteristics 

|**Parameter**|**S3 Android M ASSP**|
|---|---|
|VIC|1V|
|LPSDDuty|60% (estimates used for benchmarking purposes)|
|KPDDuty|40% (estimates used for benchmarking purposes)|
|ILSPD|130 µA|
|IKPD|1,000 µA<sup>a</sup>|
|VBAT|4V|
|DCDC|85%|
|IBAT|1V x (130 µA x 0.6)+(1,000 µA x 0.4) / 0.85/ 4V = 140 µA<sup>a</sup>at 4V|



a. The measured current varies with model size, and when other features are enabled such as motion processing. 

#### **Algorithm Accuracy** 

KPD performance is characterized and measured as a False Rejection Rate (FRR) in an environment with a particular number of False Acceptance (FA) occurrences. This is typically in a clean (low noise) environment and controlled noise field. 

For authentication, the number of Intrusion Acceptances (IAs) with a statistically significant number of speakers is used to characterized the effectiveness of the authentication. **Table 2** shows the KPD accuracy performance metrics. 

Table 2: KPD Algorithm Accuracy 

|**Keyphrase Detection Accuracy**|**Performance Metric**|
|---|---|
|Poor recognition|FRR = Total number of phrases not recognized / Total number of phrases<br>Recognition accuracy = 1 - FRR<br>Measure the FRR in (1) quiet and (2) noisy conditions<br>100+ phrase utterances|
|Trigger with other speech|FA occurrences = Number of FAs that occur in continued speech when the<br>phrase is not spoken<br>100+ hours of continuous speech|
|Authentication failure|IA occurrences - Number of occurrences an imposter (person different from<br>the enrolled user) is able to trigger and authenticate<br>100+ imposter utterances, different genders and ages|



**4** <u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Android M ASSP Always-On Keyphrase Detection Performance and Validation Methods – Rev. 1.0_** 

#### **Algorithm Tuning** 

To be successful in the fast moving mobile market, OEMs must be able to tune the KPD algorithm quickly to avoid time-consuming tasks such as collecting numerous recordings or relying on a vendor to fine-tune a fixed keyphrase only to find out it does not work, or triggers too often. The S3 Android M ASSP with TrulyHandsFree addresses this need by providing FA/FR tuning options, which allow the OEM to make these trade-offs in a single release. **Figure 3** shows the first tuning parameter with FA/FR. 

Figure 3: First Tuning Parameter 



<!-- Start of picture text -->
False<br>Rejection OEM-provided tuning points to choose trade-off<br>Example:<br>Yellow (noise) = 1 FA per day, 20% FRs<br>Yellow point (clean) = 1 FA per day, 5% FRs<br>Noisy Environment<br>Clean Environment<br>False<br>Lower Better Acceptance<br><!-- End of picture text -->

<u>www.quicklogic.com</u> **5** • • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Android M ASSP Always-On Keyphrase Detection Performance and Validation Methods – Rev. 1.0_** 

For enrolled and user-defined fixed triggers, the OEM can choose how stringent the configurable thresholds are for the speaker verification confirmation. **Table 3** lists the KPD algorithm performance metrics. 

Table 3: Algorithm Performance 



<!-- Start of picture text -->
Index Parameter Requirement<br>1 Fixed Trigger (FT) Performance Validation QuickLogic KPD<br>delivery01_OKQL_2.html<br>“OK QuickLogic” keyphrase search index 5 target point (red<br>performance<br>below graph), delivery01_OKQL_2 release.<br>Clean Environment:<br>Clean Targets :<br>False Accepts: 0.28/h<br>- False Rejects: 1.17%<br>Noise Targets:<br>1.1 FT False Acceptances (FA) 28 ±3 FA target<br>Note:  28 FA = 0.28 FA/hour x 100 hours ±10%.<br><!-- End of picture text -->



<!-- Start of picture text -->
PRELIMINARY<br><!-- End of picture text -->

**6** <u>www.quicklogic.com</u> •• •••• 

© 2016 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Android M ASSP Always-On Keyphrase Detection Performance and Validation Methods – Rev. 1.0_** 

Table 3: Algorithm Performance _(Continued)_ 

|**Index**|**Parameter**|**Requirement**|
|---|---|---|
|**1.2**|**FT False Rejection Rate (FRR)**<br>Statistically significant recordings of keyphrases are needed<br>Clean Environment –100 utterances from different people<br>(20 people, 5 times each).<br>Noise Environment – Same clean corpus with noise being<br>played on noise environment loudspeaker. The noise type and<br>level (measured as a Signal to Noise Ratio (SNR)) can be<br>modified.<br>The minimum validation requirements are 12 dB SNR Car and<br>12 dB SNR Babble to reflect mobile handheld devices.<br>FRR = 1 – Number of acceptances/100 total utterances.<br>**Note:**The Clean 1.17% False Rejection Rate and Noise 1.79%<br>False Rejection rate are targets from Sensory frontier graph<br>release notes of “OK QuickLogic.”|Clean: 1% ±0.5%<br>12 dB SNR Car: 2% ±1%<br>12 dB SNR Babble: 5% ±1%<br>**Note:**See**Table 6**.|
|**2**|**Enrollment Fixed Trigger (EFT) Performance Validation**<br>**Note:**Test setup assumes a “cooperative” user (follows<br>enrollment instructions, clear speech) and “good” training (quiet<br>environment).|Verify significant reduction of FA<br>compared to FT keyphrase<br>Verify low IAs|
|**2.1**|**EFT False Acceptances**<br>Same test procedure as 1.1.|Lower FA than fixed trigger.|
|**2.2**|**EFT False Rejection Rate**<br>Clean Environment – 30 utterances from the same person.<br>5 People<br>Noise Environment – Same EFT clean corpus with noise being<br>played on noise environment loudspeaker. The noise type and<br>level (measured as a Signal to Noise Ratio (SNR)) can be<br>modified.<br>The minimum validation requirements are 12 dB SNR Car and<br>12dB SNR Babble to reflect mobile handheld devices.<br>FRR = Number of rejections/30 total utterances.|Measure FRR.|
|**2.3**|**EFT Imposter Acceptances (IA)**<br>Clean Environment – 100 utterances from the non-enrollment<br>different people (20 people, 5 times each) shall be tested against<br>the enrolled model. Any false keyphrase detection of these non-<br>enrolled users shall be considered an Imposter Acceptance.<br>**Note:**Gender and accent will affect results.<br>**Note:**TSSV will have the same test case. Expect a low IA rate<br>when TSSV is running.|Measure IA|
|**3**|**User Defined Trigger (UDT)**<br>Keyphrase must have >10 phonemes.<br>Due to the significantly different FA/FRR performance of UDTs<br>based on the phonetic content, UDT functionally shall only be<br>tested functionally.||



<u>www.quicklogic.com</u> **7** • • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Android M ASSP Always-On Keyphrase Detection Performance and Validation Methods – Rev. 1.0_** 

## **Measuring Keyphrase Detection Performance** 

### **Test Environment Description (Audio Lab)** 

The goal of the test environment is to create a lab to accurately and repeatedly reproduce speech and sound environments. This allows for comparing solutions, seeing improvement, and simulating performance in different environments. 

The lab recommendation is based on the “ETSI Room” treatment to a conference room. Validation of a KPD algorithm is supported by the S3 Android M ASSP. It does not require all four loudspeakers and sound equipment described in the _ETSI EG 202 396-1_ specification as the intent is only to duplicate the acoustic environment of the room. 

Place a host computer outside the room, with a cable port (or under the door) for routing of the loudspeaker playback, to ensure tests can be started and stopped without interruption. This type of laboratory is shown in **Figure 4** . 

Figure 4: Example of ETSI Room Lab 



### **Voice Laboratory - ETSI Room Details** 

**Table 4** provides the measurable room characteristics. Consistent room creation with the same equipment helps to ensure repeatability between laboratories. 

Table 4: ETSI Room Characteristics 

|**Index**|**Characteristic**|**Target Value**|
|---|---|---|
|1|Room Dimensions|Target: 3 m x 3 m, carpeted with no windows, and independent AC control.<br>ETSI Standard: 2.5 x 3 m and 3.5 x 4 m.<br>Room Height: between 2.20 m and 2.50 m|
|2|Noise Floor|Target: 50 dB SPL(A)<br>ETSI Standard: 30 dB SPL(A)|
|3|Reverberation (RT60)|Target: 500 ms<br>ETSI Standard: 200 ms to 700 ms|



# **<mark>PRELIMINARY</mark>** 

•• •••• 

© 2016 QuickLogic Corporation 

**8** <u>www.quicklogic.com</u> 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Android M ASSP Always-On Keyphrase Detection Performance and Validation Methods – Rev. 1.0_** 

Different labs should have comparable room sizes and when possible, be outfitted with the same equipment. The lab should be uninterruptible (lock/signage) and dedicated (equipment should not be moved in and out). 

The lab must have a table and fixture with the ability to have 1 to 20 devices in parallel. 

The table and fixture must have measurement and distances. SPL measurements at the microphones of the devices under test (DUT) and distance from loudspeakers must be noted for each device. **Table 5** describes the equipment requirements. 

Table 5: Equipment Requirements 

|**Equipment**|**Notes**|
|---|---|
|Loudspeakers|Two loudspeakers:<br>• Signal (voice) playback<br>• Noise playback to create acoustically mixed noise environment|
||Powered loudspeakers simplify equipment list.|
|SPL meter|Consumer grade SPL meter for measuring sound pressure levels.|
|Acoustic wall treatment|Affix sound treatment wedges to walls to control reverberation.|



### **Industry Lab and Test Signal References** 

Table 6: Industry Lab and Test Signal References 

|**Index**|**Name**|**Description**|
|---|---|---|
|1|Background Noise Corpus|• Babble Noise:<br>https://docbox.etsi.org/stq/Open/EG%20202%20396-<br>1%20Background%20noise%20database/Binaural_Signals/Pub_Noise<br>_Binaural_V2.wav<br>• Car Noise:<br>https://docbox.etsi.org/stq/Open/EG%20202%20396-<br>1%20Background%20noise%20database/Binaural_Signals/Midsize_Ca<br>r1_100Kmh_binaural%20(%200.00-30.00%20s).wav|
|||• These files should be normalized to a digital -26 dB FS level.<br>• Background noise audio files can be looped for continuous time to<br>create a longer audio file.|
|2|False Acceptance Corpus|• Collect 100 hours of audio containing continuous speech.<br>• Normalized to a digital 26 dB FS level.<br>• No specific industry standard benchmark.<br>• Record talk radio.|
|3|Fixed Trigger Test Corpus|• 100 of utterances with different people (20 people, 5 times each).|



<u>www.quicklogic.com</u> **9** • • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Android M ASSP Always-On Keyphrase Detection Performance and Validation Methods – Rev. 1.0_** 

### **Industry Standards Links** 

Table 7: Industry Standards Links 

|**Index**|**Name**|**Description**|
|---|---|---|
|1|ETSI Room (Section 6.1)|http://www.etsi.org/deliver/etsi_eg/202300_202399/20239601/0<br>1.02.02_60/eg_20239601v010202p.pdf|
|2|ETSI Background Noise|https://docbox.etsi.org/stq/Open/EG%20202%20396-|
||Database|1%20Background%20noise%20database|



## **Contact Information** 

Phone: (408) 990-4000 (US) +(44) 1932-21-3160 (Europe) +(886) 26-603-8950 (Taiwan) +(86) 139-0517-5302 (China) +(81) 3-5875-0547 (Japan) +(82) 31-601-4225 (Korea) E-mail: <u>info@quicklogic.com</u> Sales: <u>America-sales@quicklogic.com Europe-sales@quicklogic.com Asia-sales@quicklogic.com Japan-sales@quicklogic.com Korea-sales@quicklogic.com</u> 

Support: <u>www.quicklogic.com/support</u> Internet: <u>www.quicklogic.com</u> 

## **Revision History** 

|**Revision**|**Date**|**Originator and Comments**|
|---|---|---|
|1.0|November 2016|Taro Kimura and Kathleen Bylsma|



**<mark>PRELIMINARY</mark>** 

**10** <u>www.quicklogic.com</u> •• •••• 

© 2016 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Android M ASSP Always-On Keyphrase Detection Performance and Validation Methods – Rev. 1.0_** 

## **Notice of Disclaimer** 

QuickLogic is providing this design, product or intellectual property "as is." By providing the design, product or intellectual property as one possible implementation of your desired system-level feature, application, or standard, QuickLogic makes no representation that this implementation is free from any claims of infringement and any implied warranties of merchantability or fitness for a particular purpose. 

You are responsible for obtaining any rights you may require for your system implementation. QuickLogic shall not be liable for any damages arising out of or in connection with the use of the design, product or intellectual property including liability for lost profit, business interruption, or any other damages whatsoever. QuickLogic products are not designed for use in life-support equipment or applications that would cause a life-threatening situation if any such products failed. Do not use QuickLogic products in these types of equipment or applications. 

QuickLogic does not assume any liability for errors which may appear in this document. However, QuickLogic attempts to notify customers of such errors. QuickLogic retains the right to make changes to either the documentation, specification, or product without notice. Verify with QuickLogic that you have the latest specifications before finalizing a product design. 

<u>www.quicklogic.com</u> **11** • • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 Android M ASSP Always-On Keyphrase Detection Performance and Validation Methods – Rev. 1.0_** 

## **Copyright and Trademark Information** 

Copyright © 2016 QuickLogic Corporation. All Rights Reserved. 

The information contained in this document is protected by copyright. All rights are reserved by QuickLogic Corporation. QuickLogic Corporation reserves the right to modify this document without any obligation to notify any person or entity of such revision. Copying, duplicating, selling, or otherwise distributing any part of this product without the prior written consent of an authorized representative of QuickLogic is prohibited. 

QuickLogic is a registered trademark, and the EOS design and QuickLogic logo are trademarks of QuickLogic. Other trademarks are the property of their respective companies. 

•• •••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

**12** 

<u>www.quicklogic.com</u> 

