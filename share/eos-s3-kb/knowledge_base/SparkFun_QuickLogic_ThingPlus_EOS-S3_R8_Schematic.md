---
title: "QTPLUS_R8"
source_file: "SparkFun_QuickLogic_ThingPlus_EOS-S3_R8_Schematic.pdf"
pages: 6
sha256: ede4787d6ce893598b7a0b2a71b38b135e0a679d84fa4a9311122f0ae0e299c5
---

# QTPLUS_R8



<!-- Start of picture text -->
5 4 3 2 1<br>+VBUS +VBAT<br>D1<br>D +3V3 PMEG4005EJ,115 D<br>+VBAT<br>C1<br>R1<br>C2 R39 4.7uF<br>R2 100K 1M5 R3<br>100pF IC1 +3V3 100K<br>453K 1 8 PG<br>3V3_EN EN PG<br>2 7 L1<br>FB VIN<br>3 6 1 2<br>AGND SW<br>4 5<br>NC PGND<br>DFE201610E_R47M=P2<br>R4 C3<br>TPS62821DLCR<br>100K<br>22uF Q1<br>NX3008CBKV_115<br>C C<br>POWER SUPPLY<br>R5<br>ADC0<br>200K<br>ADC0_EN<br>R7<br>R6 100K<br>10K<br>+VBUS<br>B +VBAT B<br>LED1<br>R8 BATTERY VOLTAGE MONITOR<br>2 1 IC2<br>A K J1<br>MCP73831T_2ACI_OT<br>1K5 1 4 S2<br>2 STAT VDD 5 SHIELD__1 S1 +VBAT<br>APT1608SYCK VSS PROG SHIELD<br>3<br>VBAT<br>2<br>2<br>1<br>1<br>R9<br>C4<br>S2B-PH-SM4-TBLFSN<br>4K7<br>4.7uF<br>Q2 FD1<br>H1<br>2N7002KW<br>PG 1 3<br>G D fiducial H2<br>A C5 2 A<br>BATTERY CHARGER S Optimus Logic Sys Pvt Ltd<br>H3<br>1uF FD2 H4 Title QuickThing+<br>fiducial<br>Size Document Number Rev<br>A <Doc> 0<br>Date: Tuesday, October 27, 2020 Sheet 1 of 6<br>5 4 3 2 1<br>2<br>1<br>6 5 4<br>D1 G2 S2<br>S1 G1 D2<br>1 2 3<br><!-- End of picture text -->



<!-- Start of picture text -->
5 4 3 2 1<br>U1<br>+3V3<br>TP1<br>A6 B7<br>D LDO_VIN LDO_VOUT1 D<br>TP2<br>D8 B6<br>AVDD LDO_VOUT2 +3V3<br>A7 C8 C9<br>ADC0 ADC0<br>C7<br>ADC1 ADC1<br>4.7uF 4.7uF<br>C6 C10 C7 C11<br>C8<br>J2 J3 OSCO<br>+3V3 0.1uF 0.1uF 0.1uF 0.1uF<br>CON2 CON2 B8<br>Y2 OSCI<br>+3V3<br>ABS07-32768KHZ-T +3V3<br>E4 C2<br>VCCIOB1 VCCIOA<br>C13 E6<br>VCCIOB2<br>C12<br>12 pF<br>12 pF R11<br>R10<br>10K E7 B1<br>10K SPI_SLV_CLK D7 GPIO16 GPIO0 C1 I2C_SCL<br>C SPI_SLV_MISO E8 GPIO17 GPIO1 A1 I2C_SDA C<br>Q_LED_B H8 GPIO18 GPIO2 A2 S3IO_2<br>SPI_SLV_MOSI G8 GPIO19 GPIO3 B2 IMU_INT<br>SPI_SLV_CSn H7 GPIO20 GPIO4 C3 S3IO_4<br>R12 Q_LED_G G7 GPIO21 GPIO5 B3 S3IO_5<br>10K R13 Q_LED_R H6 GPIO22 GPIO6 A3 USR_BUTTON TP3<br>DNP 10K I2S_WCLK G6 GPIO23 GPIO7 C4 S3IO_7<br>DNP I2S_DOUT F7 GPIO24 GPIO8 B4 S3IO_8<br>S3IO_25 F6 GPIO25 GPIO9 A4 S3IO_9<br>ADC0_EN H5 GPIO26 GPIO10 C5 S3IO_10<br>SPI_MST_CS2 G5 GPIO27 GPIO11 B5 S3IO_11<br>PDM_DATA F5 GPIO28 GPIO12 D6 S3IO_12 R14 R15<br>PDM_CKO F4 GPIO29 GPIO13 A5 S3IO_13<br>S3IO_30 G4 GPIO30 GPIO14 C6 SWD_CLK 10K 10K<br>I2S_CLK H4 GPIO31 GPIO15 SWD_IO<br>TP4 E3 GPIO32<br>GPIO33<br>SPI_MST_CLK F3<br>SPI_MST_CLK F2 GPIO34<br>S3IO_35 SPI_MST_MISO H3 GPIO35<br>R16 SPI_MST_MISO G2 GPIO36<br>SPI_MST_MOSI E2 GPIO37 G3<br>USB_D_N R17 SPI_MST_MOSI SPI_MST_SS H2 GPIO38 VPP_FSOURCE<br>1K5 D2 GPIO39 E5<br>B 22E H1F1 GPIO40GPIO41 STM A8 B<br>R18 D1 GPIO42 AGND D3<br>USB_D_P 22E HEADER_P6 E1 GPIO43 GND1 D4<br>HEADER_TX G1 GPIO44 GND2 D5<br>R19 HEADER_RX GPIO45 GND3<br>F8<br>SYS_RST SYS_RSTn +3V3 TP7 +3V3<br>1K5<br>EOS_S3B_VBGA64<br>R20<br>IC3<br>R21 GD25Q16CWIGR 10K<br>+3V3 10K SPI_MST_SS 1 8<br>SPI_MST_MISO 2 CS# VCC 7<br>3 SO__IO1_ HOLD#__IO3_ 6 SPI_MST_CLK<br>4 WP#__IO2_ SCLK 5 SPI_MST_MOSI<br>+3V3 C14 VSS SI__IO0_<br>0.1uF<br>R22 R23<br>A 10K 10K A<br>SYS_RST Optimus Logic Sys Pvt Ltd<br>USR_BUTTON Title QuickThing+<br>Size Document Number Rev<br>B <Doc> 0<br>Date: Thursday, October 22, 2020 Sheet 2 of 6<br>5 4 3 2 1<br>1 2 1 2<br>PAD<br>9<br><!-- End of picture text -->

4 

3 

2 

1 

5 

C 

D 

B 

A 



<!-- Start of picture text -->
LED2<br>R24<br>LED_R R26 220E 1 2 100E LED_G D<br>3 4<br>67-23/R6GHBHC-B06/2T  +3V3<br>LED_B R25<br>100E<br>IC4<br>IC5<br>2N7002PV_115 2N7002PV_115 C<br>1 4 1 4<br>S1 S2 S1 S2<br>2 5 2 5<br>Q_LED_R G1 G2 Q_LED_B G1 G2 Q_LED_G<br>3 6 LED_R LED_G 3 6 LED_B<br>D2 D1 D2 D1<br>SYS_RST USR_BUTTON<br>B<br>S1<br>KMR221GLFS<br>S2<br>KMR221GLFS 4 3<br>4 3<br>1 2<br>1 2<br>4 3<br>4 3<br>1 2<br>1 2<br>Optimus Logic Sys Pvt Ltd A<br>Title QuickThing+<br>Size Document Number Rev<br>A <Doc> 0<br>Date: Thursday, October 22, 2020 Sheet 3 of 6<br>5 4 3 2 1<br><!-- End of picture text -->

4 

3 

2 

1 

5 

D 

C 

B 

A 



<!-- Start of picture text -->
J4<br>4<br>I2C_SCL 4<br>+3V3 3<br>I2C_SDA 3<br>2 6<br>2 6<br>1 5<br>1 5<br>Qwiic_PRT-14417 / 4208<br><!-- End of picture text -->

D 

C 



<!-- Start of picture text -->
+VBUS<br>J5 C15<br>A4/B9<br>VBUS<br>B4/A9 4.7uF<br>A5 VBUS__1<br>CC1<br>A6 B5<br>USB_D_P DP1 CC2 B<br>A7 B6<br>USB_D_N DN1 DP2 USB_D_P<br>A8 B7<br>SBU1 DN2 USB_D_N<br>B8<br>SBU2<br>D2 A1/B12<br>GND<br>TPD2EUSB30DRTR B1/A12<br>GND__1 G1<br>GND__2 G2<br>GND__3 G3<br>GND__4 G4<br>GND__5<br>USB4105-GF-A<br>Optimus Logic Sys Pvt Ltd A<br>Title QuickThing+<br>Size Document Number Rev<br>A <Doc> 0<br>Date: Thursday, October 22, 2020 Sheet 4 of 6<br>5 4 3 2 1<br>2 1<br>DM DP<br>GND<br>3<br><!-- End of picture text -->

4 

3 

2 

1 

5 

C 

D 

B 

A 



<!-- Start of picture text -->
+3V3<br>+3V3<br>U2<br>R28<br>6 1<br>VDD DATA PDM_DATA<br>C16 100E<br>4 2<br>I2C_SCL SCL SDA I2C_SDA<br>0.1uF<br>5 3<br>PDM_CKO CLOCK INT S3IO_12<br>7<br>SELECT<br>8<br>GND<br>VM3011<br>+3V3<br>+3V3<br>R29 R31 AC1 R30<br>9<br>VDD<br>4K7 4K7 10 10K<br>VDD_IO<br>2 12<br>CS INT1 IMU_INT<br>11<br>INT2<br>1<br>I2C_SCL SCL/SPC<br>+3V3 4<br>I2C_SDA SDA/SDI/SDO<br>3<br>SDO/SAO<br>5<br>RES<br>C17 6<br>GND<br>7<br>0.1uF GND__1 8<br>GND__2<br>LIS2DH12TR<br>Optimus Logic Sys Pvt Ltd<br>Title QuickThing+<br>Size Document Number Rev<br>A <Doc> 0<br>Date: Thursday, October 22, 2020 Sheet 5 of 6<br>4 3 2 1<br><!-- End of picture text -->

D 

C 

B 

A 

5 

4 

2 

5 

D C 

B 

A 



<!-- Start of picture text -->
1<br><!-- End of picture text -->

3 



<!-- Start of picture text -->
+3V3 D3<br>J6 RN1<br>TPD2EUSB30DRTR<br>EXB_2HV220JV<br>16<br>SYS_RST<br>15 1 3 1 16 J8.1<br>DP GND PDM_DATA 1 16<br>14 2 2 15 J8.2<br>SYS_RST DM PDM_CKO 2 15<br>13 R32 22E 3 14 J8.3<br>ADC1 I2S_WCLK 3 14<br>12 4 13 J8.4<br>I2S_DOUT 4 13<br>11 R33 22E D4 5 12 J8.5<br>S3IO_30 I2S_CLK 5 12 D<br>10 TPD2EUSB30DRTR 6 11 J8.6<br>S3IO_11 6 11<br>9 1 16 7 10 J8.7<br>1 16 S3IO_25 S3IO_12 7 10<br>8 2 15 1 3 8 9 J8.8<br>2 15 S3IO_13 SWD_IO DP GND S3IO_4 8 9<br>7 3 14 2<br>3 14 S3IO_2 SWD_CLK DM<br>6 4 13<br>4 13 SPI_MST_CLK<br>5 5 12<br>5 12 SPI_MST_MOSI<br>4 6 11<br>6 11 SPI_MST_MISO<br>3 7 10<br>7 10 HEADER_RX<br>2 8 9<br>8 9 HEADER_TX<br>1<br>RN2 +3V3<br>RN3<br>EXB_2HV220JV<br>CON16 EXB_2HV220JV<br>1 16 J8.9<br>S3IO_5 1 16<br>2 15 J8.10<br>USR_BUTTON 2 15<br>+3V3 R34 R35 3 14 J8.11<br>S3IO_7 3 14<br>4 13 J8.12<br>S3IO_8 4 13<br>10K 10K S3IO_10 5 5 12 12 J8.13 C<br>J7 6 11 J8.14<br>S3IO_35 6 11<br>62201021121 7 10<br>7 10<br>1 2 8 9<br>1 2 SWD_IO 8 9<br>3 4<br>3 4 SWD_CLK<br>D5 5 6<br>5 6<br>C18 7 8<br>7 8<br>9 10<br>9 10 SYS_RST<br>0.1uF<br>J8<br>TP5 J8.1 1 2 J8.2<br>TP6 SWD_IO J8.3 3 6 J8.4 B<br>SWD_CLK<br>+VBAT +3V3 J8.5 5 4 J8.6<br>R36 22E J8.7 7 8 J8.8<br>3V3_EN<br>+VBUS J9 J8.9 9 10 J8.10<br>J8.11 11 12 J8.12<br>1 J8.13 13 14 J8.14<br>R38 22E 2 15 16<br>SPI_MST_CS2<br>3 17 18<br>4<br>1 16 5<br>SPI_SLV_CSn 1 16<br>2 15 6 CON18A<br>SPI_SLV_MOSI 2 15<br>3 14 7<br>SPI_SLV_MISO 3 14<br>4 13 8<br>SPI_SLV_CLK 4 13<br>5 12 9<br>HEADER_P6 5 12<br>6 11 10<br>IMU_INT 6 11<br>7 10 11<br>I2C_SCL 7 10<br>8 9 12<br>I2C_SDA 8 9<br>Optimus Logic Sys Pvt Ltd A<br>RN4 CON12 Title<br>EXB_2HV220JV QuickThing+<br>Size Document Number Rev<br>A <Doc> 0<br>Date: Thursday, October 22, 2020 Sheet 6 of 6<br>5 4 3 2 1<br>1<br>2<br>SD05C.TCT<br><!-- End of picture text -->

