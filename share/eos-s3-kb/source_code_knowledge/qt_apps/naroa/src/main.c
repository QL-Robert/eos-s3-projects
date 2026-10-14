/*==========================================================
 * Copyright 2021 QuickLogic Corporation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *==========================================================*/

/*==========================================================
 *
 *    File   : main.c
 *    Purpose: main for Thing Plus helloworldsw and LED/UserButton test
 *                                                          
 *=========================================================*/

#include "Fw_global_config.h"   // This defines application specific charactersitics

#include <stdio.h>
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"
#include "timers.h"
#include "RtosTask.h"

/*    Include the generic headers required for QORC */
#include "eoss3_hal_gpio.h"
#include "eoss3_hal_rtc.h"
#include "eoss3_hal_fpga_usbserial.h"
#include "ql_time.h"
#include "s3x_clock_hal.h"
#include "s3x_clock.h"
#include "s3x_pi.h"
#include "dbg_uart.h"

#include "cli.h"

#include "fpga_loader.h"    // API for loading FPGA
#include "gateware.h"           // FPGA bitstream to load into FPGA




/*
 * Global variable definition
 */

#define USER_BUTTON_GPIO_NUM (0) //PAD 6, GPIO is connected to User Button
#define BLUE_LED_GPIO_NUM (4) //PAD 18, GPIO is connected to Blue LED
#define GREEN_LED_GPIO_NUM (5) //PAD 21, GPIO is connected to Green LED
#define RED_LED_GPIO_NUM (6) //PAD 22, GPIO is connected to Red LED
#define NVIC_USER_IRQ_OFFSET          16

extern void qf_hardwareSetup();
static void nvic_init(void);
static void leds(void);
void buttontoggle(void);
extern void qf_hardwareSetup_in(void);
void buttonstate(void);
extern void SensorGpio_Handler(void) ;

int main(void)
{
    uint32_t control;
    int aux;

    qf_hardwareSetup_in();
    nvic_init();
    load_fpga(axFPGABitStream_length,axFPGABitStream);
    // Use 0x6141 as USB serial product ID (USB PID)
    HAL_usbserial_init2(false, false, 0x6141);        // Start USB serial not using interrupts
    for (int i = 0; i != 4000000; i++) ;   // Give it time to enumerate
    
	
	dbg_str( "\n\nHello world!!\n\n");	// <<<<<<<<<<<<<<<<<<<<<  Change me!

     
    /* Start the tasks and timer running. */
    //vTaskStartScheduler();

    dbg_str("\n");
    HAL_GPIO_Write(BLUE_LED_GPIO_NUM, 1);

    
    aux = NVIC_GetPendingIRQ(Gpio_IRQn);
    dbg_str("NVIC_GetPendingIRQ(Gpio_IRQn):");
    dbg_int(aux);
    dbg_str("\n");

    aux = NVIC_GetActive(Gpio_IRQn);
    dbg_str("NVIC_GetActive(Gpio_IRQn):");
    dbg_int(aux);
    dbg_str("\n");

    aux = (((NVIC->ISER[(Gpio_IRQn >> 5UL)] & (1UL << (Gpio_IRQn & 0x1FUL))) != 0UL) ? 1UL : 0UL);
    dbg_str("NVIC_GetEnableIRQn(Gpio_IRQn):");
    dbg_int(aux);
    dbg_str("\n");

    uint32_t vector = (uint32_t)SensorGpio_Handler;
    uint32_t vectors = (uint32_t )SCB->VTOR;
    (* (int *) (vectors + ((int32_t)Gpio_IRQn + NVIC_USER_IRQ_OFFSET) * 4)) = vector;

    vectors = (uint32_t )SCB->VTOR;
    control = (uint32_t)(* (int *) (vectors + ((int32_t)Gpio_IRQn + NVIC_USER_IRQ_OFFSET) * 4));

    dbg_str("NVIC_GetVector(Gpio_IRQn):");
    dbg_hex32(control);
    dbg_str("\n");
    
    control = INTR_CTRL->GPIO_INTR;
    aux = control & (1 << GPIO_2);
    dbg_str("INTR_CTRL->GPIO_INTR:");
    dbg_hex32(control);
    dbg_str("\n");
    dbg_str("INTR_CTRL->GPIO_INTR & (1<<GPIO_2):");
    dbg_int(aux);
    dbg_str("\n");

    control = INTR_CTRL->GPIO_INTR_EN_M4;
    aux = control & (1 << GPIO_2);
    dbg_str("INTR_CTRL->GPIO_INTR_EN_M4:");
    dbg_hex32(control);
    dbg_str("\n");
    dbg_str("INTR_CTRL->GPIO_INTR_EN_M4 & (1<<GPIO_2):");
    dbg_int(aux);
    dbg_str("\n");

    if ( aux != 4){
      dbg_str("Error: GPIO interrupt not enabled\n");
    }
    else{
      dbg_str("GPIO interrupt enabled\n");
    }
    
    dbg_str("INTR_CTRL->GPIO_INTR:");
    INTR_CTRL->GPIO_INTR = GPIO_2_INTR;
    dbg_hex32(INTR_CTRL->GPIO_INTR);
    dbg_str("\n");

    aux = NVIC_GetPendingIRQ(Gpio_IRQn);
    dbg_str("NVIC_GetPendingIRQ(Gpio_IRQn):");
    dbg_int(aux);
    dbg_str("\n");

    aux = NVIC_GetActive(Gpio_IRQn);
    dbg_str("NVIC_GetActive(Gpio_IRQn):");
    dbg_int(aux);
    dbg_str("\n");

    aux = (((NVIC->ISER[(Gpio_IRQn >> 5UL)] & (1UL << (Gpio_IRQn & 0x1FUL))) != 0UL) ? 1UL : 0UL);
    dbg_str("NVIC_GetEnableIRQn(Gpio_IRQn):");
    dbg_int(aux);
    dbg_str("\n");

    while(1){
      
      uint8_t ucVal_boton = 0;
      uint8_t ucVal_pad = 0;

      HAL_GPIO_Read(2, &ucVal_boton);
      HAL_GPIO_Read(BLUE_LED_GPIO_NUM, &ucVal_pad);

      dbg_str( "Botón:" );
      dbg_int( ucVal_boton );
      dbg_str( "\n" );

      dbg_str( "LED:" );
      dbg_int( ucVal_pad );
      dbg_str( "\n" );

      
      dbg_str("\n");
      dbg_str( "\n" );
      
      for (uint32_t i = 0; i < 1152001; i++) {
          dbg_str( "" ); 
      }
      
    };
}

static void nvic_init(void)
 {
    // To initialize system, this interrupt should be triggered at main.
    // So, we will set its priority just before calling vTaskStartScheduler(), not the time of enabling each irq.
    NVIC_SetPriority(Ffe0_IRQn, configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY);
    NVIC_SetPriority(SpiMs_IRQn, configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY);
    NVIC_SetPriority(CfgDma_IRQn, configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY);
    NVIC_SetPriority(Uart_IRQn, configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY);
    NVIC_SetPriority(FbMsg_IRQn, configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY);
 }    

//needed for startup_EOSS3b.s asm file
void SystemInit(void)
{

}

static void leds(void){
        /*
        dbg_str( "\n" );
        dbg_str( "##########################\n\n");
        dbg_str("Se enciende el led rojo\n");
        dbg_str( "##########################\n\n");
        dbg_str( "\n" );
        */
        for (uint32_t i = 0; i < 1152001; i++) {
          dbg_str( "" ); 
        }
        HAL_GPIO_Write(RED_LED_GPIO_NUM, 1);
        
        /*
        dbg_str( "\n" );
        dbg_str( "##########################\n\n");
        dbg_str("Se apaga el led rojo\n");
        dbg_str( "##########################\n\n");
        dbg_str( "\n" );
        */
        for (uint32_t i = 0; i < 1152001; i++) {
          dbg_str( "" ); 
        }
        HAL_GPIO_Write(RED_LED_GPIO_NUM, 0);
}

void buttontoggle(void)
{ 
    uint8_t ucVal_boton = 0;
    uint8_t ucVal_led = 0;

    HAL_GPIO_Read(2, &ucVal_boton);
    if (ucVal_boton != 1) { 
      dbg_str("paso por 1\n");
      for (uint32_t i = 0; i < 1152001; i++) {
          dbg_str( "" ); 
      }
      HAL_GPIO_Read(2, &ucVal_boton);
      if (ucVal_boton != 1) {
        dbg_str("paso por 1\n");
        HAL_GPIO_Read(BLUE_LED_GPIO_NUM, &ucVal_led); 

        if(ucVal_led){
          HAL_GPIO_Write(BLUE_LED_GPIO_NUM, 1);
        }
        else{
          HAL_GPIO_Write(BLUE_LED_GPIO_NUM, 0);
        }
            
      }

      for (int i = 0; i < 4000000; i++){
        dbg_str( "" ); 
      } 
    }
}
