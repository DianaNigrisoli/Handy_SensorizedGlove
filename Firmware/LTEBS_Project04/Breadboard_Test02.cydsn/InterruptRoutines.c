
#include "InterruptRoutines.h"
#include "project.h"
int i = 0;

uint8 ch_received; 
int num_count = 0; /* number of received numbers */

// Sensor outputs
int32 data_res[MUX_INPUTS];
int16 data_acc[ACC_REGISTERS];

uint8 data_acc_H;   // Accelerometer MSB
uint8 data_acc_L;   // Accelerometrr LSB

// Sum of received samples
int32 sum_res[MUX_INPUTS] = {0, 0, 0, 0, 0, 0, 0};
int32 sum_acc[ACC_REGISTERS] = {0, 0, 0};

// Mean of received samples
float mean_res[MUX_INPUTS] ={0, 0, 0, 0, 0, 0, 0};;
float mean_acc[ACC_REGISTERS] = {0, 0, 0};


// Timer interrupt, called at 10 Hz frequency
CY_ISR(Custom_ISR_Timer)
{
// Read Timer status register 
Timer_ReadStatusRegister();


// Scanning MUX inputs (analog sensors)
for(i=0; i<MUX_INPUTS; i++)
{
    
    // Select channel i and read the corresponding value
    AMux_Select(i);
    data_res[i] = ADC_Read32();
    
    // Control the value read by the ADC and correct it
    if (data_res[i] < MIN_ADC_VALUE)
    {
        data_res[i] = MIN_ADC_VALUE;
    }
    else if (data_res[i] > MAX_ADC_VALUE)
    {
        data_res[i] = MAX_ADC_VALUE;
    }
    
    // Compute the incremental sum
    sum_res[i]+=data_res[i];

}

    // Scan the accelerometer registers
    for(i=0; i<ACC_REGISTERS; i++)
    {
        // Read accelerometer data and check for errors
        if ((I2C_Peripheral_ReadRegister(ACC_ADDRESS, OUTPUT_ADDRESS+(i*2), &data_acc_L) == NO_ERROR) &&
            (I2C_Peripheral_ReadRegister(ACC_ADDRESS, OUTPUT_ADDRESS+1+(i*2), &data_acc_H) == NO_ERROR))
        {
            // Save correct data
            data_acc[i] = (int16)(data_acc_L | (data_acc_H<<8));
            
        }
        else
        {
            
            // Save placeholder value
            data_acc[i] = I2C_ERROR_PLACEHOLDER;
            
        }
        
        // Compute the incremental sum
        sum_acc[i] += data_acc[i];
        
    }    


    // Increase counter variable
    num_count++;

    // After 10 samples
    if(num_count == N_SAMPLES)
    {
        // Stop the timer
        Timer_Stop();
        
        // Compute each channel mean and initialize the corresponding incremental sum
        for(i=0; i<MUX_INPUTS; i++)
        {
            
            mean_res[i] = sum_res[i]/N_SAMPLES;
            sum_res[i] = 0;
            
        }
        
        // Compute each axis mean and initialize the corresponding incremental sum
        for(i=0; i<ACC_REGISTERS; i++)
        {
            
            mean_acc[i] = sum_acc[i]/N_SAMPLES;
            sum_acc[i] = 0;
            
        }
        
        
        
        // Initialize counter variable, write string and raise flag to send string through UART
        num_count = 0;
        
        // Create a string with all the computed means
        sprintf(DataBuffer, "%.0f, %.0f, %.0f, %.0f, %.0f, %.0f, %.0f, %.0f, %.0f, %.0f",
                mean_res[0], mean_res[1], mean_res[2], mean_res[3], mean_res[4], mean_res[5], mean_res[6],
                mean_acc[0], mean_acc[1], mean_acc[2]);
        
        // Raise flag to send thr string through UART
        PacketReadyFlag = 1;
        
    }

}

// UART-receive interrupt
CY_ISR(Custom_ISR_RX){
    
    // Non-blocking call to get the latest data received
    ch_received = UART_GetChar();
    
    // Set flag based on received character
    if(ch_received == 's'){
        
        // Start the timer pnly if the received character is 's'
        Timer_Start();
            
    }
    
}

CY_ISR(Custom_ISR_Timer_Battery)
{
    
    
    
}

/* [] END OF FILE */
