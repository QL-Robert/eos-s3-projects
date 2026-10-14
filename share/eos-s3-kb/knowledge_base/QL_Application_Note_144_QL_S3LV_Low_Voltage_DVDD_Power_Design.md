---
title: "Technical Writer"
source_file: "QL Application Note 144 \u2013 QL S3LV \u2013 Low Voltage DVDD Power Design.pdf"
pages: 8
sha256: 6145b66f2afc9258f6e25e0d4dc76f58e64e83a59cf00aca9b13d69c1d9b0b38
---

# Technical Writer

# **QuickLogic**<sup>**®**</sup> **S3LV – Low Voltage DVDD Power Design** <mark>SS</mark> 

**• • • • • • QuickLogic Application Note 144** 

## **Introduction** 

This application note presents an implementation overview for S3LV system designer to implement a power circuit for S3LV. 

### **Scope of Document** 

This document focuses on the implementation of a core power external circuit, and covers the following topics: 

- Reference circuit design for S3LV DVDD using a TOREX XC9272 Series converter 

- Power supply analysis 

- Things to look for when selecting a power switcher for S3LV 

- Detailed schematic for the supply circuit 

### **Requirements** 

The S3LV requires the following supplies: 

- Analog supply (AVDD): range from 1.7V to 3.6V 

- IO power A (VCCIOA): range from 1.7V to 3.6V 

- IO power B (VCCIOB): range from 1.7V to 3.6V 

- Core power (DVDD or LDO_VOUT1/2): range from 0.85V ± 20mV to 1.1V 

### **References** 

For additional information refer to: 

- _QuickLogic_<sup>_®_</sup> _S3LV Sensor Processing Platform Data Sheet_ 

- _TOREX_<sup>_®_</sup> _XC9272 Series Data Sheet_ Scope of Document 

••• ••• 

**<mark>CONFIDENTIAL</mark> PRELIMINARY** 

© 2018 QuickLogic Corporation 

<u>www.quicklogic.com</u> **1** 

**_QuickLogic_**<sup>**_®_**</sup> **_S3LV – Low Voltage DVDD Power Design Rev. 1.0_** 

## **S3LV Core Voltage Supply Overview** 

The S3LV has two internal LDOs (as shown in **Figure 1** ) that provide voltage supplies to the device memories and core logic. The internal LDO outputs are programmable, and can be turned off to allow an external switcher to supply a lower voltage (as low as 0.85V ± 20mV). The external switcher is recommended for a system design that must achieve the lowest possible power consumption by the S3LV core. 

A system design that does not include an external switcher (BOM reduction) is possible; the power consumption reduction is limited by the LDOs output voltage setting (0.95V) and low efficiency due to a voltage drop from 1.8V input to 0.95V output. 

At power-on, the S3LV default is to turn on the internal LDOs. The setting voltage is 1.07V; depending on the configuration setting (via boot-strap pins), the device configuration is performed by a Host (Slave Mode) or boot from flash device. At the end of device configuration, the firmware turns off the internal LDOs and allows the external switcher to provide the proper voltage level for operations. 

**NOTE:** At a core voltage of 0.85V, the maximum operating frequency for S3LV M4F is 48 MHz. 

Figure 1: S3LV DVDDx Supply Circuit 



<!-- Start of picture text -->
Switcher<br>AVDD<br>Analog<br>1.62V – 3.6V<br>0.85V<br>SRAMs<br>DVDD1<br>LDO‐1<br>LDO_VIN<br>1.62V – 3.6V<br>DVDD2<br>LDO‐2<br>Logic<br>Gates<br><!-- End of picture text -->

**2** <u>www.quicklogic.com</u> •• •••• 

**<mark>CONFIDENTIAL</mark> PRELIMINARY** 

© 2018 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3LV – Low Voltage DVDD Power Design Rev. 1.0_** 

## **Switcher Operation Schemes** 

Depending on the selection of external switcher, a different firmware operation scheme is required. There are three power schemes: 

- Scheme 1: External switcher does not pull down when output is over-driven. 

- Scheme 2: External switcher does pull down when the output is over-driven and has an output enable signal. 

- Scheme 3: External switcher with multiple output voltages (dual voltage switcher). 

### **Scheme 1** 

In this scheme, the operation of the system is straight forward. The sequence is: 

**1.** The system is powered on. 

**2.** The internal LDOs are powered on and the output of the LDOs is set to ~1.07V, which causes an overdriven voltage event at the switcher output. 

**3.** In response, the switcher turns off its output and current dissipates via the switcher internal pull-down resistor. 

**4.** After the device configuration is completed, the firmware disables the S3LV internal LDOs. 

**5.** The switcher turns on its output, which must match with the bulk capacitor used for DVDDx to avoid voltage loss. 

### **Scheme 2** 

In this scheme, the operation requires hardware design to control the switcher at power-on. The sequence is: 

**1.** The system powered on. 

**2.** The S3LV IO is in default mode; the majority of S3LV IOs are in tristate mode. An external pull-up or pulldown is connected to the switcher output enable pin to disable its output. 

**3.** The internal LDOs are powered on and the LDOs output is set to ~1.07V 

**4.** After device configuration is completed, the firmware sets the LDO output to 0.85V 

**5.** The firmware enables the external switcher (via an IO setting) and disables the S3LV internal LDOs. This causes a momentary contention between the LDOs output and the switcher output. 

• • • ••• 

**<mark>CONFIDENTIAL</mark> PRELIMINARY** 

© 2018 QuickLogic Corporation 

<u>www.quicklogic.com</u> **3** 

**_QuickLogic_**<sup>**_®_**</sup> **_S3LV – Low Voltage DVDD Power Design Rev. 1.0_** 

### **Scheme 3** 

Scheme 3 requires a different system power connection for the DVDDs. The S3LV LDOs are off by default. The external switcher output is used to provide voltage to S3LV DVDDs. See **Figure** for the power connection. The switcher can provide two voltages: 1.1V and 0.85V; the high voltage level is needed for device power-on and configuration. The low voltage level is used for normal operations to minimize the S3LV current consumption. The sequence is: 

**1.** The system is powered on. 

**2.** The S3LV IO is in default mode; the majority of S3LV IOs are in tristate mode. An external pull-up or pulldown is connected to the switcher output select pin to default to 1.1V. 

**3.** The internal LDOs are powered off due to the hardware connection. 

**4.** After the device configuration is completed, the firmware sets the switcher output select signal to select 0.85V output. 

Figure 2: Connection with Dual Output Switcher 



<!-- Start of picture text -->
Switcher<br>AVDD Select<br>Analog<br>1.62V – 3.6V 1.10V<br>0.85V<br>SRAMs<br>DVDD1<br>LDO‐1<br>LDO_VIN<br>DVDD2<br>LDO‐2<br>Logic<br>Gates<br><!-- End of picture text -->

**4** <u>www.quicklogic.com</u> •• •••• 

**<mark>CONFIDENTIAL</mark> PRELIMINARY** 

© 2018 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3LV – Low Voltage DVDD Power Design Rev. 1.0_** 

## **Designing Using the TOREX XC9272 Switcher** 

The TOREX XC9272 device is an ultra-low power synchronous step-down DC/DC converter for a device that requires low voltage supply. **Figure 3** shows an example of a typical system connection for XC9272 device. 

#### Figure 3: Typical Connection for XC9272 



<!-- Start of picture text -->
0.85V<br>L<br>VIN VIN LX VOUT<br>XC9272<br>CIN (10uF/10V) CL (22uF/10V)<br>CE VOUT<br>GND<br><!-- End of picture text -->

For example: 

The CE pin has the following operations: 

- CE = H: output is active 

- CE = L: output is standby 

**NOTE:** The CE pin must not be open. 

Recommendations for system connection to CE: 

- If there is IO available that is not from the S3LV and this IO is active prior to VIN being active, the system can drive the signal low at VIN power-on. Once S3LV configuration is done, GPIO can drive the CE high before disabling the S3LV internal LDOs. 

- If the S3LV IO is used to drive the CE, add a pull-down resistor to the CE line to disable the switcher output at power-on. Once S3LV configuration is done, the S3LV can drive the CE high before disabling the S3LV internal LDOs. 

- If no IO is available to control the CE pin, connect the pin to pull-up resistor. As shown in **Figure 4** additional leakage will occur until firmware disables the internal LDOs. 

- When the S3LV LDOs output voltage (@ 1.07V) is active, the XC9272 output is lower than the driving voltage and the system leakage current flows through the VOUT of the IC. 

• • • ••• 

**<mark>CONFIDENTIAL</mark> PRELIMINARY** 

© 2018 QuickLogic Corporation 

<u>www.quicklogic.com</u> **5** 

**_QuickLogic_**<sup>**_®_**</sup> **_S3LV – Low Voltage DVDD Power Design Rev. 1.0_** 

Figure 4: Leakage Current Path Due to Higher VOUT 



<!-- Start of picture text -->
0.85V<br>L<br>VIN VIN LX VOUT 1.10V<br>XC9272<br>CIN (10uF/10V) CL (22uF/10V)<br>CE VOUT<br>GND<br>Leakage Current<br>Figure 5  provides additional details inside the switcher.<br>Figure 5: Leakage Path<br>PFM Comparator Unit<br>VOUT<br>CF B RFB1<br>Short Current<br>Protection Sense<br>CL<br>RFB2 PFM<br>Discharge<br>Comparator<br>FB<br>Leak Current –<br>PFM<br>+<br>Controller<br>Synch<br>Buffer LX<br>CE CE Controller Logic VREF Driver<br>VDD<br>GND<br>UVLO<br>VIN<br>VIN Start Up<br>Controller<br><!-- End of picture text -->

**Figure 5** provides additional details inside the switcher. 

**NOTE:** The leakage current for VIN @ 3.7V and VOUT @ 1.1V is 0.11 µA 



<!-- Start of picture text -->
6 www.quicklogic.com CONFIDENTIAL<br>•• ••••<br>PRELIMINARY<br><!-- End of picture text -->

© 2018 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3LV – Low Voltage DVDD Power Design Rev. 1.0_** 

## **Contact Information** 

Phone: (408) 990-4000 (US) +(44) 1932-21-3160 (Europe) +(886) 2-6603-8947 (Taiwan) +(86) 139-0517-5302 (China) +(81) 3-5875-0547 (Japan) +(82) 31-601-4225 (Korea) 

E-mail: <u>info@quicklogic.com</u> Sales: <u>America-sales@quicklogic.com Europe-sales@quicklogic.com Asia-sales@quicklogic.com Japan-sales@quicklogic.com Korea-sales@quicklogic.com</u> 

Support: <u>www.quicklogic.com/support</u> 

Internet: <u>www.quicklogic.com</u> 

## **Revision History** 

|**Revision**|**Date**|**Originator and Comments**|
|---|---|---|
|1.0|March 2018|AnthonyLe and Kathleen Bylsma|



## **Notice of Disclaimer** 

QuickLogic is providing this design, product or intellectual property "as is." By providing the design, product or intellectual property as one possible implementation of your desired system-level feature, application, or standard, QuickLogic makes no representation that this implementation is free from any claims of infringement and any implied warranties of merchantability or fitness for a particular purpose. 

You are responsible for obtaining any rights you may require for your system implementation. QuickLogic shall not be liable for any damages arising out of or in connection with the use of the design, product or intellectual property including liability for lost profit, business interruption, or any other damages whatsoever. QuickLogic products are not designed for use in life-support equipment or applications that would cause a life-threatening situation if any such products failed. Do not use QuickLogic products in these types of equipment or applications. 

QuickLogic does not assume any liability for errors which may appear in this document. However, QuickLogic attempts to notify customers of such errors. QuickLogic retains the right to make changes to either the documentation, specification, or product without notice. Verify with QuickLogic that you have the latest specifications before finalizing a product design. 

<u>www.quicklogic.com</u> **7** • • • ••• 

**<mark>CONFIDENTIAL</mark> PRELIMINARY** 

© 2018 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3LV – Low Voltage DVDD Power Design Rev. 1.0_** 

## **Copyright and Trademark Information** 

Copyright © 2018 QuickLogic Corporation. All Rights Reserved. 

The information contained in this document is protected by copyright. All rights are reserved by QuickLogic Corporation. QuickLogic Corporation reserves the right to modify this document without any obligation to notify any person or entity of such revision. Copying, duplicating, selling, or otherwise distributing any part of this product without the prior written consent of an authorized representative of QuickLogic is prohibited. 

QuickLogic is a registered trademark, and the QuickLogic logo is trademark of QuickLogic. Other trademarks are the property of their respective companies. 

•• •••• 

**<mark>CONFIDENTIAL</mark> PRELIMINARY** 

© 2018 QuickLogic Corporation 

**8** <u>www.quicklogic.com</u> 

