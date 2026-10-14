---
title: "Connecting External Sensors to Merced 1.1 HDK Application Note"
source_file: "QL Application Note 150 Connecting External Sensors to Merced HDK.pdf"
pages: 12
sha256: 4d46b4612be6777fd94238e3942391a0b5ff53ccfa179bdd0fc3d4d593bf9f16
---

# Connecting External Sensors to Merced 1.1 HDK Application Note



<!-- Start of picture text -->
geQuickLoaic<br><!-- End of picture text -->

# **Connecting External Sensors to Merced 1.1 HDK** 

#### **Application Note 150** 

This document describes the procedure to connect external sensors to the QuickAI™ Merced 1.1 Hardware Development Kit (HDK). 

The QuickAI Merced 1.1 HDK together with the QuickLogic Software Development Kit provides a good starting point for developing and testing AI applications. The board connectors support standard Arduino™ expandability making the HDK ideal for Proof-of-Concept (PoC) developments. 

The Merced 1.1 HDK contains: 

- Boards Stack 

- Micro USB cable 

- µSD card USB adapter 

Figure 1: Merced 1.1 HDK 



<!-- Start of picture text -->
jE sere Be) ieee?) Rrra sie tt © le kiobe ast Serta is<br>= = (AS, et 33) 3) 2 SS 4 - 123) sb<br>wey [2 5 ae - - ve firs sestan=esa=)} UACILEEECEEE’ | 4<br>Ee= me 5 nn oe ea rea ak = Co a<br>= as SaaS -—— i .<br><!-- End of picture text -->

The following sensors are supported by the Merced 1.1 HDK: 

- Analog interface sensors (additional analog to digital conversion hardware is required) 

- Inertial measurement unit sensors such as Accelerometer, Gyroscope, and Magnetometer. 

© 2019 QuickLogic Corporation 

www.quicklogic.com 1 

**_QuickLogic Connecting External Sensors to Merced 1.1 HDK Application Note - Version 1.0_** 

**_29-150_** 

## **1. Analog Interface Sensors Support** 

Connecting the Analog Sensor Board to the Merced 1.1 HDK requires the Mayhew Extended ADC Shield hardware platform from Mayhew Labs. The Mayhew ADC Shield board is compatible with the Merced 1.1 HDK Arduino connections. The QuickLogic SDK provides functions that is compatible with the LTC1859 device on the Mayhew ADC Shield. 

Figure 2: System Connection Diagram 



<!-- Start of picture text -->
+5V supply Mayhew<br>(viaUSB) + _ e ADC Shield<br>as a e<br>f a Be —<br>Merced 1.1 ees ‘at ee Deon ty s a’<br>HDK te © ON ae 2<br>ial ea Arduino<br>a<br>Sg<br><!-- End of picture text -->

### **1.1. Single-Ended Analog Sensor Connection** 

Connect the Analog Sensor Board wires to the P1 connector on the Mayhew Extended ADC Shield. Tighten the screws to ensure good contact between the wires and the connector. Connect the ground between the Analog Sensor Board and the ADC Shield. 

Power up the Analog Sensor Board using a DC power source. 

Figure 3: Single-Ended Analog Connection 



<!-- Start of picture text -->
Input 0<br>Input 1<br>Input 2<br>Input 3<br><!-- End of picture text -->



<!-- Start of picture text -->
a<uBfes: Ro<br>KRowvwnnxx<br>PL Bio ke P3<br>e<br>ACCc< }|RPa EY * P51E5985 @ @ © @:  ©)<br>@® IOiey =e<br>4i 6)mi@)s@2 OR RoLn =pave )}HH/0 is misolsvtesp. | ja<br>2 A ee SS op Beciz =<br>2 @|GND wy = BENS vemacar —[SCK MOS!<br>ey) OE85) (=e £85 ==~ gpaecis21 |Rst|cno] &<br>|“RGM Pe lOS new = ee, mzetarcies7)<br>les °* took Dg macig, — MeoucTcrese)<br>@}7 32... cis’ wih e Hiei (c1c1859)<br>\4 3 ya<br>GND # #' tr<br>g1 © a | eeehe 38 MayhewExtended ADC Labs Shield<br>ae @<br>SES aRye 2 - Seo<br><!-- End of picture text -->

© 2019 QuickLogic Corporation 

www.quicklogic.com 2 

**_QuickLogic Connecting External Sensors to Merced 1.1 HDK Application Note - Version 1.0_** 

**_29-150_** 

### **1.2. Differential Analog Sensor Connection** 

Connect the Analog Sensor Board wires to the P1 connector on the Mayhew Extended ADC Shield. Tighten the screws to ensure good contact between the wires and the connector. Connect the ground between the Analog Sensor Board and the ADC Shield. 

Power up the Analog Sensor Board using a DC power source. 

Figure 4: Differential Analog Connection 



<!-- Start of picture text -->
Input 0<br>Input 1<br>Input 2<br>Input 3<br><!-- End of picture text -->



<!-- Start of picture text -->
PL oe KS 3<br>tS)| >© |ea KXBExSSE XX)<br>Role}: 3: 2°5°83 @<br>| >, OBE _ ut 3 ae<br>a ma i@js Ce Ry = HH/0) misolsv | ja<br>a F ee SS R= Mueciz ~<br>2 @)GND ay = 38N= vewc21 —[SCK MOS!|<br>j @ Oso,9 Sean SHES(So SeHosts [pstlow] am<br>4P me iO> peek = eee mznarcies7)<br>A el” 3h... cia” gl bine Hits.ba (cTC1859)<br>WD ts} wo<br>an |@\cle|cno eeOF men Beer+2  cis B4-vt 101858)<br>1 © teed 38 Mayhew Labs<br>ADC Shield<br>EE a | be Extended<br>Bea aracon @<br>ee °° be 6 ele<br><!-- End of picture text -->

© 2019 QuickLogic Corporation 

www.quicklogic.com 3 

**_QuickLogic Connecting External Sensors to Merced 1.1 HDK Application Note - Version 1.0_** 

**_29-150_** 

### **1.3. Wiring** 

On the Mayhew ADC Shield, connect these pins as shown in the following figure. 

- P5-1 to P6-13 

- P5-2 to P6-11 

- P5-3 to P3-6 

- P5-4 to P3-5 

- P5-5 to P3-4 

- P5-6 to P3-3 

Figure 5: Wiring Connection 



<!-- Start of picture text -->
a8 P6 ; a<br>PL dasBectece "Ti Lies<br>tS<br>q G feo sitOOO008<br>< ees BESESR<br>A Fe<br>2 © @) oF ao pes hy I EB r)<br>ele sek = y= 5 Go we<br>= @|GND wy = Pre] S Hoeciz ‘<br>1 -© bd a(S8S BRSSes SB cemeczswmacis (SKRete]HOSH @ ~Bs<br>5 Os wed =——~te)pancis M20 Te1857)<br>aCA \C Gedon tol Ds tw C19 Hi'4-nit (LT101858)<br>i @? Sean as’ sh @ Hite it (L7c1859)<br>e7 © { @|GNoaewa? =o35 Mayhew Labs<br>Ae & Extended ADC Shield<br>825 ao Ee oer en nee<br><!-- End of picture text -->

The following figure shows the system integration. 

Figure 6: System Integration 



<!-- Start of picture text -->
| )<br>—- &<br><!-- End of picture text -->

© 2019 QuickLogic Corporation 

www.quicklogic.com 4 

**_QuickLogic Connecting External Sensors to Merced 1.1 HDK Application Note - Version 1.0_** 

**_29-150_** 

### **1.4. Mayhew Extended ADC Shield** 

The Mayhew Extended ADC Shield is a plug-and-play board that can be connected to the Merced 1.1 HDK through the Arduino compatible connections. The Mayhew ADC Shield is capable of supporting eight single-ended or four differential inputs. The current Analog SDK supports four single-ended input channels or four differential input channels. 

The Mayhew ADC Shield supports: 

- Input voltage of 0 V to 5 V, 0 V to 10 V, ±5 V or ±10 V 

- Total sampling rate of 100 ksps (K sampling per second) 

- 3 V SPI 

The Mayhew ADC Shield shipped by QuickLogic is modified to work with the Merced 1.1 HDK out-of-the-box. The part number is QAI-MAYHEW16BIT-AA-1.0. 

The kit contains: 

- Modified Mayhew Extended ADC Shield 

- Cables set (6 cables) 

##### Figure 7: Extended Shield and Cables 



Merced 1.1 HDK 

ADC Shield Wiring Cables 

© 2019 QuickLogic Corporation 

www.quicklogic.com 5 

**_QuickLogic Connecting External Sensors to Merced 1.1 HDK Application Note - Version 1.0_** 

**_29-150_** 

### **1.5. Extended ADC Shield Modifications** 

The following modifications are required when the Mayhew ADC Shield is purchased from a third party: 

1. Install a 1x6 header on the P5 connector. An example part number is M20-9990646. 

Figure 8: P5 — 1x6 Header Installation 



<!-- Start of picture text -->
- | Leeman38 8 Ps E<br>fe)q Ee... CLK XXX)<br>jo Own. POS OR a<br>2D @: os"fi} Zz e£oga8SY fa r )<br>&“abA | @\2(@)3 LmOm9 tinS83 =zSEas Us (sy osc IMisolsvsolsvisp. | k&Be<br>@jcnomg ES zVS reac SOK Mos]<br>J N@l4 4* E288 S  Hnects [Rst|cno| &<br>Sean Bee fe<br>Peete @)® one® FF IID, mann across)<br>7 C tes Fou 5 hata? Mest crore)<br>A e|7 324. et! i ¢ Hitsbi (.101859)<br>7 i Oele\c S B =333 Mayhew Labs<br>E a | = Extended ADC Shield<br>528 fo ris eo<br><!-- End of picture text -->

2. Replace the P8 header with a 6-position receptacle. An example part number is M20-7830346. 

Figure 9: P8 — Receptacle Replacement 



<!-- Start of picture text -->
200NNHOH CON6OGGK"9@§<br>.<br>g<br>.885505<br>BHOOZO @o<br>eeeee8 A<br>$J1: CONVST om u<br>PB $J3: SCK e<br>+1109 |icsps|1cses|icses| 1010] 108 S48: SO! te @3<br>© ||| @|@|® ss: sus a<br>other [oTwer [ower |orwer |orHer OTHER<br>O/0/0|0|0|0 cx@ #7<br>4@ ws<br>5®@<br>6@ 4Os<br>Py 7@ @6<br>spicomteve: CNO@ @ 7<br>* =)SJ? @Le5V 3.3V S fa9<br>29909 C9eeenre @<br><!-- End of picture text -->

3. Remove solder bridges from SJ1, SJ2, SJ3, SJ4, SJ5, and SJ6. 

4. Change the solder bridge of SJ7 to 3.3 V SPI. 

© 2019 QuickLogic Corporation 

www.quicklogic.com 6 

**_QuickLogic Connecting External Sensors to Merced 1.1 HDK Application Note - Version 1.0_** 

**_29-150_** 

Figure 10: Change Solder Bridges 



5. Install filter capacitors based on the analog connections. Either single-ended or differential connection can be used. For smoothening the noise on the incoming analog signals, consider populating capacitors C1 through C12 with 3000 pF and 0603 SMD size. For single-ended connection, populate C1, C4, C7, and C10. For differential connection, populate C2, C5, C8, and C11. 

NOTE: It is not recommended to populate all locations so that the input can be switched between single-ended and differential connections. We recommend preparing two different boards — one for single-ended input and the other for differential input. 

Figure 11: Filter Capacitors 



© 2019 QuickLogic Corporation 

www.quicklogic.com 7 

**_QuickLogic Connecting External Sensors to Merced 1.1 HDK Application Note - Version 1.0_** 

**_29-150_** 

6. Install a 1x9 header on the P4 connector (optional). 

Figure 12: P4 — 1x9 Header Installation 



<!-- Start of picture text -->
Ee P6<br>Pr g P3<br>1c<br>1 < E rs) . PTX— OxonXX)o><br>0 Cm me, oO i @<br>A oe a Z$°3° 983<br>@ 1} OF Z a<br>3@<br>2 = 3) Ommoaac sz Sh== ‘onnciz MISPY Ba-<br>y N@l4 y* S283 S  muects [RST IGNO]<br>5 Sawa 4 ae°°=S— = fem C20<br>45 C 6|6 oOge 2 . ccs M2isntbtccTct857)(L101858)<br>6 Gees3 on Fe sollcz wisi fee‘  CLS Bhe.bit (LTC1859)<br>7 bieeae tr3° Mayhew Labs<br>c le ] 3 ExtendedADC Shield<br>brsa a z Aaig RY @<br>P2 *<br>@ C25 >> o-no eo<br><!-- End of picture text -->

© 2019 QuickLogic Corporation 

www.quicklogic.com 8 

**_QuickLogic Connecting External Sensors to Merced 1.1 HDK Application Note - Version 1.0_** 

**_29-150_** 

## **2. I2C Sensor Support** 

An I2C sensor can be connected to the Merced 1.1 HDK through the Arduino connectors (J1 and J7). The followings I2C addresses are used for connection: 

- AKM 9915: 0x1A and 0x1B (7-bit address + R/W: 0x0D+R/W) 

- BMI160: 0xA0 and A1 (7-bit address + R/W: 0x68+R/W) 

The following table lists the available connections for the I2C sensor: 

Table 1: I2C Support 

|**Connector**|**Pin #**|**Function**|
|---|---|---|
|J2|9|I2C SDA|
|J2|10|I2C SCL|
|J7|1|USB 5V|
|J7|5|I2C IO 3.3 V|
|J7|2, 3|GROUND|



Figure 13: I2C Sensor Connection 





<!-- Start of picture text -->
5 V<br>GND<br>3.3 V<br><!-- End of picture text -->



<!-- Start of picture text -->
SCL<br>SDA<br><!-- End of picture text -->

© 2019 QuickLogic Corporation 

www.quicklogic.com 9 

**_QuickLogic Connecting External Sensors to Merced 1.1 HDK Application Note - Version 1.0_** 

**_29-150_** 

## **3. SPI Sensor Support** 

An SPI sensor can be connected to Merced 1.1 HDK through the Arduino connectors. The following table lists the available connections for the SPI sensor: 

Table 2: SPI Support 

|**Connector**|**Pin #**|**Function**|
|---|---|---|
|J2|4|SPI SENSOR MOSI|
|J2|5|SPI SENSOR MISO|
|J2|6|SPI SENSOR SCLK|
|J1|5|SPI SENSOR SSN3 (select 3)|
|J7|1|USB 5 V|
|J7|5|I2C IO 3.3 V|
|J7|2, 3|GROUND|



Figure 14: SPI Sensor Connection 





<!-- Start of picture text -->
5 V<br>GND<br>3.3 V<br>SCLK<br>MISO<br>MOSI<br>SSN3<br><!-- End of picture text -->

© 2019 QuickLogic Corporation 

www.quicklogic.com 10 

**_QuickLogic Connecting External Sensors to Merced 1.1 HDK Application Note - Version 1.0_** 

**_29-150_** 

## **4. Revision History** 

|**Version**|**Date**||**Revision**|
|---|---|---|---|
|1.0|May 2019|First release.||



© 2019 QuickLogic Corporation 

www.quicklogic.com 11 

**_QuickLogic Connecting External Sensors to Merced 1.1 HDK Application Note - Version 1.0_** 

**_29-150_** 

## **Contact Information** 

Phone: (408) 990-4000 (US) 

+44 1932-213160 (Europe) +886 2-6603-8950 (Taiwan) +86 1390517502 (China) +81 3-5875-0547 (Japan) +82-31-601-4225 (Korea) E-mail: info@quicklogic.com Sales: America-sales@quicklogic.com Europe-sales@quicklogic.com Asia-sales@quicklogic.com Japan-sales@quicklogic.com Korea-sales@quicklogic.com 

Support:  www.quicklogic.com/support Internet: www.quicklogic.com 

## **Notice of Disclaimer** 

QuickLogic is providing this design, product or intellectual property, ‘as is’. By providing the design, product or intellectual property as one possible implementation of your desired system-level feature, application, or standard, QuickLogic makes no representation that this implementation is free from any claims of infringement and any implied warranties of merchantability or fitness for a particular purpose. 

You are responsible for obtaining any rights you may require for your system implementation. QuickLogic shall not be liable for any damages arising out of or in connection with the use of the design, product or intellectual property including liability for lost profit, business interruption, or any other damages whatsoever. QuickLogic products are not designed for use in life-support equipment or applications that would cause a life-threatening situation if any such products failed. Do not use QuickLogic products in these types of equipment or applications. 

QuickLogic does not assume any liability for errors which may appear in this document. However, QuickLogic attempts to notify customers of such errors. QuickLogic retains the right to make changes to either the documentation, specification, or product without notice. Verify with QuickLogic that you have the latest specifications before finalizing a product design. 

## **Copyright and Trademark Information** 

Copyright © 2019 QuickLogic Corporation. All Rights Reserved. 

The information contained in this document is protected by copyright. All rights are reserved by QuickLogic Corporation. QuickLogic Corporation reserves the right to modify this document without any obligation to notify any person or entity of such revision. Copying, duplicating, selling, or otherwise distributing any part of this product without the prior written consent of an authorized representative of QuickLogic is prohibited. 

QuickLogic is a registered trademark, and Aurora, ArcticPro, and the QuickLogic logo are trademarks of QuickLogic. Other trademarks are the property of their respective companies. 

© 2019 QuickLogic Corporation 

www.quicklogic.com 12 

