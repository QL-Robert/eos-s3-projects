---
title: "QuickLogic Application Note 140 - QuickLogic\u00ae S3 I2S Master/Slave Framework"
source_file: "QL Application Note 140 \u2013 S3 OPEN I2S MasterSlave Framework.pdf"
pages: 12
sha256: c0972bfa79fc0b7f04e38e8fb879c7c2c3e3877f0d72d4f7f788a46bdf95f7cf
---

# QuickLogic Application Note 140 - QuickLogic® S3 I2S Master/Slave Framework

# **QuickLogic**<sup>**®**</sup> **S3 I**<sup>**2**</sup> **S Master/Slave Framework** 

**• • • • • • QuickLogic Application Note 140** 

## **Introduction** 

The QuickLogic S3 supports the I<sup>2</sup> S Master in Rx mode and I<sup>2</sup> S Slave in Tx mode. The I<sup>2</sup> S Master in Rx and I<sup>2</sup> S Slave in Tx is integrated into the QuickLogic I<sup>2</sup> S Framework for ease of use. Also, for efficient use of the memory by using the ping-pong buffer mechanism during Tx/Rx. This document explains the I<sup>2</sup> S application programming interfaces (APIs) for the Master and Slave using the QuickLogic I<sup>2</sup> S Framework and the integration details. 

## **I**<sup>**2**</sup> **S Master and Slave on S3** 

### **I**<sup>**2**</sup> **S Master Interface** 

The I<sup>2</sup> S Master is connected to the microphone on S3, but can be connected to other sources and the I<sup>2</sup> S Framework has the I<sup>2</sup> S Master driver code integrated into it. It is capable of receiving audio data in 16 kHz and 32 kHz sampling rates. 

- CLKOUT => Clock from S3 to MIC or any other external source. 

- WORD SELECT => Left/right word select from S3. 

- DATA IN => Data In to S3 from MIC or any other external source. 

- **Figure 1** illustrates the I<sup>2</sup> S Master interface. 

Figure 1: I<sup>2</sup> S Master Interface 



<!-- Start of picture text -->
é 12S Master in Rx mode ‘<br>i DATA IN (<br>i Microphone $3 :<br>i WORD SELECT i<br><!-- End of picture text -->

<u>www.quicklogic.com</u> **1** ••• ••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 I_**<sup>**_2_**</sup> **_S Master/Slave Framework –  Rev. 1.0_** 

### **I**<sup>**2**</sup> **S Slave Interface** 

The I<sup>2</sup> S Slave can be connected to an external I<sup>2</sup> S Master and can be used for streaming audio data over I<sup>2</sup> S. The QuickLogic Framework I<sup>2</sup> S APIs have the I<sup>2</sup> S Slave Tx driver code integrated into it. 

- SCLKIN => Clock in to S3. 

- WORD SELECT => Left/right word select to S3. 

- DATA OUT => Data out from S3 

**Figure 2** illustrates the I<sup>2</sup> S Slave interface. 

Figure 2: I<sup>2</sup> S Slave Interface 



<!-- Start of picture text -->
EE EEEEEES"128 Slave inTxmode<br>i AP $3 i<br><!-- End of picture text -->

**2** <u>www.quicklogic.com</u> •• •••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 I_**<sup>**_2_**</sup> **_S Master/Slave Framework –  Rev. 1.0_** 

## **QuickLogic I**<sup>**2**</sup> **S Framework State Flow** 

**Figure 3** shows the sequence of calls and the state change with each call. For more information about the usage of APIs see **I**<sup>**2**</sup> **S Framework APIs** on page 9. 

Figure 3: QuickLogic I<sup>2</sup> S Framework State Flow 



<!-- Start of picture text -->
HAL_DS Init pene<br>1 nnny<br>I 1<br>— | | DATA Tx/Rx goes on until there is H<br>| DS_STATE INITIALIZED | | | HAL 12S Stop call !<br>ph----------------------------1 1<br>i | Ds _STATE START | !<br>HAL 12S TX RX Start 5i a Te | 1H<br>H i<br>1 1<br>! 1<br>{<br>1H<br>t DATA Tx/Rx t'<br>=| 1if<br>| IS_STATE_STOP |} !<br>, RES | | 1<br>iLanennnn nnn nnnn anennnn ane nnnn anne<br>| 12S_STATE_UNINITIALIZED |<br><!-- End of picture text -->

<u>www.quicklogic.com</u> **3** • • • ••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 I_**<sup>**_2_**</sup> **_S Master/Slave Framework –  Rev. 1.0_** 

## **QuickLogic I**<sup>**2**</sup> **S Configurations** 

This section describes the I<sup>2</sup> S Master/Slave configuration enabling and pin configurations. 

### **I**<sup>**2**</sup> **S Master/Slave Configurations** 

The configurations shown in **Table 1** enable the I<sup>2</sup> S Master/Slave. 

Table 1: I<sup>2</sup> S Master/Slave Configurations 

|**Parameter**|**Description**|
|---|---|
|ENABLE_I2S_MASTER_ASSP_RX|Enables the I<sup>2</sup>S Master in Rx mode.|
|ENABLE_I2S_SLAVE_ASSP_TX|Enables the I<sup>2</sup>S Slave in Tx mode.|



Define the I<sup>2</sup> S features to be used in the Fw_global_config.h file based on the I<sup>2</sup> S Master in Rx/ I<sup>2</sup> S Slave in Tx as required. 

#define ENABLE_I2S_MASTER_ASSP_RX #define ENABLE_I2S_SLAVE_ASSP_TX 

### **I**<sup>**2**</sup> **S Master Rx Pad Configurations** 

The following is a snippet of the I<sup>2</sup> S Master interface PAD configuration. The following PAD configurations are for an S3 reference design board (RDB) and are ported accordingly for new boards. 

Source Directory: HAL\Src\ eoss3_hal_i2s_master_assp.c 

Function: void HAL_I2S_Master_Assp_Configure_Pins (void) 

#### **I**<sup>**2**</sup> **S DATA IN Configuration** 

/* PAD28 - I2S_DIN Mux Pin Settings */ xPadConf.ucPin = PAD_28; xPadConf.ucFunc = PAD28_FUNC_SEL_I2S_DIN; xPadConf.ucCtrl = PAD_CTRL_SRC_A0; xPadConf.ucMode = PAD_MODE_INPUT_EN; xPadConf.ucPull = PAD_PULLUP; xPadConf.ucDrv = PAD_DRV_STRENGHT_4MA; xPadConf.ucSpeed = PAD_SLEW_RATE_SLOW; xPadConf.ucSmtTrg = PAD_SMT_TRIG_DIS; HAL_PAD_Config(&xPadConf); 

**4** <u>www.quicklogic.com</u> •• •••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 I_**<sup>**_2_**</sup> **_S Master/Slave Framework –  Rev. 1.0_** 

#### **I**<sup>**2**</sup> **S Clock OUT Configuration** 

/* PAD29 - I2S_CKO Mux Pin Settings */ xPadConf.ucPin = PAD_29; xPadConf.ucFunc = PAD29_FUNC_SEL_I2S_CKO; xPadConf.ucCtrl = PAD_CTRL_SRC_A0; xPadConf.ucMode = PAD_MODE_OUTPUT_EN; xPadConf.ucPull = PAD_PULLUP; xPadConf.ucDrv = PAD_DRV_STRENGHT_4MA; xPadConf.ucSpeed = PAD_SLEW_RATE_SLOW; xPadConf.ucSmtTrg = PAD_SMT_TRIG_DIS; HAL_PAD_Config(&xPadConf); 

#### **I**<sup>**2**</sup> **S Word Select Configuration** 

/* PAD30 - I2S_WD_CKO Mux Pin Settings */ xPadConf.ucPin = PAD_30; xPadConf.ucFunc = PAD30_FUNC_SEL_I2S_WD_CKO; xPadConf.ucCtrl = PAD_CTRL_SRC_A0; xPadConf.ucMode = PAD_MODE_OUTPUT_EN; xPadConf.ucPull = PAD_PULLUP; xPadConf.ucDrv = PAD_DRV_STRENGHT_4MA; xPadConf.ucSpeed = PAD_SLEW_RATE_SLOW; xPadConf.ucSmtTrg = PAD_SMT_TRIG_DIS; 

<u>www.quicklogic.com</u> **5** • • • ••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 I_**<sup>**_2_**</sup> **_S Master/Slave Framework –  Rev. 1.0_** 

### **I**<sup>**2**</sup> **S Slave Tx Pad Configurations** 

The following is a snippet of the I<sup>2</sup> S Slave interface PAD configuration. The following PAD configurations are for an S3 RDB and are ported accordingly for new boards. 

Source Directory: HAL\Src\ eoss3_hal_i2s_slave_assp.c 

Function: void HAL_I2S_Slave_Assp_Pad_Config (void) 

#### **I**<sup>**2**</sup> **S DATA OUT Configuration** 

/* PAD24 I2S Mux Pin Settings */ xPadConf.ucPin = PAD_24; xPadConf.ucFunc = PAD24_FUNC_SEL_AP_I2S_DOUT; xPadConf.ucCtrl = PAD_CTRL_SRC_A0; xPadConf.ucMode = PAD_MODE_OUTPUT_EN; xPadConf.ucPull = PAD_PULLUP; xPadConf.ucDrv = PAD_DRV_STRENGHT_4MA; xPadConf.ucSpeed = PAD_SLEW_RATE_SLOW; xPadConf.ucSmtTrg = PAD_SMT_TRIG_DIS; HAL_PAD_Config(&xPadConf); 

#### **I**<sup>**2**</sup> **S Clock IN Configuration** 

/* PAD 31 I2S CLK IN Mux Pin Settings */ xPadConf.ucPin = PAD_31; xPadConf.ucFunc = PAD31_FUNC_SEL_AP_I2S_CLK_IN; xPadConf.ucCtrl = PAD_CTRL_SRC_A0; xPadConf.ucMode = PAD_MODE_INPUT_EN; xPadConf.ucPull = PAD_PULLUP; xPadConf.ucDrv = PAD_DRV_STRENGHT_4MA; xPadConf.ucSpeed = PAD_SLEW_RATE_SLOW; xPadConf.ucSmtTrg = PAD_SMT_TRIG_DIS; HAL_PAD_Config(&xPadConf); 

#### **I**<sup>**2**</sup> **S Word Select Configuration** 

/* PAD 23 WD_CLK_IN Mux Pin Settings */ xPadConf.ucPin = PAD_23; xPadConf.ucFunc = PAD23_FUNC_SEL_AP_I2S_WD_CLK_IN; xPadConf.ucCtrl = PAD_CTRL_SRC_A0; xPadConf.ucMode = PAD_MODE_INPUT_EN; xPadConf.ucPull = PAD_PULLUP; xPadConf.ucDrv = PAD_DRV_STRENGHT_4MA; xPadConf.ucSpeed = PAD_SLEW_RATE_SLOW; xPadConf.ucSmtTrg = PAD_SMT_TRIG_DIS; HAL_PAD_Config(&xPadConf); 

**6** <u>www.quicklogic.com</u> •• •••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 I_**<sup>**_2_**</sup> **_S Master/Slave Framework –  Rev. 1.0_** 

### **QuickLogic I**<sup>**2**</sup> **S Framework and Driver** 

#### **I**<sup>**2**</sup> **S Framework Source** 

**Table 2** shows the I<sup>2</sup> S Framework source file locations. 

Table 2: I<sup>2</sup> S Framework Source 

|**Filename**|**Directory**|**Description**|
|---|---|---|
|eoss3_hal_i2s.c|\HAL\Src|Framework for the I<sup>2</sup>S Master and Slave.|
|eoss3_hal_i2s.h|\HAL\Src|Header file for I<sup>2</sup>S Master and Slave framework.|



#### **I**<sup>**2**</sup> **S Driver Source** 

**Table 3** shows the I<sup>2</sup> S Master and Slave source file locations. 

Table 3: I<sup>2</sup> S Driver Source 

|**Filename**|**Directory**|**Description**|
|---|---|---|
|eoss3_hal_i2s_master_assp.c|\HAL\Src|I<sup>2</sup>S Master in Rx mode code.|
|eoss3_hal_i2s_slave_assp.c|\HAL\Src|I<sup>2</sup>S Slave in Tx mode code.|



<u>www.quicklogic.com</u> **7** • • • ••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 I_**<sup>**_2_**</sup> **_S Master/Slave Framework –  Rev. 1.0_** 

## **I**<sup>**2**</sup> **S Framework APIs** 

### **Data Structures and Macros** 

#### **I**<sup>**2**</sup> **S Return Value Definitions** 

#define HAL_I2S_RET_VAL          (0x0) #define HAL_I2S_RET_VAL_ERROR    (0x20) #define HAL_I2S_SUCCESS          (HAL_I2S_RET_VAL + 0x0) #define HAL_I2S_ERROR            (HAL_I2S_RET_VAL_ERROR + 0x1) #define HAL_I2S_TX_ERROR         (HAL_I2S_RET_VAL_ERROR + 0x2) #define HAL_I2S_RX_ERROR         (HAL_I2S_RET_VAL_ERROR + 0x3) #define HAL_I2S_TIME_OUT_ERROR   (HAL_I2S_RET_VAL_ERROR + 0x4) #define HAL_I2S_BAD_PARAMETER    (HAL_I2S_RET_VAL_ERROR + 0x5) #define HAL_I2S_INVALID_STATE    (HAL_I2S_RET_VAL_ERROR + 0x6) 

#### **I**<sup>**2**</sup> **S Stereo/Mono Selection** 

#define I2S_CHANNELS_STEREO     0x0     /* Stereo channel */ #define I2S_CHANNELS_MONO       0x1     /* Mono channel */ 

#### **I**<sup>**2**</sup> **S Mono Left/ Mono Right Selection** 

#define I2S_CHANNEL_MONO_LEFT   0x0     /* Mono Left channel */ #define I2S_CHANNEL_MONO_RIGHT  0x1     /* Mono Right channel */ 

#### **I**<sup>**2**</sup> **S Master/Slave in Use Details** 

#define I2S_MASTER_ASSP_RX      0x0 /* I2S master in use with Rx */ #define I2S_SLAVE_ASSP_TX       0x1 /* I2S slave in use with Tx */ #define I2S_MASTER_SLAVE_MAX    0x2 /* Max number of i2s   instances */ 

#### **I**<sup>**2**</sup> **S Driver Configuration Selection Structure Using the Above Parameters** 

typedef struct { uint8_t sdma_used; /* SDMA used, if not will use normal mode of Tx/Rx */ uint8_t i2s_wd_clk;     /* I2S left /right sync clock applicable for Master only (either 32 or 16)*/ uint8_t ch_sel;    /* Channel select (Stereo/Mono) */ uint8_t mono_sel;     /* Mono Left/Right Selection */ } I2S_Config_t; 

**8** <u>www.quicklogic.com</u> •• •••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 I_**<sup>**_2_**</sup> **_S Master/Slave Framework –  Rev. 1.0_** 

### **I**<sup>**2**</sup> **S Framework APIs** 

uint32_t HAL_I2S_Init (uint8_t i2s_id_sel, I2S_Config_t *p_i2s_cfg, HAL_I2S_Cb_Handler_t handler) 

##### **Description:** 

This API initializes the I<sup>2</sup> S driver. 

**Parameter:** i2s_id_sel 

The I<sup>2</sup> S ID identifies which I<sup>2</sup> S driver to operate on. 

**Parameter:** p_i2s_cfg To be filled with required settings for the I<sup>2</sup> S configuration. **Parameter:** Handler 

The I<sup>2</sup> S data handler gets called after completion of Tx/Rx. 

**Returns:** uint32_t Returns an HAL_I2S_SUCCESS in case of success. Returns HAL_I2S_ERROR in case of failure. 

typedef void (* HAL_I2S_Cb_Handler_t)(uint8_t i2s_id_sel, uint32_t const * p_data_received, uint32_t * p_data_to_send, uint16_t   buffer_size) 

##### **Description:** 

This API is called after the completion of each transaction of registering a callback handler during initialization. 

**Parameter:** i2s_id_sel 

The I<sup>2</sup> S ID identifies which I<sup>2</sup> S driver to operate on. 

**Parameter:** p_data_received Received buffer in case of Rx, otherwise NULL. **Parameter:** p_data_to_send Transferred buffer in case of Tx, otherwise NULL. 

**Parameter:** buffer_size Buffer size in Bytes. **Returns:** Void Void. 

<u>www.quicklogic.com</u> **9** • • • ••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 I_**<sup>**_2_**</sup> **_S Master/Slave Framework –  Rev. 1.0_** 

uint32_t HAL_I2S_TX_RX_Start (uint8_t i2s_id_sel, uint32_t * p_rx_buffer, uint32_t * p_tx_buffer, uint16_t   buffer_size) 

##### **Description:** 

Tx/Rx buffers are divided in to two parts enabling a ping-pong buffer mechanism; while one buffer is in use by a peripheral the other one is in use for Tx/Rx. 

This API should be called before initiating the transfer. This API enables the clock domains required, enables SDMA/DMA, enables irq, and sets the I<sup>2</sup> S Master/Slave registers. Until HAL_I2S_drv_stop is called, the transfer continues using a ping-pong buffer mechanism. 

**Parameter:** i2s_id_sel 

The I<sup>2</sup> S ID identifies which I<sup>2</sup> S driver to operate on. 

**Parameter:** p_rx_buffer Receives buffer in case of Rx, otherwise NULL. **Parameter:** p_tx_buffer Transfers buffer in case of Tx, otherwise NULL. **Parameter:** buffer_size Buffer size in Bytes. 

**Returns:** uint32_t Returns an HAL_I2S_SUCCESS in case of success. Returns HAL_I2S_ERROR in case of failure. 

uint32_t HAL_I2S_Stop (uint8_t i2s_id_sel) 

##### **Description:** 

This API should be once done with the data transfer. This API disables the I<sup>2</sup> S Master/Slave Tx/Rx. 

**Parameter:** i2s_id_sel 

The I<sup>2</sup> S ID identifies which I<sup>2</sup> S driver to operate on. 

**Returns:** uint32_t 

Returns an HAL_I2S_SUCCESS in case of success. Returns HAL_I2S_ERROR in case of failure. 

**10** <u>www.quicklogic.com</u> •• •••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 I_**<sup>**_2_**</sup> **_S Master/Slave Framework –  Rev. 1.0_** 

uint32_t HAL_I2S_Uninit (uint8_t i2s_id_sel) 

**Description:** 

This API un-initializes the I<sup>2</sup> S driver. 

**Parameter:** i2s_id_sel The I<sup>2</sup> S ID identifies which I<sup>2</sup> S driver to operate on. **Returns:** void Void. 

## **Contact Information** 

Phone: (408) 990-4000 (US) +(44) 1932-21-3160 (Europe) +(886) 26-603-8950 (Taiwan) +(86) 139-0517-5302 (China) +(81) 3-5875-0547 (Japan) +(82) 31-601-4225 (Korea) 

E-mail: <u>info@quicklogic.com</u> Sales: <u>America-sales@quicklogic.com Europe-sales@quicklogic.com Asia-sales@quicklogic.com Japan-sales@quicklogic.com Korea-sales@quicklogic.com</u> 

Support: <u>www.quicklogic.com/support</u> 

Internet: <u>www.quicklogic.com</u> 

## **Revision History** 

|**Revision**|**Date**|**Originator and Comments**|
|---|---|---|
|1.0|September 2017|Nilanjan Roychowdhury and Kathleen Bylsma<br>Initial release.|



<u>www.quicklogic.com</u> **11** • • • ••• 

© 2017 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_S3 I_**<sup>**_2_**</sup> **_S Master/Slave Framework –  Rev. 1.0_** 

## **Notice of Disclaimer** 

QuickLogic is providing this design, product or intellectual property "as is." By providing the design, product or intellectual property as one possible implementation of your desired system-level feature, application, or standard, QuickLogic makes no representation that this implementation is free from any claims of infringement and any implied warranties of merchantability or fitness for a particular purpose. 

You are responsible for obtaining any rights you may require for your system implementation. QuickLogic shall not be liable for any damages arising out of or in connection with the use of the design, product or intellectual property including liability for lost profit, business interruption, or any other damages whatsoever. QuickLogic products are not designed for use in life-support equipment or applications that would cause a life-threatening situation if any such products failed. Do not use QuickLogic products in these types of equipment or applications. 

QuickLogic does not assume any liability for errors which may appear in this document. However, QuickLogic attempts to notify customers of such errors. QuickLogic retains the right to make changes to either the documentation, specification, or product without notice. Verify with QuickLogic that you have the latest specifications before finalizing a product design. 

## **Copyright and Trademark Information** 

Copyright © 2017 QuickLogic Corporation. All Rights Reserved. 

The information contained in this document is protected by copyright. All rights are reserved by QuickLogic Corporation. QuickLogic Corporation reserves the right to modify this document without any obligation to notify any person or entity of such revision. Copying, duplicating, selling, or otherwise distributing any part of this product without the prior written consent of an authorized representative of QuickLogic is prohibited. 

QuickLogic is a registered trademark, and the QuickLogic logo is a trademark of QuickLogic. Other trademarks are the property of their respective companies. 

**12** <u>www.quicklogic.com</u> •• •••• 

© 2017 QuickLogic Corporation 

