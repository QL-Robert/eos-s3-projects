# EOS S3 Knowledge Base

Markdown conversions of every PDF in `W:\2026\EOS`, for use as a knowledge database (RAG / search / LLM context).

Each file starts with YAML front matter: `title`, `source_file` (path relative to the EOS folder), `pages`, `sha256`. Text was extracted with PyMuPDF4LLM; image-heavy pages were OCR'd with Tesseract. Figures/images are not embedded — diagram text may be partial.

**39 converted PDFs + 12 notes** · 980 pages

## Datasheets & Reference Manual

| Document | Pages | Source |
|---|---:|---|
| [EOS S3 Ultra Low Power multicore MCU datasheet](<QL-EOS-S3-Ultra-Low-Power-multicore-MCU-Datasheet-2020.md>) | 119 | `QL-EOS-S3-Ultra-Low-Power-multicore-MCU-Datasheet-2020.pdf` |
| [QL EOS S3 Ultra Low Power multicore MCU Datasheet](<QL-EOS-S3-Ultra-Low-Power-multicore-MCU-Datasheet-v3_3d.md>) | 116 | `QL-EOS-S3-Ultra-Low-Power-multicore-MCU-Datasheet-v3_3d.pdf` |
| [QL S3 Technical Reference Manual](<QL-S3-Technical-Reference-Manual.md>) | 363 | `QL-S3-Technical-Reference-Manual.pdf` |

## Application Notes & User Guides

| Document | Pages | Source |
|---|---:|---|
| [GNU Debugger (GDB) Usage](<QL_Application_Note_121_GNU_Debugger_GDB_Usage.md>) | 11 | `QL Application Note 121 GNU Debugger (GDB) Usage.pdf` |
| [QuickLogic® ArcticLink® 3 S2 ULPSH Sensor Fusion Output Specifications](<QL_Application_Note_124_QL_ArcticLink_3_S2_ULPSH_Sensor_Fusion_Output_Specifications.md>) | 6 | `QL Application Note 124 QL ArcticLink 3 S2 ULPSH Sensor Fusion Output Specifications.pdf` |
| [Celeris Studio Integrated Development Environment (IDE) – FFE-GDB Server and Client Setup](<QL_Application_Note_125_Celeris_Studio_IDE_FFE-GDB_Server_and_Client_Setup.md>) | 12 | `QL Application Note 125 Celeris Studio IDE – FFE-GDB Server and Client Setup.pdf` |
| [QuickLogic EOS S3 Application Note 126: Implementing SDMA](<QL_Application_Note_126_EOS_S3_Implementing_SDMA.md>) | 17 | `QL Application Note 126 EOS S3 Implementing SDMA.pdf` |
| [QuickLogic ArcticLink III VX and BX CSSPs –— PCB Layout Guidelines](<QL_Application_Note_128_EOS_S3_Sensor_Processor_Platform_PCB_Guidlines.md>) | 9 | `QL Application Note 128 EOS S3 Sensor Processor Platform PCB Guidlines.pdf` |
| [QuickLogic® EOS S3 Real-Time Operating System (RTOS) Porting Guide](<QL_Application_Note_135_RTOS_Porting_Guide.md>) | 9 | `QL Application Note 135 – RTOS Porting Guide.pdf` |
| [QuickLogic® S3 OPEN – Power Management Software](<QL_Application_Note_136_S3_OPEN_Power_Management_Software.md>) | 13 | `QL Application Note 136 – S3 OPEN – Power Management Software.pdf` |
| [QuickLogic Application Note 139 - QuickLogic® S3 OPEN – QLUART Protocol](<QL_Application_Note_139_S3_OPEN_QLUART_Protocol.md>) | 19 | `QL Application Note 139 – S3 OPEN QLUART Protocol.pdf` |
| [QuickLogic Application Note 140 - QuickLogic® S3 I2S Master/Slave Framework](<QL_Application_Note_140_S3_OPEN_I2S_MasterSlave_Framework.md>) | 12 | `QL Application Note 140 – S3 OPEN I2S MasterSlave Framework.pdf` |
| [Technical Writer](<QL_Application_Note_144_QL_S3LV_Low_Voltage_DVDD_Power_Design.md>) | 8 | `QL Application Note 144 – QL S3LV – Low Voltage DVDD Power Design.pdf` |
| [QuickLogic Application 146 - EOS S3LV Integration Guide](<QL_Application_Note_146_QL_S3LV_Integration_Guide.md>) | 5 | `QL Application Note 146 – QL S3LV Integration Guide.pdf` |
| [Technical Writer](<QL_Application_Note_147_QL_EOS_S3_AEC_2_0_Integration_Guide.md>) | 5 | `QL Application Note 147 – QL EOS S3 AEC 2.0 Integration Guide.pdf` |
| [Technical Writer](<QL_Application_Note_148_QL_S3_DSPC_Noise_Suppression_and_Beamforming_Integration_Guide.md>) | 9 | `QL Application Note 148 QL S3 DSPC Noise Suppression and Beamforming Integration Guide.pdf` |
| [Connecting External Sensors to Merced 1.1 HDK Application Note](<QL_Application_Note_150_Connecting_External_Sensors_to_Merced_HDK.md>) | 12 | `QL Application Note 150 Connecting External Sensors to Merced HDK.pdf` |
| [QL EOS S3 I2C control via M4 App Note](<QL_EOS_S3_I2C_control_via_M4_App_Note.md>) | 15 | `QL EOS S3 I2C control via M4 App Note.pdf` |
| [QL Flash Image Tool User Guide](<QL_Flash_Tool_User_Guide.md>) | 17 | `QL Flash Tool User Guide.pdf` |
| [Technical Writer](<QL_S3_Android_M_ASSP_-_Always_On_Keyphrase_Detection_Performance_and_Validation_Methods_AN_131.md>) | 12 | `QL S3 Android M ASSP - Always On Keyphrase Detection Performance and Validation Methods AN 131.pdf` |
| [QuickLogic S3 Android M ASSP EVK Power Meausrement AB 132](<QL_S3_ASSP_EVK_Power_Measurement_AN_132_1.md>) | 12 | `QL S3 ASSP EVK Power Measurement AN 132  (1).pdf` |
| [QuickLogic S3 Boot Loader](<QL_S3_Boot_Loader_Application_Note_134.md>) | 12 | `QL S3 Boot Loader Application Note 134.pdf` |
| [QuickLogic® S3 OPEN – Batching in Companion Mode](<QL_S3_OPEN_-_Batching_in_Companion_Mode_Application_Note_133.md>) | 13 | `QL S3 OPEN - Batching in Companion Mode Application Note 133.pdf` |

## FPGA Gateware / IP Docs (qorc-sdk)

| Document | Pages | Source |
|---|---:|---|
| [ADC FPGA IP for EOS 3B](<ADC_IF_IP_Rev100.md>) | 13 | `qorc-sdk/s3-gateware/adc_ad7476_if/doc/ADC_IF_IP_Rev100.pdf` |
| [FLL_I2S IP for EOS 3B](<FLL_I2S_register_map.md>) | 9 | `qorc-sdk/s3-gateware/ip_modules/FLL_I2S/docs/FLL_I2S_register_map.pdf` |
| [FLL_I2S FPGA Project for EOS 3B](<FPGA_FLL_I2S.md>) | 7 | `qorc-sdk/s3-gateware/projects/S3_FLL_I2S/docs/FPGA_FLL_I2S.pdf` |
| [UART IP for EOS 3B](<FPGA_UART_1x.md>) | 7 | `qorc-sdk/s3-gateware/projects/S3_FPGA_UART/docs/FPGA_UART_1x.pdf` |
| [UART IP for EOS 3B](<FPGA_UART_2x.md>) | 7 | `qorc-sdk/s3-gateware/projects/S3_FPGA_2xUART/docs/FPGA_UART_2x.pdf` |
| [UART+GPIO FPGA Project for EOS 3B](<FPGA_UART_GPIO.md>) | 7 | `qorc-sdk/s3-gateware/projects/S3_FPGA_UART_GPIO/docs/FPGA_UART_GPIO.pdf` |
| [GPIO IP for EOS 3B](<GPIO_register_map.md>) | 9 | `qorc-sdk/s3-gateware/ip_modules/GPIO/docs/GPIO_register_map.pdf` |
| [UART IP for EOS 3B](<UART_16550_register_map.md>) | 17 | `qorc-sdk/s3-gateware/ip_modules/UART_16550/docs/UART_16550_register_map.pdf` |
| [USBserialport_FPGA_register_map](<USBserialport_FPGA_register_map.md>) | 2 | `qorc-sdk/s3-gateware/usb2serial/docs/USBserialport_FPGA_register_map.pdf` |

## Boards & Schematics

| Document | Pages | Source |
|---|---:|---|
| [chandalar_rev1_0](<chandalar_rev1_0.md>) | 12 | `chandalar_rev1_0.pdf-revHEAD.svn000.tmp.pdf` |
| [QTPLUS_R8](<SparkFun_QuickLogic_ThingPlus_EOS-S3_R8_Schematic.md>) | 6 | `SparkFun_QuickLogic_ThingPlus_EOS-S3_R8_Schematic.pdf` |
| [C:UserslvaleDocumentsTinyFPGA
eposTinyFPGA-A-ProgrammeroardTinyFPGA-A-Programmer.pdf](<TinyFPGA-A-Programmer.md>) | 1 | `QuickThingPlus/TinyFPGA-Programmer-Application/a-series-programmer/board/TinyFPGA-A-Programmer.pdf` |
| [C:UserslvaleDocumentsTinyFPGA
eposTinyFPGA-B-SeriesoardTinyFPGA-B.pdf](<TinyFPGA-B.md>) | 1 | `QuickThingPlus/TinyFPGA-Programmer-Application/b-series/board/TinyFPGA-B.pdf` |
| [Microsoft Word - Microchip Customer Reseller Rights Request Form for WHQL Driver_030913.doc](<USB_-_Obtaining_a_WHQL_Certified_USB_Driver_Package.md>) | 2 | `QuickThingPlus/TinyFPGA-Programmer-Application/a-series-programmer/firmware/mcc_generated_files/usb/utilities/USB - Obtaining a WHQL Certified USB Driver Package.pdf` |

## Board Reference (`boards/`)

Curated board notes added 2026-10-11 from the QORC SDK, the schematics, the datasheet pinout table and the vendor guides.

| Document | Topic |
|---|---|
| [QuickFeather — board reference](<boards/QuickFeather.md>) | QFN (`PU64`) board: parts, pins in use, boot/programming workflow, 2 MB flash map, M4 memory regions, BSP and example apps |
| [SparkFun QuickThing Plus — board reference](<boards/QuickThing_Plus.md>) | BGA (`PD64`) board: parts, J6/J7/J8/J9 header tables, boot-strap shunts, factory restore, differences from QuickFeather, source conflicts |
| [EOS S3 IO to package pin map](<boards/EOS_S3_IO_Package_Map.md>) | All 46 IOs: WLCSP ball, BGA ball, QFN pin, plus QuickFeather and QuickThing Plus usage; LED/button/UART PCF equivalences |

## SDK & Tools

| Document | Pages | Source |
|---|---:|---|
| [CMSIS Meeting EW 2019](<CMSIS_EW2019.md>) | 51 | `qorc-sdk/Libraries/CMSIS_5/CMSIS_EW2019.pdf` |
| [Esp32_Flashing](<Esp32_Flashing.md>) | 3 | `qorc-sdk/qf_vr_apps/qf_vr_aec_app/ESP32_Wifi/Esp32_Flashing.pdf` |

## FPGA Design Flow

| Document | Topic |
|---|---|
| [QuickLogic EOS S3 — eFPGA Design Flow](<EOS_S3_FPGA_Design_Flow.md>) | Fabric resources, toolchains (ql_symbiflow, F4PGA, Aurora, MatrixIDE, SpDE), install, design entry & hard macros, PCF/SDC/QDC, flow stages & outputs, simulation, loading (header / flash .bin / J-Link / OpenOCD), SDK build integration, checklist |

## FPGA Wishbone Interface (`wishbone/`)

EOS S3 eFPGA AHB-to-Wishbone bridge reference, from the eos-s3-wishbone-mcp project (added 2026-10-09). Server source code: `source_code_knowledge/eos-s3-wishbone-mcp/`.

| Document | Topic |
|---|---|
| [EOS S3 eFPGA Wishbone Interface — Reference Notes](<wishbone/EOS_S3_Wishbone_Reference_Notes.md>) | Memory map, bus protocol & timing, byte strobes, clocks/resets, adc_ad7476_if walkthrough, firmware side, design checklist, TRM cross-check and gaps |
| [EOS S3 Wishbone — Registers, Signals and Clock Limits](<wishbone/EOS_S3_Wishbone_Registers_Signals_Clocks.md>) | 28 registers (CRU, PMU, CFG_CTL, interrupts, ADC IP), 26 `qlal4s3b_cell_macro` ports, clock limits, example RTL index |
| [eos-s3-wishbone-mcp — MCP server README](<wishbone/EOS_S3_Wishbone_MCP_Server.md>) | Install, `.mcp.json`, tool list, caveats |

## eFPGA Designs (`designs/`)

| Document | Topic |
|---|---|
| [S3_FPGA_2xUART_GPIO](<designs/S3_FPGA_2xUART_GPIO.md>) | 2× UART 16550 + GPIO on Wishbone for QuickFeather: memory map, interrupts, pins, build, issues found. Source: `source_code_knowledge/designs/S3_FPGA_2xUART_GPIO/` |
| [qorc-onion-apps](<designs/qorc-onion-apps.md>) | 17 EOS S3 apps from github.com/coolbreeze413/qorc-onion-apps: Wishbone GPIO/PWM/breathe/timer controllers (with FPGA→M4 interrupt), composite design, bootloaders, templates, FPGA reload. Overview + memory map; full source and READMEs in `source_code_knowledge/designs/qorc-onion-apps/` |

## Notes & Discussion Logs

Engineering notes and session logs (Markdown originals, added 2026-10-09).

| Document | Topic |
|---|---|
| [QORC SDK — Getting Started on QuickFeather](<QORC_SDK_Getting_Started_QuickFeather.md>) | SDK setup, Lessons 1a–3 (helloworldsw/hw, advancedfpga), flashing with qfprog, creating an app |
| [EOS S3 Pin Planner — Discussion & Change Log](<EOS_S3_Pin_Planner_Discussion_Log.md>) | QuickFeather pin map, `.pcf` / `pincfg_table.c` generator |
| [EOS S3 – Timing Constraint & Report Files](<EOS_S3_VPR_Timing_Constraint_and_Report_Notes.md>) | `.qdc` / `.sdc` constraints, VPR timing reports |
| [EOS S3 — Open-Toolchain Flow, Verified Notes & MCP Automation](<EOS_S3_Open_Toolchain_Flow_and_MCP_Notes.md>) | First-hand notes from building an IP + QuickFeather board flow on SymbiFlow v1.3.1: two-Yosys rule, install pins and the libtbb fix, `synth_quicklogic -family pp3` options and gotchas, the three `qlal4s3b_cell_macro` clock port names, `ql_symbiflow` usage, VPR/tatum log formats, `.pcf`/`.sdc` rules, the `.bin` container and pad registers, QuickFeather programming (incl. Windows COM from WSL), measured resource figures, and rules for driving the flow from an MCP server. Entries tagged VERIFIED / SOURCE / DOCS |

## Skipped duplicates (byte-identical to a converted file)

- `QL S3 ASSP EVK Power Measurement AN 132 .pdf` → [QL_S3_ASSP_EVK_Power_Measurement_AN_132_1.md](<QL_S3_ASSP_EVK_Power_Measurement_AN_132_1.md>)
- `Boards/chandalar_rev1_0.pdf-revHEAD.svn000.tmp.pdf` → [chandalar_rev1_0.md](<chandalar_rev1_0.md>)
- `qorc-sdk-master/qorc-sdk-master/Libraries/CMSIS_5/CMSIS_EW2019.pdf` → [CMSIS_EW2019.md](<CMSIS_EW2019.md>)
- `qorc-sdk/qf_vr_apps/qf_vr_raw_wifi_app/ESP32_Wifi/Esp32_Flashing.pdf` → [Esp32_Flashing.md](<Esp32_Flashing.md>)
- `qorc-sdk-master/qorc-sdk-master/qf_vr_apps/qf_vr_aec_app/ESP32_Wifi/Esp32_Flashing.pdf` → [Esp32_Flashing.md](<Esp32_Flashing.md>)
- `qorc-sdk-master/qorc-sdk-master/qf_vr_apps/qf_vr_raw_wifi_app/ESP32_Wifi/Esp32_Flashing.pdf` → [Esp32_Flashing.md](<Esp32_Flashing.md>)
