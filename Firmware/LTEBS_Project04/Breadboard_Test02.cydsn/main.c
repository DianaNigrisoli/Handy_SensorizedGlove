
#include "project.h"
#include "stdio.h"
#include "InterruptRoutines.h"
#include "ErrorCodes.h"
#include "I2C_Interface.h"

int main(void)
{
    // Enable global interrupts
    CyGlobalIntEnable; 

    //Start the ADC and UART
    ADC_Start(); 
    UART_Start();    
    
    //Interrupt initialization
    isr_Timer_StartEx(Custom_ISR_Timer);
    isr_RX_StartEx(Custom_ISR_RX);

    // Disconnect all MUX channels and start MUX
    AMux_Start();
    
    // Start the ADC conversion
    ADC_StartConvert();
   
    // Initialize I2C
    I2C_Peripheral_Start();
    
    
    // Set accelerometer registers CTRL4 and CTRL1
    I2C_Peripheral_WriteRegister(ACC_ADDRESS, ACC_CTRL4, 0x80);
    I2C_Peripheral_WriteRegister(ACC_ADDRESS, ACC_CTRL1, 0x37);
    Pin_LED_ONBOARD_Write(1);
    Pin_BatteryStatus_LED_Write(1);
    
    
    // Initialize send flag
    PacketReadyFlag = 0;
    
    for(;;)
    {
        // Check for raised flag
        if(PacketReadyFlag==1){
                            
           // Send data to terminal
           UART_PutString(DataBuffer);
           UART_PutString("\r\n");
           
           // Lower the flag
           PacketReadyFlag = 0;
       }
    }
}

/* [] END OF FILE */
