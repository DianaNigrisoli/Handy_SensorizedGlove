/* ========================================
 *
 * Copyright YOUR COMPANY, THE YEAR
 * All Rights Reserved
 * UNPUBLISHED, LICENSED SOFTWARE.
 *
 * CONFIDENTIAL AND PROPRIETARY INFORMATION
 * WHICH IS THE PROPERTY OF your company.
 *
 * ========================================
*/
#ifndef __INTERRUPT_ROUTINES_H
  #define __INTERRUPT_ROUTINES_H
  
    #include "cytypes.h"
    #include "stdio.h"
    #include "I2C_Interface.h"
    
    #define TRANSMIT_BUFFER_SIZE 132    // Max dimension of the buffer to be sent through UART
    #define MUX_INPUTS 7                // Number of analog sensors to be connected to the ADC through the MUX
    #define ACC_REGISTERS 3             // Number of axis to be read from the accelerometer (x, y, z)
    
    // Values to check the correct reading of the ADc output
    #define MIN_ADC_VALUE 0
    #define MAX_ADC_VALUE 65535
    
    // Useful accelerometer register addresses and the value to be written in them
    #define ACC_ADDRESS 0x18
    #define ACC_CTRL4 0x23
    #define ACC_CTRL1 0x20
    #define ACC_CTRL4_VALUE 0x80    // Enabling the BDU option
    #define ACC_CTRL1_VALUE 0x37    // Enabling all 3 axis of the accelerometer and set its frequency at 25 Hz
    #define OUTPUT_ADDRESS 0x28     // Address of the registers containing the first byte of the first axis data

    #define I2C_ERROR_PLACEHOLDER 1000000   // Value to be written in the accelerometer data variable in case of
                                            // I2C communication failure
    
    #define N_SAMPLES 10        // Number of samples used to compute the mean of a sensor output
                                // 10 samples → 1 second
    
    CY_ISR_PROTO(Custom_ISR_Timer);
    CY_ISR_PROTO(Custom_ISR_Timer_Battery);
    CY_ISR_PROTO(Custom_ISR_RX);

    char DataBuffer[TRANSMIT_BUFFER_SIZE];  // String which will be sent through the UART
    volatile uint8 PacketReadyFlag;         // Flag to be used to send the string through UART
#endif
/* [] END OF FILE */
