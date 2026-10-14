---
title: "Esp32_Flashing"
source_file: "qorc-sdk/qf_vr_apps/qf_vr_aec_app/ESP32_Wifi/Esp32_Flashing.pdf"
pages: 3
sha256: fe4df494179d801db49ce092f64e9d20969f6bf043332d3f6c35702077155818
---

# Esp32_Flashing

# How To Flash Adafruit ESP32 HUZZAH32 Feather Board? 

Note: More information about HUZZAH32 Feather Board can be found at 

<u>https://learn.adafruit.com/adafruit-huzzah32-esp32-feather</u> 

ESP32-HUZZAH32 uses a SiLabs CP210x, USB to UART Bridge on board. The Driver can be found at 

<u>https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers</u> 

1. Download the ESP32 Flash Tool from the following link. Select “Flash Download Tools (ESP8266 & ESP32 & ESP32-S2)” 

<u>https://www.espressif.com/en/support/download/other-tools</u> 

2. Unzip the file “flash_download_tool_v3.8.5.zip” file (where 3.8.5 is version of the tool). 

3. See the Reference document “Flash_Download_Tool__en.pdf”  in the folder flash_download_tool_v3.8.5\doc 

Read the Section 4 Download for ESP32 series 

4. Make sure all the 3 bin files are available 

   1. bootloader.bin 

   2. partitions_singleapp.bin 

   3. qf_wifi_server_xx_xx_2021.bin 

5. Open the bin file “flash_download_tool_3.8.5.exe” and select “Developer Mode” and then select “ESP32 Download Tool”. (Expand window to see full path of files.” Leave or Set the SPI Speed at 40MHz, SPI Mode “DIO” and Flash size 32Mbits 

   - a. Set the COM port number by pulling down the scroll (at the bottom of the window) 

   - b. Set the baudrate to 961800 

   - c. Click on the browse button (..) and select “bootloader.bin” 

   - d. Fill the start address(@) as 0x1000 

   - e. Browse and select “partitions_singleapp.bin”. Fill the start address 0x8000 

   - f. Browse and select “qf_wifi_server_xx_xx_2021.bin”. Fill the start address 0x10000 

   - g. Put Ticks (ie select) in the 3 square boxes at the start ( **See Figure 1 below** ) 

   - h. Click on “Start” below the green IDLE button 

If all the parameters are correct, it should finish flashing and show FINISH in the green button as shown in **Figure 2 below** . Then close the Flash Download windows to exit. 



<!-- Start of picture text -->
| /sPIDowelosd |HSPIDownlosd | GPOCoMfg<br>(2 [GAG agicigoresakewAg ve appe\G_ Faw. wilpp\ESP32 Wit\bootloaderbin| OT) © |ocioc<br>© CNcuitogigoresw vcapp wm vi aplESPS ipattonssngeappbin<br>© [CAQuickLogie qore-sdk- wav appear wif app\ESP32, Wit gf wif. server 02,04.2021bin<br>ie |<br>i |<br>Oi |<br>Ofie<br>oro FF<br>SpiFlashConfig<br>CHEE) CombineBin | [ASH SIZE CiSpiAutoset<br>@40MHz eft | Osnbit (DoNotChgBin<br>O26.7MHz IMODe O 16Mbit<br>© 20MHz eed © 32Mbit; LOCK SETTINGS<br>O20mHz a Ocampit ae<br>ou © 128Mbit<br>@opi0<br>Opout<br>OFASTRD<br>Download Panel 1<br>IDLE<br>aE<br>[sm| soe | ewe |<br>ft<br><!-- End of picture text -->

**Figure 1.** 



<!-- Start of picture text -->
@! ESP32 DOWNLOAD TOOL V3.8.5 - o xX<br>SPIDownload | HSPIDownload | GPIOConfig<br>a<br>apESPEZVMbecoderbin<br>©©©ie[CAQuickLogieCACuiedeggresdkwaCAduildeggoreqore-sak- stealwa vrappe\af.-rwapseapse vowowtwif app\ESP32,apEPEZ VpaitnssnglapptinWit gf wif server02,04=2021.bin ==|. = 0D |OD(010000|<br>i |<br>Oi |<br>oof<br>a<br>SpiFlashConfig<br>@40MHz Deft | Osnbit (DoNotChgBin<br>Sonne, SPI MODE Soe16Mbit LOCK SETTINGS<br>Oaomte Caio Osambit DETECTED INFO<br>Oaout flash vendor:<br>@o10 O 128mbit flash20h: N/AdeviD:<br>Opout 4016h<br>OFASTRD ‘QUAD;32Mbitcrystal:<br>40 Mhz<br>Download Panel 1<br>Fa eit im| AP: 246248018409 STA: 2462ABD1B408<br>PGI) FT: 2462ABDIBADA ETHERNET: 2462A8D18408<br>Sar:— comsao<br>|<br><!-- End of picture text -->

**Figure 2** 

