---
title: "CMSIS Meeting EW 2019"
source_file: "qorc-sdk/Libraries/CMSIS_5/CMSIS_EW2019.pdf"
pages: 51
sha256: a242e7e432afcdfec355443b296366044597e34429bf2c3860b77d36a2a444ce
---

# CMSIS Meeting EW 2019



# **Welcome to 10 years of CMSIS** 

CMSIS Partner Meeting Embedded World 2019 

Reinhard Keil Sr. Director Embedded Tools 

Joachim Krech Director of Engineering CMSIS/Tools Shebu Varghese Kuriakose Senior Software Technology Manager 

## Agenda 



<!-- Start of picture text -->
Oeusis<br><!-- End of picture text -->

# **Welcome to 10 years of CMSIS** 

- Armv8.1-M enhancements that improve DSP and ML performance 

- Secure Debug: Reference implementation with CMSIS-DAP 

- CMSIS-Zone system partitioning and TrustZone setup 

- PSA (Platform Security Architecture) and Trusted Firmware-M 

- How CMSIS and TF-M software packs simplify IoT 

- CMSIS roadmap & discussion 

IMPORTANT: This presentation will be available here: **<u>https://github.com/arm-software/cmsis_5</u> - CMSIS_EW2019.pdf** 



<!-- Start of picture text -->
arm<br><!-- End of picture text -->

2 2019 Arm Limited 

## CMSIS has 10 years of history – how it began! 



<!-- Start of picture text -->
w COMPLIANT<br><!-- End of picture text -->



<!-- Start of picture text -->
Making the News: CMSIS Pre: CMSIS — Lead<br>Industry puts weight ® Silicon Partners<br>Cmsis software standard = Atmel<br>troller software interface stan- for safety requirements. = Luminary<br>dard), and acts as a vendor-inde- Fabless semiconductor<br>pendent hardware abstraction my Luminary Micri = NXP<br>layer for the Cortex-M series,<br>“Embedded developers re-use involved“It ts thein developingsoftware thC 7 i<br>4<br>Reinhard Keil: Keil, Anm’s director for MCU marketing officer Jear<br>to reduce complexity.”“Our goalis tools.code from“But otherpurchasedsourcescodeis andnot Booth.support “Weon ourwill Stellarishave fu<br>Thatoften integratedtinea theeinto  kaa.the project. controllersST Mucosetonce,early next ye =» ~SOftware Partners<br>a d ard,ardso we came up witha stan- has standardised on Co<br>x. Cmsisthatshould solves this.”let silicon ven- alsoits 32bit_given itsmicrocontrothbacking to = IAR Systems<br>F dors and middleware providers ~Therefs a greater goo /<br>ites Lacing area epeieend gosabeg KEIL, An ARM<br>sofwareJean AnnethatBoo t h:akes“It isthe t heime.” lyreduceintegrated.the learningIt shouldcurve alsofor ofston.STM’s“It servesmicrocontrollall our in = Micriumoe<br>“if , 4\ newCreatingmicrocontrollersoftware developers,is seen as wehavecollaborateflexibility. soWe ourcann cu = SEGGER<br>one of the major casts in the differences with our cor<br>embedded industry. Stand to undermine our cur<br>ardising the software interfaces routes to market.<br>| across all Cortex silicon vendor NXP is sampling<br>q products has the potential to LPCAxx family<br>Jim Nicholas: "There is a reduce this cost significantly, wets and is planningof Cort a Open Source<br>greater good.” especially when creating projects availability early nex<br>for new deviers or mioratine which ix why it ha<br><!-- End of picture text -->



2019 Arm Limited 

3 

## CMSIS 10 years later – where are we today? 



CMSIS is the pathway to the Arm microcontroller eco-system of tools and software 



<!-- Start of picture text -->
er<br><!-- End of picture text -->

Trillions of 

- Support for **all Cortex-M, Cortex-A5, A7, A9** 



<!-- Start of picture text -->
devices<br>use CMSIS<br><!-- End of picture text -->

- Open source – development public on GitHub: <u>https://github.com/ARM-software/CMSIS_5</u> with good contributions – thank you! 

5,500+ MCUs / ASSPs supported with CMSIS poorooonoony —i— SS Used in many projects 



<!-- Start of picture text -->
Go gle CMsIs<br>About 446.000 results<br><!-- End of picture text -->

   - **32 silicon vendors** that provide public CMSIS device family packs 

- 8,000,000 source files public on GitHub 



- CMSIS pack support in **various IDE/toolchains** : - Arm DS 

   - Arm Keil MDK 

   - IAR EWARM 

   - <u>github.com/ARM-software/cmsis-pack-eclipse</u> (which enables several vendor specific tools) 

CMSIS installations 260.000 downloads of CMSIS-Pack 5.4.0 



<!-- Start of picture text -->
arm<br><!-- End of picture text -->

4 2019 Arm Limited 



Armv8.1-M enhancements that improve DSP and ML performance 

### CMSIS enables consistent software for all Cortex-M (& A5/A7/A9) 



<!-- Start of picture text -->
Cortex-M today<br>+45 billion<br>Cortex-M  Future Cortex-M<br>based chips<br>Cortex-M7* based on Armv8.1-M<br>shipped**<br>-<br>od<br>Enabled by Arm Helium<br>Cortex-M35P*<br>Cortex-M33*<br>technology<br>Cortex-M3<br>Cortex-M4*<br>Cortex-M23<br>Cortex-M0+<br>Cortex-M0<br>Cortex-M1<br>Relative control code performance<br><!-- End of picture text -->

**Based on Arm data 

*Existing processors with DSP extensions 

Relative ML and signal processing performance 



2019 Arm Limited 

6 

Graph not to scale 

## Evolving the architecture for more capable, secure devices 

#### Armv8.1-M 

- Support for half-precision floating-point, loops and branches 

- • Additional debug features for signal processing 

• Helium Additional debug features for signal processing • Enhanced error reporting using Reliability, Availability and M-Profile Vector Extension Serviceability (RAS) extension Armv8.0-M mainline Built-in security with TrustZone for Armv8-M and PSA principles ~~<mark>p</mark>~~ <mark>t</mark> <u>developer.arm.com/technologies/helium</u> 



2019 Arm Limited 

7 

Transforming the capabilities of the smallest devices Helium is boosting signal processing and ML performance for millions of developers 

##### Signal processing 

##### Machine learning 



<!-- Start of picture text -->
Signal  Feature  Decision<br>conditioning extraction algorithm<br>Up to 5x<br>Up to 15x<br>higher signal<br>higher ML<br>processing<br>performance*<br>performance* (matrix multiplication in<br>(CFFT in int32)  int8)<br><!-- End of picture text -->

*Compared to existing Armv8-M implementation 



2019 Arm Limited 

8 

Simplified software development based on a unified programmer’s view ~~Unified toolchain for control code, signal processing and ML~~ Optimized library for Optimized library signal processing CMSIS-DSP library CMSIS-NN library for ML ~~<u><mark>c</mark> e</u>~~ <u><mark>eee</mark></u> ~~<u><mark>e|</mark></u>~~ <mark>Armv8.1-M and Helium</mark> Signal processing Machine learning Efficient control code execution 



2019 Arm Limited 

9 

## Armv8.1-M Code Example: Vector Addition 

#### Code Snippet 

#### Assembly Snippet with Helium 

```
voidmatrix_add_const(ee_u32N,MATDAT*A,MATDAT
val)
{
ee_u32i,j;
for(i=0;i<N;i++)
{
for(j=0;j<N;j++)
{
A[i*N+j]+=val;
}
}
```

```
}
```

`wlstp.16 lr, r5, exit` Low Overhead Loop Instruction variant Note: This variant is to enable loop tail predication `.LBB2_5 : vldrh.16 q0, [r6]        @ load 8 half words vadd.i16 q0, q0, r0      @ add val to 8 half words vstrh.16 q0, [r6], #16   @ store 8 half words letp lr, .LBB2_5` Loop-end with Tail predication `exit:` Note: LR stores no. of vector elements processed in this case. Notes: Above branching performance results in significant cycles savings, thereby giving higher performance, smaller code footprint and better power efficiency 



2019 Arm Limited 

10 



CMSIS Components 

## CMSIS 5 



Consistent software framework for Arm Cortex-M and Cortex-A5/A7/A9 based systems 



<!-- Start of picture text -->
µVision<br>Application code Debugger<br>Debugger<br>CMSIS-Pack<br>CMSIS-RTOS CMSIS-NN CMSIS-DSP CMSIS-Driver Peripheral HAL CMSIS-SVD<br>Real-time execution Machine learning Signal processing Middleware interface Device specific Peripheral description<br>CMSIS-CORE CMSIS-DAP CMSIS-Zone<br>Processor core and peripheral access Debug access System Partitioning<br>Communication  Specialized  CoreSight™ Access Filter<br>Arm ® Cortex ® processor<br>peripherals peripherals debug logic (MPU, SAU)<br>System-on-chip<br><!-- End of picture text -->

#### Complete documentation: <u>http://arm-software.github.io/CMSIS_5/General/html/index.html</u> 



12 2019 Arm Limited 

## CMSIS-Pack – delivery mechanism 



<!-- Start of picture text -->
Delivery<br><!-- End of picture text -->

- Software components, examples, code templates, documentation, device and board support files 

Versioning 

- Semantic versioning for lifecycle management using an embedded industry standard for reliable production 

Dependency 

- Specify dependencies upon other packs, software components, toolchains, and APIs 

Retargeting 

- Automatically replace files based on hardware selection or toolchain requirements 



<!-- Start of picture text -->
arm<br><!-- End of picture text -->

2019 Arm Limited 

13 



<!-- Start of picture text -->
CMSIS-Pack Index Files: Standardization for Download Portals<br>Multiple download portals (all are equal), with references to other portals<br>www.vendorA.com/pack pack.vendorN.com Software Pack vendors publish:<br>•<br>Vendor.pidx : Index file that lists<br>*.pack *.pack all available packs from “VendorN”<br>*.pdsc *.pdsc<br>Tool vendors use this index file to list all<br>vendorA.pidx<br>vendorN.pidx<br>available packs.<br>i<br>Benefits<br>vendorX.vidx:<br>•<br>- Software Pack vendors can update and<br><url> vendorA.pidx<br>-<br><url> vendorN.pidx add packs. This gets automatically<br>4 distributed to tools and web.<br>:<br>•<br>index.pidx Software partners can create packs for<br>software evaluation to promote their<br>— products.<br><!-- End of picture text -->

- Software partners can create packs for software evaluation to promote their products. 



<!-- Start of picture text -->
arm<br><!-- End of picture text -->

14 2019 Arm Limited 

## CMSIS-Pack is designed for tools and web portals Information you publish in packs is shown in tools and on web pages 



<!-- Start of picture text -->
Software Component Sel. Variant Versi.. Description I > GO hitps:/developer.arm.com/embedded/emsisiom..= embedded/emsis/em. fe "1 O |@ +i | € > © @ Armitd (GB) | https//developerarmcom/embedded/emsis/.. tr 1% O @ i .<br>i = :Nee own ox<br>©2 Board Support McB1500 []1.00 |MCB1S00 Board armeveloper Qe Vn Q=ee=e<br>cusis Cortex Microcontroller Software Interface Components Devi<br>@ CORE 3.30.0 |CMSIS-COREfor Cortex-M, $C000, and SC300 P. oards evices<br>% psp r 1.42 | CMSIS-DSP Libraryfor Cortex-M, $C000, and $C300 LD<br>w @ RTOS (AP) 1.0 _ | CMSIS-RTOS API for Cortex-M, $C000, and SC300<br>rs Startup, System Setup<br>start up Fino. 5 ststart for NXP LPC1500Ser i i wooaa NXP > LPC 1817<br>2-® ©DriversEthernet (APD EthernetystemInified DeviceMACStartupandDriversfor PHY Driver APL formiesCortex:M SemiconductorsNordic. > nRF5S1PCA10031 LPC1800 Series > LPC181x<br>& 3 Etherneternet PHYPHY (API)(API 2.00 _| Ethernetthemet PHYDriveriver APIAfl forfor Cortex-MCortex NXP LPC1800 devices are high-speed andoffer extensive<br>8 @ ReFlash arp (APD) | oo2.01 |12C Driver API for Cortex Nordicvelopment Semiconductor Kit board nRF51 (PCA10031) communicationIndustrial, RFID peripherals. Typicalreaders, Consumer, applications e-Metering and include White<br> @ NAND% 2 (AP) a 1.01.02.00 __|_|I2CNAND Driver for Flash Driver LPC1500API Series for Cortex-M p Information marked : goods. - Three PLLs - Quad3CT) SPI Flash interface-LCD Controller (SPIFI) -<br>@File@ USBUSBSystemDeviceDevice(API (APD 2.006.0.0 _| | File USB AccessDeviceHes onDriverDrivervarious APL API  storageforfor Cortex-Mdevices Support pack: SoftwareSemiconductor modules nRF for famil Nordic. PUBLIC *T-© IDID ForMotor eachcontrolrorenhendevice PWM for<br>i ® Graphics MDK-Pro |5.24.0 User Interface on graphical LCD displays " y- ————_<br>& MyClass Support pack: NXP LPC1800 Series Device Support,<br>8-@ Network MDK-Pro (6.0.0 _|IP Networking using Ethernet or Serial protocols [ Downloadltest & |<br>© use MDK-Pro [6.0.0 | USB Communication with various device classes Compatible Arm development tools:<br>a 0 ‘Arm Development Studio Compatible Arm development tools:<br>Validation Output Description KeIMDK Arm Development Studio<br>‘Arm Compiler Kei MOK<br>ULINK and DSTREAM debug adapter fgfnilies Arm Compiler<br>ULINK and DSTREAM debug adapter families<br>(Resse|} (__Detais_) Cored Heb<br><!-- End of picture text -->



15 2019 Arm Limited 

## CMSIS-Pack – what‘s new? 

#### **Work with repositories** 

- _<u><repository></u>_ element specifies version control ~~es~~ location, i.e. **git** or **GitHub** 

- IDE’s support “local repositories” workflow 

#### **Eclipse CMSIS-Pack v2.4.0 released** 

- <u>https://github.com/arm-software/cmsis-pack-eclipse</u> ~~Coo~~ 

- • Many enhancements, for example: Headless build: `eclipsec.exe -nosplash -application com.arm.cmsis.pack.project.CmsisHeadlessBuilder –help` 

#### **Flash programming via DAP interface** 

- _<u>< flashinfo></u>_ describes sequence-based flash 

- download – required for devices that cannot execute algorithm from RAM. 



<!-- Start of picture text -->
(DHelp 8 BeEed 4)OO=zETH<br>BS Contents 9? Search &8 Related Topics Ol Bookmarks [@ Index<br>Using Local Repositories<br>All versions of installed packs are stored below the pack root folder (refer to CMSIS Pack Manager). While<br>developing a software pack, it is useful to have direct access to its content without the need to re-build and re-<br>install the pack after modifications. For this purpose, you can add the folder of a pack’s local copy by selecting<br>y Manage Local Repositories... and pressing Add.... Select the PDSC file in the folder and press OK:<br>8% Preferences Oo x<br>type filter text Manage Local Repositories RY Ory<br>> General<br>> Arm DS Pack Repository<br>Q> occMsis packs MyVendor.MVCM3.1.0.9 —_C:/06_temp/working/Files/. [Remove |<br>Console<br>Manage Local Repositories<br>> Help<br>> Install/Update<br>> Java<br>Library Hover<br>> PyDev<br>> Remote Systems<br>> Run/Debug<br>> Team<br>> Terminal =e a<br><!-- End of picture text -->



16 2019 Arm Limited 



<!-- Start of picture text -->
Relationships of packs and software components<br>• Packs  can require other packs to be installed:<br>Pack A Pack B<br>Version n Version m<br>a ee<br><!-- End of picture text -->

- **Components** <u>can have dependencies</u> on other components; either from the same or from other packs: 



<!-- Start of picture text -->
Pack A, Version n Pack B, Version m<br>Component A Component B Component C Component A Component B Component C<br><!-- End of picture text -->



2019 Arm Limited 

17 

## CMSIS-Pack: What is a software component 



<!-- Start of picture text -->
API Interface<br>Software<br>Component #1 API headers Documentation<br>Version &<br>License<br>Source code/ Configuration<br>Information<br>libraries files<br>References to other software components<br>API headers API headers API headers<br>Source code/ Source code/ Source code/<br>libraries libraries libraries<br>SW Component #2 SW Component #3 SW Component #4<br><!-- End of picture text -->

<u>Software components</u> should have: 

- Version and history information 

- License information 

- API interface definition 

- Documentation 

- Source files 

- Configuration files (optional) 

- Requirements to other components (optional) 

<u>CMSIS-Pack defines an XML format that frames all this</u> information and can be used by project management utilities from various tools. 



18 2019 Arm Limited 

## CMSIS-Pack: Central API Interface definition 

Ensuring consistent interfaces across standard components 



<!-- Start of picture text -->
Interfaces<br>Software<br>component API headers<br>Source code/<br>libraries<br>Central<br>API headers Documentation<br>API definition<br>(Definition) of API<br>Source code/ Source code/ Source code/<br>libraries libraries libraries<br>Implementation #1 Implementation #2 Implementation #3<br><!-- End of picture text -->

A common problem: API headers evolve over time. A central API definition shares header file and documentation of an <u>API interface</u> across multiple other software components to ensure consistency. The <u>API interface</u> is distributed separate or as part of the software component that defines this interface. The API header file is therefore consistent. 

An example is the <u>CMSIS-Driver pack that contains</u> various Ethernet and Flash drivers – all compatible with the CMSIS-Driver APIs that are published in the CMSIS Pack. 



19 2019 Arm Limited 

###### **<u>CMSIS-Driver Templates</u>** 

**GitHub projects:** CMSIS-Driver Implementations for **<u>NPX LPC Series</u>** 



<!-- Start of picture text -->
CMSIS-Driver<br>Validation<br><!-- End of picture text -->

20 2019 Arm Limited 

**CMSIS-Driver Pack Generic Drivers** that are device independent are now available as separate software pack. 

<u>github.com/ ARM-software/ CMSIS-Driver</u> 



<!-- Start of picture text -->
arm<br><!-- End of picture text -->

## CMSIS-Driver: WiFi Interface (beta available) 

#### Standard interface to WiFi chipset 

##### **WiFi** 

###### CMSIS-Driver 

Management Socket Bypass (opt.) 

- <u>WiFi CMSIS-Driver</u> that provides access to: 

   - Management interface: connection to an access point (AP) 

   - Socket interface: IP stack running on WiFi module handles data communication 

   - Bypass interface: IP stack is running on MCU; Ethernet frames transferred by WiFi module 

- WiFi CMSIS-Driver is typically implemented as: 

   - Wrapper for SDK for WiFi module 

   - May use CMSIS-Driver compliant implementation for SPI, SDIO or UART connection 

SPI, SDIO, UART CMSIS-Driver 

- Beta implementation available for: 

   - <u>ISM43362</u> – **Inventek WiFi ISM43362** driver using CMSIS-Driver SPI interface 

   - <u>QCA400x</u> – **Qualcomm WiFi QCA400x** driver using CMSIS-Driver SPI interface 

   - WiP – release April 2019: **Redpine Signals RS14100** on chip WiFi 

   - WiP – release April 2019: **Espressif ESP8266 WiFi Arduino shield** 

- CMSIS-Driver template will be available to add custom WiFi chipsets 



21 2019 Arm Limited 

WiFi Driver and IoT Socket component combined Generic communication foundation for Cloud connectors on Cortex-M Cloud Connector © Google CloudPlatform <u><3</u> % Azure Security Security Security Security is provided by Mbed Mbed TLS Mbed TLS Mbed TLS <mark>EE ee ee</mark> ~~—~~ IoT Socket can interface with: IoT Socket IoT Socket IoT Socket <mark>ee ee</mark> • WiFi CMSIS-Driver to connect to various wireless WiFi Middleware lwIP chipsets CMSIS-Driver MDK <mark>ee i ee</mark> • MDK-Middleware network stack SPI,SDIO,UART Ethernet MAC Ethernet MAC • LwIP (optional, WiP – contributions welcome) CMSIS-Driver CMSIS-Driver CMSIS-Driver <mark>a ee ee</mark> Implementations available via Ethernet PHY Ethernet PHY CMSIS-Driver CMSIS-Driver (update for WiFi planned in April 2019) <mark>a</mark> 





<!-- Start of picture text -->
@WS<br>SI<br><!-- End of picture text -->

> Security is provided by Mbed ~~—~~ <u>Mbed TLS</u> 

IoT Socket can interface with: 

- WiFi CMSIS-Driver to connect to various wireless chipsets 

- MDK-Middleware network stack 

- LwIP (optional, WiP – contributions welcome) 

- Implementations available via <u>www.keil.com/IoT</u> (update for WiFi planned in April 2019) ~~a~~ 



<!-- Start of picture text -->
arm<br><!-- End of picture text -->

22 2019 Arm Limited 

## Other CMSIS improvements 

#### CMSIS-RTOS2 implemented by: 

- <u>FreeRTOS</u> 

- • <u>RTX5</u> ~~———~~ 

- <u>Zephyr</u> 

FreeRTOS and RTX5 available for: 

- Arm Compiler 5 / 6 

- GCC Compiler 

- IAR Compiler 



<!-- Start of picture text -->
Ready-to-use functional safety software framework<br>Run-time system for functional safety (FuSa RTS) for embedded applications<br>User Application code * Faster time-to-market<br>fs rusartxrtos oh... * Fully qualified for:<br>i “ Fusa  &f ey + ISO 26262, ASILD<br>Event ee. * EC 61508, sIL3<br>i Recorder \ run-time verification + IEC 62304, Class C<br>~ EN'50128, SILA<br>FuSa CMSIS-Core<br>| (Arm-Core specific) i (deuce pectic) * Optimized by the<br>i ' | architecture experts<br>i FuSaC library H<br>a ________________________________________________| «© Qne-stop shop for all<br>Arm Cortex-M processor software components<br>15 @ 2019 armUmited arm<br><!-- End of picture text -->



2019 Arm Limited 

23 



# Secure Debug 

Reference implementation with CMSIS-DAP 

### CMSIS-DAP: v1.2.0 (USB HID) + v2.0.0 (WinUSB) 



<!-- Start of picture text -->
Debug Unit Device<br>JTAG/<br>Host PC<br>SWD CoreSight<br>Cortex-M4<br>USB SWO<br>Debugger CMSIS-DAP<br>CoreSight<br>Cortex-M23<br>Many platforms supported<br>CoreSight<br>Firmware implemented<br>Cortex-A7<br>on Cortex-M MCU<br>May be integrated on a single evaluation board<br><!-- End of picture text -->

- **CMSIS v1.2.0** : continues to support USB HID as interface 

- **CMSIS v2.0.0** : introduces USB WIN support with >5x better performance 

   - SWO streaming via separate pipe allows significant better trace bandwidth 

   - Windows 10 does not require USB driver installation 

**Now working towards secure debug, learn more in this video:** <u>http://bit.ly/2TRO6J8</u> 



25 2019 Arm Limited 



<!-- Start of picture text -->
coMPortI/0 Driver<br><!-- End of picture text -->



26 2019 Arm Limited 



<!-- Start of picture text -->
Host Debug Software Target Debug Hardware/Software<br>ATP<br>All these are<br><!-- End of picture text -->



<!-- Start of picture text -->
ICom<br><!-- End of picture text -->



<!-- Start of picture text -->
All these are<br>standard<br>interfaces with<br>specifications to<br>be released by<br>Arm along with<br>reference<br>implementations<br><!-- End of picture text -->



<!-- Start of picture text -->
SDM<br>u<br>ECom rr<br>:<br>:<br>:<br>CSAPBCOM<br>au<br>i OM A O Driver<br><!-- End of picture text -->



<!-- Start of picture text -->
This allows wide<br>adoption and<br>support in all<br>popular debug<br>tooling<br><!-- End of picture text -->



<!-- Start of picture text -->
arin<br><!-- End of picture text -->

2727 2019 Arm LimitedConfidential © ARM 2017 



CMSIS-Zone system partitioning and TrustZone setup 

CMSIS-Zone – resource management for SoC systems Supports partitioning of multi-processor systems; TrustZone and MPU configuration 

System List available system resources Resources in a SoC system 

Select resources for sub-partitions i.e. independent software projects 

System Partitioning 

Partition memory & peripherals for safe process execution 

TrustZone & MPU Setup 

Generate hardware configuration and tool setup 

Build 



<!-- Start of picture text -->
@ MCBSTM32F400.szone °% “oa<br>3 System Map {& | + % Generate code © |a)<br>Name Access Size Cortex-M4 Description a<br>~ & memory<br>* IRAM1 rwx 128 KB 0x20000000<br>> @ IRAM2 rwx 64 KB 0x10000000<br>% IROM1 rx 1 MB 0x08000000<br>v & peripherals<br>>» M ADC<br>> M@CAN<br>> CRC prw 1 KB 0x40023000 Cryptographic processor<br>* DAC prw 1 KB 0x40007400 _Digital-to-analog converter<br>* DBG prw 1 KB 0xE0042000 Debug support<br>* DCMI prw 1 KB 0x50050000 Digital camera interface<br>>» MDMA<br>> % Ethemet<br> EXTl prw 1 KB 0x40013C00 External interrupt/event<br>FLASH prw 1 KB 0x40023Cc00 FLASH<br>* FSMC prw 1 KB 0xA0000000 Flexible static memory contrc<br>» M%GPIO v<br>System map Project zone map| Blinky_MPU | CoProc<br><!-- End of picture text -->



29 2019 Arm Limited 

## CMSIS-Zone – Development workflow 

Configuration and build management for system resources 

Resources Assignments *.rzone **+** *.azone Sub-system Resources *.rzone 4 McBSTM32400szone £2 =o EE 



<!-- Start of picture text -->
& System Map && (8 + @ Generatecode OF<br>Name Access Size Cortex-M4 Description a<br>v ® memory<br>@IRAMI wx 128 KB 0x20000000<br>> @IRAM2 — rwx 64 KB 0x10000000<br>@IROMI rx 1 MB 0x08000000<br>~ &i peripherals<br>> anc<br>> @ CAN<br>* CRC prw 1 KB 0x40023000 Cryptographic processor<br>* DAC prw 1 KB 0x40007400 _Digital-to-analog converter<br>* DBG prw 1 KB 0xE0042000 Debug support<br>* DCMI prw 1 KB 0x50050000 _ Digital camera interface<br>> @DMA<br>> @ Ethernet<br>+ ExT prw 1 KB 0x40013C00 _ External interrupt/event<br>® FLASH prw 1 KB 0x40023C00 FLASH<br>% FSMC prw 1 KB 0xA0000000 Flexible static memory contre<br>~ @GPIO v<br>System map | Project zone map Blinky MPU  CoProc<br><!-- End of picture text -->

Hardware Configuration 



Tool Configuration 

Resource *.rzone file lists all systems resources. Import from CMSIS-Pack/SVD possible 

Assignment *.azone file contains partitioning information and is managed by CMSIS-Zone tool 

CMSIS-Zone tool can generate subsystem resource files 



30 2019 Arm Limited 

## CMSIS-Zone – Development Workflow 

Multi-step approach shows only relevant sub-system 



<!-- Start of picture text -->
Sub-system<br>Resources<br>*.rzone<br><!-- End of picture text -->



<!-- Start of picture text -->
Assignments<br>*.azone<br><!-- End of picture text -->

**+** 



<!-- Start of picture text -->
@ MCBSTM32F400szone °% =o<br>& System Map && (8 + @ Generate code 0)<br>Name Access Size Cortex-M4 Description a<br>v ® memory<br>@IRAM1 = rwx 128 KB 0x20000000<br>@IRAM2 — rwx 64 KB 0x10000000<br>@1ROM1 rx 1 MB 0x08000000<br>~ &i peripherals<br>#% ADC<br>> SCAN<br>* CRC prw 1 KB 0x40023000 Cryptographic processor<br>* DAC prw 1 KB 0x40007400 _Digital-to-analog converter<br>* DBG prw 1 KB 0xE0042000 Debug support<br>* DMI prw 1 KB 0x50050000 _ Digital camera interface<br>> MDMA<br>> @ Ethernet<br>+ ExT prw 1 KB 0x40013C00 _ External interrupt/event<br>® FLASH prw 1 KB 0x40023C00 FLASH<br>> FSMC prw 1 KB 0xA0000000 Flexible static memory contre<br>v %GPIO v<br>System map | Project zone map | Blinky MPU CoProc<br><!-- End of picture text -->



<!-- Start of picture text -->
Sub-sub-system<br>Resources<br>*.rzone<br><!-- End of picture text -->

Hardware Configuration 



Tool Configuration 

It is possible to break down complexity of a system in multiple steps. 

Sub-systems expose only the part of the system that is relevant for the user. 

A sub-system user has no visibility to other parts of the system (access protection). 



31 2019 Arm Limited 

## CMSIS-Zone – configuration steps - example 

- Step 1: split the multi-processor system into single processor sub-systems. 

- Step 2: create the partitions for secure and non-secure execution. 

- Step 3: configure MPU protected execution zones. 



<!-- Start of picture text -->
SecureDebug Cortex-M33ee pm2 Cortex-M33rye —pat i aay DebugSecure Cortex-M33ae)pe oera<br>instruction Instruction TrustZone instruction TrustZone 5<br>Cache Cache Fiters Cache Fitters<br>Muttiayer AH8S interconnect Muli-layer AHBS interconnect<br>AHBS AHBS ;<br>A nd TrustZone TrustZone TrustZone TrustZone Spe TrustZone<br>interface Filters Filters Filters Fitters interface Fitters<br>TrustZone SRAM SRAM SRAM TrustZone SRAM<br>Filters Cnt Crt Cott Fitters Crit<br>AM AN RAK CryptoCell Code, SRAM17 RAM<br><!-- End of picture text -->



2019 Arm Limited 

32 

## CMSIS-Zone – data export for projects 

FreeMarker template engine allows to export CMSIS-Zone data to arbitrary formats 

Flexible data export for project build supports many different use cases: Build i.e. device configuration, MPU setup, linker scripts, etc. y 

Flexible data export for project build supports many different use cases: i.e. device configuration, MPU setup, linker scripts, etc. @ MCBSTM32F400.szone @Blinky_MPU.pzone [2<sup>scatter.</sup> 



<!-- Start of picture text -->
9LR_flash 0x08000000 0x00080000 { ; lo<br>10  ER_flash 0x08000000 0x00080000 { ;<br>11 *.o (RESET, +First)<br>12 * (InRoot$$Sections)<br>13 -ANY (+RO)<br>14 -ANY (+X0O)<br>15 }<br>16 RW_priv 0x20000000 0x00008000 { ; E<br>17 -ANY (+RW +ZI)<br>18 -ANY (.data.priv*)<br>19 -ANY (.bss.priv*)<br>20 }<br>21 RW_shared 0x20008000 0x00008000 { ;<br>22 -ANY (.data.shared*)<br>23 -ANY (.bss.shared*)<br>24 }<br>25  RW_processA 0x20010000 0x00000200 {<br>26 -ANY (.data.processA*)<br>27 -ANY (.bss.processA*)<br>28 =}<br>29  RW_processB 0x20010400 0x00000200 {<br>30 -ANY (.data.processB*)<br>31 -ANY (.bss.processB*)<br>«<<br><!-- End of picture text -->



<!-- Start of picture text -->
Project files for:<br>file templates<br>▪ Memory assignments<br>FreeMarker ▪ Linker configuration<br>CMSIS-Zone<br>▪<br>SAU, MPU configuration<br>Generator<br>Data Model ▪ Peripheral assignments<br><!-- End of picture text -->

33 2019 Arm Limited 



Platform Security Architecture, Trusted Firmware-M and CMSIS alignment 

Shebu V. Kuriakose 

~ <sTrusted + +++3 3 ++++++. 4 PA Firmware-M 4 <e. + + , + + + (TF-M) + + + + To Secure Trillion Connected Devices 



<!-- Start of picture text -->
+ + + + : Te} + + + + + + + +<br>++++++++++++++++<br>Shebu V. Kuriakose ‘<br>+<br>+ a F + f. + + ‘ + + + + + + +<br><!-- End of picture text -->

Platform Security Architecture A complete security offering independently tested 



<!-- Start of picture text -->
Analyze Architect: Implement Certify,<br>——<br>=}<br>Threat models Hardware & firmware Firmware<br>& security analyses architect specifications source code<br>a E B z<br>— = Da 2 OA<br>er Za So psacertified™<br><!-- End of picture text -->

Find out more at **2pm on 28**<sup>**th**</sup> **February** with Rob Coombs: Building Trust: Evaluating Platform Security Architecture (PSA) 

## Trustedfirmware.org Open Source, open governance Openly published 



<!-- Start of picture text -->
Sea== oo<br>a<br>OPEN SOURCETRUSTEDSECUREFIRMWAREWORLD SOFTWARE<br><!-- End of picture text -->



2019 Arm Limited 

36 

Trusted Firmware-M Framework Secure Boot, Isolation, Secure Partition 



<!-- Start of picture text -->
Non-Secure<br>Processing<br>Environment<br><!-- End of picture text -->



<!-- Start of picture text -->
Secure Processing<br>Environment<br><!-- End of picture text -->





<!-- Start of picture text -->
Non-secure Partition Secure Partition Secure Partition Trusted Partition<br>TF-M Core<br><!-- End of picture text -->



2019 Arm Limited 

37 

## TF-M v1.0-Beta  @ Embedded World’19 

- Secure Boot based on 

mcuboot 

- Level 1 Isolation 

- Secure Storage 

- Crypto Functions 

- Attestation following EAT (Entity Attestation Token) Spec 

- PSA Functional API Certification PSA L1 Security Certification 



<!-- Start of picture text -->
Non-Secure Secure/TF-M<br>PSA Test Suite*<br>TF-M Core (SPM, Interrupt Handling) Secure Boot<br>RTOS<br>HAL API<br>HAL<br>TBSA-M Hardware<br>TF-M PSA RoT Application  * Containing Test Suite of<br>(Secure  RoT PSA Crypto, Secure<br>Privileged  Storage & Attestation<br>APIs<br>PSA Storage  APIs Storage PSA Crypto  APIs Crypto PSA Attestation  APIs Attestation<br>PSA Dev APIs<br><!-- End of picture text -->

PSA RoT (Secure Privileged Domain) 

Isolation Boundary TF-M 



38 2019 Arm Limited 

## Trusted Firmware-M: Enabling a Secure Ecosystem 

- Sample Integration with RTOS **RTX5 RTOS** 

- arm g 

- • CMSIS Packs • Standardized PSA APIs MBED Yess (éRTOS) on 

- Standard HAL Interface 

- Public Mailing List: Open Design and Review 

##### Secure/TF-M 

##### Non-Secure 



<!-- Start of picture text -->
PSA Test Suite*<br>TF-M Core  (SPM, Interrupt Handling) Secure Boot<br>RTOS<br>| as<br>HAL API<br>Ee HAL<br>TBSA-M Hardware<br>Storage Crypto Attestation<br>PSA Storage  APIs PSA Crypto  APIs PSA Attestation  APIs<br>PSA Dev APIs<br><!-- End of picture text -->

- Multiple Toolchains 

- Certifiable Friendly 



<!-- Start of picture text -->
arm<br><!-- End of picture text -->

2019 Arm Limited 

39 

## Proof Of Concept: Google Cloud/Zephyr/TF-M 

- Musca-A Board 

   - Arm IoT Reference Platform 

   - – Cortex-M33 core 

- SPE - TF-M 

- NSPE - Google Client on Zephyr RTOS 

- Google Client uses JWT Sign Service and Secure LED Service 

Non-secure Processing Environment (NSPE) 

Google Non-secure partition Cloud<sup>——</sup> Google Client 

Zephyr 

Secure Processing Environment (SPE) 



Trusted partition Trusted function Trusted function 

Secure partition 

Secure partition Secure LED Service 

JWT Sign Service 

Secure Partition Manager 

Secure isolation 

Secure debug 

Secure IPC 

Isolation boundary 



<!-- Start of picture text -->
arm<br><!-- End of picture text -->

40 2019 Arm Limited 

TF-M TF-M v1.0 PSA Specs, v1.0-Beta TF-M L2 Certified TF.org PSA Func, PSA v0.1 Launched L1 Certified 

Today 

2019 

Q4’2018 

Q1’2018 

Q3’2017 



41 2019 Arm Limited 

# **Roadmap** 

Released Development Adv. Planning Concept 

**Core (Isolate, Interact, Execute)** Armv8-M Level 2 Isolation, Interrupt Handling, Driver Framework, <mark>LI</mark> © O O Dual v7-M Proto. Full Isolation, Supplicant Support Library Mode Scheduler, PSA IPC Dual Armv7-M Level1 Isolation **Secure Boot** Key Revocation, BL1 Bootloader Multiple Image <mark>+</mark> mcu boot, ‘SS O oO Crypto Hardware, Update, Non-Swapping boot, Rollback Protection mcuboot upstream RAM Loading **Secure Services** PSA APIs IPC Compatibility, Provisioning 0 Protected Storage, © e Oo - Storage, Crypto, - Storage, Crypto, Crypto, Attestation Attestation Platform Initial Attestation Service - Timer, NVCount, NONCE Crypto Hardware, Audit Logging Available 2019 Q1 2019 Q2 Future 



<!-- Start of picture text -->
arm<br><!-- End of picture text -->

42 2019 Arm Limited 



How CMSIS and TF-M software packs simplify IoT end-node development 



<!-- Start of picture text -->
How can we deploy<br>software to all these<br>IoT devices<br>44 2019 Arm Limited<br>Mage<br><!-- End of picture text -->

# CMSIS vision 10 years ago: SW components easy to exchange 



<!-- Start of picture text -->
Software Complexity — The Challenge<br>(Industrial Application) o/s RS232<br>Development Costs s/> aw<br>Ue | cieloe<br>%» & | EREEthernet<br>SD/MD<br>1970 1980 1990 2000 2010 Hardware Components can be easily exchanged<br>= Well-known issues the drive software costs<br>= Increasing product requirements that are implemented by software<br>= Hardware problems tend to become compensated by software<br>= Software components are incompatible and cannot be re-used.<br>Software Standards are key for the future!<br><!-- End of picture text -->

### **Where are we today?** 

- CMSIS-Core, RTOS, DSP, NN, Driver define common SW for variou processors/devices and peripherals 

- TF-M adds security for IoT 

- All relevant silicon vendors deliver device family packs in CMSIS format 

- CMSIS-Pack defines the frame work for software components 

- CMSIS-Pack management is implemented by several mainstream toolchains: IAR, Arm Development Studio, Keil MDK, and SiP toolchains 

- **So, lets apply it….** 



45 2019 Arm Limited 

# Cloud connector software stack and IoT kits 



<!-- Start of picture text -->
: reaies oeSacks | ah ee fieit ee"es “it<br>by : . EFTTe seemmnnmm af di Teoex aT<br>| Suge 7<br>oy 1 (2S) ge ey (RO<br>Ai Pe ail fun Boe § i]<br>= weet oe or we oe<br>= fe Ee<br><!-- End of picture text -->



<!-- Start of picture text -->
tii2, Sg? COGCSS TT Buea ae | fi SC<br>sss,ma  SEs sf> a Zoe aaeeeees<br>[eee : iia : WIFIIOE Module bs<br>mS, e33ies: 2ADPOGT216 z<br>Be? =| [\DY(D)! 2: Ma) 245007687353 [ieee<br>az UNA 2 2 Sm |S<br>Hai Re<br><!-- End of picture text -->



<!-- Start of picture text -->
RE MSIE Se Sy of B<br>ibis<br>ae REY api oe a: iD Teer<br>: bE Sine<br>Paget OTE) ROR, Ui es<br>& cotsa Lg ety |<br>eaI) os tet weSareeAC I<br>ete eee Ee FP i<br>See<br><!-- End of picture text -->



<!-- Start of picture text -->
EERE > a<br>H as<br>aN "26 Re ATE 8 et ae<br>me ae<br>le =a se AP et = ulrwrrarrar epee iis a ©<br><!-- End of picture text -->



<!-- Start of picture text -->
= q<br>i ers =<br>ay ahs Ke Your Own THINGS<br>i ““"@<br><!-- End of picture text -->



<!-- Start of picture text -->
Sao<br>RBS,}<br>Zaks ios Ss ae oe<br>\‘e sex aeie 82eerOewe ote, a 4 *<br>Pes¢ weesante y L<br>De & BY<br>oe‘Op ess<br><!-- End of picture text -->



46 2019 Arm Limited 

# Cloud connector software stack – framed in packs 

### Application code 

## Proof of Concept 

Cloud connector and service 

WiFi Secure Socket Software Connector CBOR JSON SDK Driver Security Update Key Service TinyCBOR Jsmn WiFi mbed TLS Service 

SDK Project Template Board configuration Device CMSIS SDK Drivers SDK Drivers RTOS Startup CORE _All_ Flash 

<mark>Benefit: easy to add new components.</mark> SiP <mark>can differentiate!</mark> 

Cloud connector stack re-worked to use software packs. 

PoC separates common software components: now it is simpler to re-use and update. 

**Seven components are hardware dependant and need rework to adopt a new target hardware.** 

<mark>CMSIS pack</mark> 

<mark>RTOS pack Cloud pack</mark> 

<mark>BSP</mark> 

<mark>DFP</mark> 

<mark>3</mark><sup>rd</sup> <mark>party pack Mbed TLS pack</mark> 



47 2019 Arm Limited 

# Adding WiFi Driver and IoT Socket packs 

Application code Cloud connector and service 

WiFi IoT Socket CMSIS-Driver CBOR JSON WiFi Security Update Key Service TinyCBOR Jsmn SDK mbed TLS Service SDK Project Template SPI/UART Board configuration CMSIS-Driver Device CMSIS SDK Drivers SDK Drivers RTOS Startup CORE _All_ Flash 

Utilizing generic WiFi, Networking, and IoT Socket packs can further reduce efforts of hardware adoption. 

WiFi chipsets frequently interface via SPI. Utilizing the CMSIS-Driver interface makes it generic. 

<mark>BSP</mark> 

<mark>DFP</mark> 

<mark>3</mark><sup>rd</sup> <mark>party pack</mark> 

<mark>Mbed TLS pack</mark> 

<mark>Com pack</mark> 



<mark>CMSIS pack RTOS pack</mark> 

<mark>Cloud pack</mark> 

48 2019 Arm Limited 

# Cloud software stack on Armv8-M with TrustZone 



<!-- Start of picture text -->
Application code<br>Cloud connector and service<br>WiFi<br>IoT Socket<br>CMSIS-Driver<br>CBOR JSON WiFi TF-M TF-M TF-M<br>TinyCBOR Jsmn SDK Crypto NS Storage NS Boot NS<br>SDK Project Template SPI/UART<br>Board configuration CMSIS-Driver<br>Device CMSIS SDK Drivers TF-M TF-M<br>RTOS<br>Startup CORE All IPC CORE<br>Non-secure Secure<br>Alignment with CMSIS and TF-M can simplify security, crypto, and firmware update<br>CMSIS pack RTOS pack Cloud pack BSP DFP 3 rd party pack Mbed TLS pack Com pack<br>Flash<br>Driver Driver<br>Memory<br>Hardware  Accelerator<br>Hardware Interfaces<br>Boot<br>Crypto<br>Storage<br>PSA Services<br><!-- End of picture text -->

CMSIS + TF-M can drastically simplify software configuration to custom hardware 



49 2019 Arm Limited 

#### **CMSIS timeline Description** 

#### **How you can contribute** 

April 2019 **CMSIS v5.5.0** release with: Review live repository on - Core(M): Armv8.1-M support <u>https://github.com/arm-software/cmsis_5</u> - Driver: WiFi API Use ‘ **<u>Issues</u>** ’ to report problems or raise requests - DSP: resolved reported issues April/May 2019 WiFi driver implementations and WiFi chip set vendor: <u>add your own driver IoT Connector</u> release Tool vendor: <u>adopt projects to your toolchain</u> April 2019 **CMSIS-Zone** beta version: Feedback on <u>current CMSIS-Zone specification</u> - examples: for v8M devices Review example projects, adapt examples to April – June - heterogenous system setup your toolchain or RTOS - RTX5 with MPU protection Open source project with examples on July 2019 **CMSIS-Zone** final release <u>https://github.com/arm-software/CMSIS-Zone</u> June 2019 TF-M with generic HAL tbd 

June 2019 TF-M with generic HAL adopted to several Cortex-M23/33 

Outlook CMSIS-DAP: Secure Debug reference implementation CMSIS-SVD: extensions for v8-M devices to provide data to CMSIS-ZONE CMSIS-Pack: Generic project file format 



50 2019 Arm Limited 



The Arm trademarks featured in this presentation are registered trademarks or trademarks of Arm Limited (or its subsidiaries) in the US and/or elsewhere. All rights reserved. All other marks featured may be trademarks of their respective owners. 

www.arm.com/company/policies/trademarks 

