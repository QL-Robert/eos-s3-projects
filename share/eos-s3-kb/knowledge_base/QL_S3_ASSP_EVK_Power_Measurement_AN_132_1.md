---
title: "QuickLogic S3 Android M ASSP EVK Power Meausrement AB 132"
source_file: "QL S3 ASSP EVK Power Measurement AN 132  (1).pdf"
pages: 12
sha256: a6f6f67e3d3e42a31f383373235429e82e1e19d6505b6ad5bbecd3e2f838282d
---

# QuickLogic S3 Android M ASSP EVK Power Meausrement AB 132

# **QuickLogic**<sup>**®**</sup> **S3 ApplicationSpecific Standard Product (ASSP) Evaluation Kit (EVK) Power Measurement** <mark>SS</mark> 

**• • • • • • Application Note 132** 

### **Introduction** 

The S3 Android M ASSP is a comprehensive integrated solution for concurrent motion sensor and voice processing. This turn-key ASSP includes: 

- _Sensory TrulyHandsFree_ ™ voice control technology running on QuickLogic’s proprietary technology 

   - Low-power speech detection (LPSD) 

   - Keyphrase detection (KPD) 

   - Multiphrase command support 

- _CyWeeMotion_ intelligent motion sensing technology 

   - Sensor fusion 

   - Gesture recognition 

   - Context awareness 

   - Navigation (PDR Assist) 

- Ultra-low power 

   - Always-on, always-listening hardware-based sound recognition 

   - Power management unit minimizes power in all conditions 

   - Thirty-one independent, power islands 

- Software solution 

   - S3 Android M ASSP is completely preconfigured and preprogrammed 

   - Sensor hub software provided for inclusion in the Android application processor 

   - S3 Android Voice and Motion APKs provided for reference 

- S3 ASSP EVK 

   - Nexus 5 phone with Android M operating system configured with ASSP software, firmware and APKs 

   - QuickLogic Chandalar board connected to phone via USB port for power 

   - Voice and Motion APKs 

The application note provides instructions and information that enables an experienced and knowledgeable end-user to measure power consumption using the QuickLogic S3 ASSP EVK, Release 1.0. 

**<mark>PRELIMINARY</mark>** 

••• ••• 

© 2016 QuickLogic Corporation 

<u>www.quicklogic.com</u> **1** 

**_QuickLogic S3 ASSP EVK Power Measurement – Rev. 1.0_** 

### **Hardware Setup** 

As shown in **Figure 1** , the QuickLogic S3 ASSP EVK consists of: 

- Nexus 5 phone with the Android M operating system, configured with the proper ASSP firmware and applications (such as Motion, Voice, etc.) 

- QuickLogic Chandalar board, connecting the phone via special SPI wiring 

- USB OTG cable, connecting the phone USB port to the Chandalar USB connector 

- Plastic cover with cut-outs for DVDD current measurement and microphones 

- A calibrated high-speed digital multimeter (DMM) 

**NOTE:** Agilent 34461A and Keithley DMM7510 were used for data collection featured in this document. 

- Cables and connecting wires 

**WARNING:** Do not move the connecting wires, they are very delicate and easy to break. 

Figure 1: S3 ASSP EVK 



To obtain information, technical support, or to inquire about any support-related issue for a QuickLogic product, contact your local Field Application Engineer (FAE). 

**2** <u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

**_QuickLogic S3 ASSP EVK Power Measurement – Rev. 1.0_** 

#### **Current Measurement** 

##### **Setting Up the DMM** 

To set up the DMM: 

**1.** Remove the jumper at the plastic opening (P14). 

**2.** Connect the DMM probes to the two header pins, as shown in **Figure 2** . 

**3.** If mimicking motion during measurement, secure the cable connections by taping them to the plastic cover to avoid unintended disconnection. 

**4.** Turn on the DMM and set to the current measurement. 

**5.** If the DMM does not have fast response auto-range switching, do not use the auto-range setting. Set the DMM to a current range of 10 mA or 100 mA. 

**NOTE:** Consult the DMM user manual for accuracy for a particular setting current range. 

Figure 2: Hardware Setup Schematics 



<!-- Start of picture text -->
P14<br>Bee Re ee | i |<br>PE ae<br>DMM Probes<br><!-- End of picture text -->

##### **Powering On the EVK** 

To power on the EVK: 

**1.** Power on the Nexus 5 phone. 

The Nexus 5 phone comes with a fully charged battery right out of the box, and powers the PCB with an USB OTG cable. Charge the phone when the battery icon indicates low power. 

**2.** Touch the application icon on the phone screen to launch the pre-installed software application. 

• • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

<u>www.quicklogic.com</u> **3** 

**_QuickLogic S3 ASSP EVK Power Measurement – Rev. 1.0_** 

##### **Software Navigation** 

Using the pre-installed APK, Voice and/or Cywee, put the EVK in the desired operating condition before taking current measurements. See **Software Settings** on page 6 for instructions about how to put the EVK in various operating modes for current measurement. 

##### **DMM Current Reading** 

A simple DMM will provide a fluctuated number for current reading due to the S3 ASSP core current consumption based on the “CPU load,” especially when the EVK is performing motion sensor fusion computation or processing voice data. This applies to most low-cost hand-held instruments. 

With a hand-held DMM that is not capable of logging current readings, post data processing is required to get accurate average current consumption. 

For medium to high quality instruments that have a high sampling rate, the instrument provides minimum, average and maximum readings. 

- Minimum data: lowest current consumption (base) 

- Average data: accumulation of number of samples 

- Maximum data: peak current demand (for system power design consideration) 

In most cases, the DMM will collect data for 60 seconds and an average current measurement is obtained. This allows the DMM to collect enough samples to avoid skew in data results due to start of measurement. 

**NOTE:** In all cases, clearing the DMM reading is required to collect a new set of samples to post new measurement results. 

**4** <u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

**_QuickLogic S3 ASSP EVK Power Measurement – Rev. 1.0_** 

### **Power Consumption** 

**Table 1** through **Table 4** show power consumption measurements performed on the S3 ASSP reference design board. Developers can expect to measure similar current values at 25°C. Refer to the power optimized schematic available from QuickLogic. 

Table 1: Motion Sensor Only Power Consumption 

|**Mode**|**VDD at**<br>**1.0 V**|**AVDD at**<br>**1.8 V**|**Test Condition**|
|---|---|---|---|
|Step Counter|356 µA|14 µA|Step counter|
|9-Axis Sensor Fusion|840 µA|18 µA|Constant movement through 3-axis of Accel + Magneto +Gyro<br>sensors.|



Table 2: Voice Processing Only Power Consumption (Motion Sensor Algorithms Not Installed) 

|**Mode**|**VDD at**<br>**1.0 V**|**AVDD at**<br>**1.8 V**|**Test Condition**|
|---|---|---|---|
|LPSD|96 µA|14 µA|Listening, but not triggered (256 KB SRAM used, 1 trigger)|
|KPD|1,165 µA|16 µA|KPD triggered (phrase “OK QuickLogic”)|
|60% in LPSD, 40% KPD|524 µA||Typical use-case over a 24 hour period|



Table 3: Voice Processing Only Power Consumption (Motion Sensor Algorithms Idled) 

|**Mode**|**VDD at**<br>**1.0 V**|**AVDD at**<br>**1.8 V**|**Test Condition**|
|---|---|---|---|
|LPSD|281 µA|14 µA|Listening, but not triggered (512 KB SRAM used, 1 trigger)|
|KPD (“OK QuickLogic”)|1,165 µA|16 µA|KPD triggered (phrase “OK QuickLogic”)|
|60% in LPSD, 40% KPD|635 µA||Typical use-case over a 24 hour period|



Table 4: Concurrent Motion Sensor and Voice Processing Power Consumption (Typical) 

|**Mode**|**VDD at**<br>**1.0 V**|**AVDD at**<br>**1.8 V**|**Test Condition**|
|---|---|---|---|
|LPSD + Step Counter|384 µA|14 µA|Listening, but not triggered with active step counter|
|KPD + Step Counter|1,333 µA|16 µA|KPD triggered (phrase “OK QuickLogic”) with active step counter|
|60% in LPSD, 40% KPD<br>Detected + Step Counter|702 µA||Typical use-case over a 24 hour period with active step counter|



<u>www.quicklogic.com</u> **5** • • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

**_QuickLogic S3 ASSP EVK Power Measurement – Rev. 1.0_** 

### **Software Settings** 

#### **Step Counter** 

**NOTE:** Power cycle the EVK if the system has been used for Voice operations prior to measuring current consumption. The system power cycle (off/on) ensures all running applications are closed. 

To measure the step counter current consumption: 

**1.** Select (touch) the **2.** Touch Sensor List **3.** Scroll down, touch **4.** Select Cywee Step CyweeMotion icon to Demo. Cywee Step Counter. launch the preCounter and OK. **5.** Clear the DMM 

installed application. reading, wait for 60 seconds, and collect the average reading. 

**6.** De-select the Cywee Step Counter. 

**7.** Touch the Return button to return to the previous screen 

28 On ge: ne Geng BO Onde O Save tog 

iT e Sipe¥ SENSOR LIST DEMO O GyroscopeiaKe-0P) Uncalibrated * Bjarne voiceBak “ofl Significant Motion O nhamat © wt © came© rarest 2S Sle Sophie oe C1 cCyweestep Detector Ose ones 

Sata **Cywee icon** ge = ©; a step Cyweeotectr WAKE.Step Counter UP) **Select and de‐select** C Step Counter (WAKE_UP) 

e; [Geomagnetic Rotation **return** 

. OO cyweeTilt detector 

Rc **OK** 

## **<mark>PRELIMINARY</mark>** 

**6** <u>www.quicklogic.com</u> •• •••• 

© 2016 QuickLogic Corporation 

**_QuickLogic S3 ASSP EVK Power Measurement – Rev. 1.0_** 

#### **9-Axis Sensor Fusion** 

**NOTE:** Power cycle the EVK if the system been used for Voice operations prior to measuring current consumption. The system power cycle (off/on) ensures all running applications are closed. 

To measure the 9-axis sensor fusion current consumption: 



<!-- Start of picture text -->
1. Select (touch) the  2. Touch Car Demo. 3. Clear the DMM  4. Collect the average<br>CyweeMotion icon to  reading, wait for 60  reading.<br>launch the pre- seconds.<br>5. Touch the Return<br>installed application.<br>NOTE:  A moving car  button to return to the<br>will show a current  previous screen.<br>number similar to<br>what is shown in<br>Table 1  on page 5.<br>The current will be<br>lower if the EVK is<br>actually still in this<br>mode.<br>=e Oe Ber ze Os B62<br>3) SSiges:<br>pal e eae:<br>a ae => .<br>Cywee icon<br>: ~= <p ——sro-<br>g966<br><!-- End of picture text -->



<!-- Start of picture text -->
PRELIMINARY<br><!-- End of picture text -->

<u>www.quicklogic.com</u> **7** • • • ••• 

© 2016 QuickLogic Corporation 

**_QuickLogic S3 ASSP EVK Power Measurement – Rev. 1.0_** 

#### **Low Power Sound Detection (LPSD)** 

**NOTE:** Power cycle the EVK if the system been used for motion operations prior to measuring current consumption. The system power cycle (off/on) ensures all running applications are closed. 

To measure the LPSD current consumption: 



<!-- Start of picture text -->
1. Select (touch) the S3  2. Touch Keyphrase  3. Touch the Play 4. Clear the DMM<br>Voice Evaluation icon  Detection. button. The screen  reading and start a<br>to launch the pre- will go black.  new reading<br>installed application. Listening for the  sequence.<br>keyphrase “OK<br>5. Wait 60 seconds.<br>QuickLogic.” The<br>blue LED lights up on  6. Collect the average<br>the board to indicate  reading.<br>the system has gone<br>7. Touch the Return<br>into low power mode<br>button to return to the<br>(listening).<br>previous screen.<br>=. So GO mor I or gen<br>PLAY<br>—ae |<br>Voice icon bs > Voice enrollment<br>. 8 @@<br>qd ° o qd ° o d o} oa<br><!-- End of picture text -->

Figure 3: The Blue LED Lights Up on the Board to Indicate the System is in Low Power Mode 



<!-- Start of picture text -->
Green LED (Power)<br>spas uted<br>Pathe. --— flie fais<br>ft oles S Ges ine |<br>pec tsee emft) erece, |<br>Opening to P14 for VDD  Blue LED indicates HW is<br>current measurement  listening for sound<br><!-- End of picture text -->



<!-- Start of picture text -->
PRELIMINARY<br><!-- End of picture text -->

**8** <u>www.quicklogic.com</u> •• •••• 

© 2016 QuickLogic Corporation 

**_QuickLogic S3 ASSP EVK Power Measurement – Rev. 1.0_** 

#### **Keyphrase Detection (KPD)** 

**NOTE:** Do this step immediately after LPSD data measuring. 

To measure the KPD current consumption: 

**1.** Clear the DMM **2.** Make sound by **3.** Collect the average **5.** Speak the keyphrase reading. talking for 60 reading. “OK QuickLogic.” seconds; avoid The red LED lights up **4.** Touch the Return 

speaking the on the board when button to return to the 

keyphrase “OK the keyphrase is previous screen. 

QuickLogic.” detected and the Keyphrase Detection screen is displayed on the phone. 

Figure 4: The Red LED Lights Up on the Board When the Keyphrase is Detected 



<!-- Start of picture text -->
Green LED (Power)<br>as<br>reser aaE |<br>Opening to P14 for VDD  Green LED and red LED<br>current measurement  indicates Keyphrase is detected<br><!-- End of picture text -->

<u>www.quicklogic.com</u> **9** • • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

**_QuickLogic S3 ASSP EVK Power Measurement – Rev. 1.0_** 

#### **LPSD + Step Counter** 

To measure LPSD plus Step Counter current consumption: 

|**1.**|Select (touch) the<br>CyweeMotion icon to<br>launch the pre-<br>installed application.|**2.** TouchSensor List<br>Demo.|**3.** Scroll down, touch<br>Cywee Step<br>CounterandOK.|**4.** SelectCywee Step<br>Counter.|
|---|---|---|---|---|
|**5.**|Touch theReturn<br>button to return to the<br>homescreen.|**6.** Select (touch) the S3<br>Voice Evaluation icon<br>to launch the pre-<br>installed application.|**7.** TouchKeyphrase<br>Detection.|**8.** Touch thePlay<br>button. The screen<br>will go black.<br>Listening for the<br>keyphrase “OK<br>QuickLogic.” The<br>blue LED on the<br>board will light up to<br>indicate the system<br>has gone into low<br>power mode<br>(listening).|
|**9.**|Clear the DMM<br>reading and start a<br>new reading<br>sequence.|**10.**Wait 60 seconds.|**11.**Collect the average<br>reading.|**12.**Touch the Return<br>button to return to the<br>previous screen.|



#### **KPD + Step Counter** 

**NOTE:** Do this step immediately after LPSD + step counter data measuring. 

To measure the KPD plus step counter current consumption: 

|**1.** Clear the DMM<br>reading.|**2.** Make sound by<br>talking for 60<br>seconds; avoid<br>speaking the<br>keyphrase “OK<br>QuickLogic.”|**3.** Collect the average<br>reading.|**4.** Touch the Return<br>button to return to the<br>previous screen.|
|---|---|---|---|
|**5.** Speak the keyphrase<br>“OK QuickLogic.”<br>The red LED lights up<br>on the board when<br>the keyphrase is<br>detected and the<br>Keyphrase Detection<br>screen is displayed on<br>the phone.|**6.** Touch the Return<br>button to return to the<br>previous screen.|||



<u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

**10** 

**_QuickLogic S3 ASSP EVK Power Measurement – Rev. 1.0_** 

### **Contact Information** 

Phone: (408) 990-4000 (US) +(44) 1932-21-3160 (Europe) +(886) 26-603-8950 (Taiwan) +(86) 139-0517-5302 (China) +(81) 3-5875-0547 (Japan) +(82) 31-601-4225 (Korea) 

E-mail: <u>info@quicklogic.com</u> Sales: <u>America-sales@quicklogic.com Europe-sales@quicklogic.com Asia-sales@quicklogic.com Japan-sales@quicklogic.com Korea-sales@quicklogic.com</u> 

Support: <u>www.quicklogic.com/support</u> 

Internet: <u>www.quicklogic.com</u> 

### **Revision History** 

|**Revision**|**Date**|**Originator and Comments**|
|---|---|---|
|1.0|December 2016|Initial Release. AnthonyLe and Kathleen Bylsma|



### **Notice of Disclaimer** 

QuickLogic is providing this design, product or intellectual property "as is." By providing the design, product or intellectual property as one possible implementation of your desired system-level feature, application, or standard, QuickLogic makes no representation that this implementation is free from any claims of infringement and any implied warranties of merchantability or fitness for a particular purpose. 

You are responsible for obtaining any rights you may require for your system implementation. QuickLogic shall not be liable for any damages arising out of or in connection with the use of the design, product or intellectual property including liability for lost profit, business interruption, or any other damages whatsoever. QuickLogic products are not designed for use in life-support equipment or applications that would cause a life-threatening situation if any such products failed. Do not use QuickLogic products in these types of equipment or applications. 

QuickLogic does not assume any liability for errors which may appear in this document. However, QuickLogic attempts to notify customers of such errors. QuickLogic retains the right to make changes to either the documentation, specification, or product without notice. Verify with QuickLogic that you have the latest specifications before finalizing a product design. 

<u>www.quicklogic.com</u> **11** • • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

**_QuickLogic S3 ASSP EVK Power Measurement – Rev. 1.0_** 

### **Copyright and Trademark Information** 

Copyright © 2016 QuickLogic Corporation. All Rights Reserved. 

The information contained in this document is protected by copyright. All rights are reserved by QuickLogic Corporation. QuickLogic Corporation reserves the right to modify this document without any obligation to notify any person or entity of such revision. Copying, duplicating, selling, or otherwise distributing any part of this product without the prior written consent of an authorized representative of QuickLogic is prohibited. 

QuickLogic is a registered trademark, and the EOS design and QuickLogic logo are trademarks of QuickLogic. Other trademarks are the property of their respective companies. 

•• •••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

**12** 

<u>www.quicklogic.com</u> 

