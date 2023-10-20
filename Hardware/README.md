# Hardware

## Contents 
In "Project_04" folder: 

| File | Description |
|------|-------------|
| `Project_04_Schematic.sch` | Schematic |
| `Project_04_Board.brd` | Board |
| `Project_04_ToPrint.pdf` | PCB Design PDF file 1:1 scaled |
| `sparkfun.dru` | Design rules | 
| `README.md` | This README file. |

## Tools 

Both Schematic and Board Design were implemented using the 9.6.2 version of EAGLE software. 

## Detailed files description 
### Schematic 
#### List of schematic components 
| Name | Description | On PCB |
| --------- | ----------- | ------ |
| J1 | Plated through-hole 7 pin connector | Generic 0.1 inch spaced male headers connected to flex sensors and force-sensing resistors |
| J2 | Plated through-hole 7 pin connector | Generic 0.1 inch spaced male headers connected to 3.3V supply voltage | 
| J3.1 - PSOC | Plated through-hole 7 pin connector | Generic 0.1 inch spaced female headers connected to PSOC pins from 0.0 to 0.7 |
| J3.2 - PSOC | Plated through-hole 2 pin connector | Generic 0.1 inch spaced female headers connected to PSOC pins 12.0 (SCL) and 12.1 (SDA) |
| J3.3 - PSOC | Plated through-hole 4 pin connector | Generic 0.1 inch spaced female headers connected to PSOC pins 12.6 (RX), 12.7 (TX), 2.7 and 2.6 |
| J3.4 - PSOC | Plated through-hole 2 pin connector | Generic 0.1 inch spaced female headers connected to PSOC pins VDDIO and GND |
| J3 - LED | Plated through-hole 2 pin connector | Generic 0.1 inch spaced male headers connected to yellow LED |
| J4 - BATTERY | Plated through-hole 2 pin connector | Generic 0.1 inch spaced female headers connected to 4.5V external battery and external switch |
| J5 - BT | Plated through-hole 6 pin connector | Generic 0.1 inch spaced male headers connected to HC-05 Bluetooth module |
| J6 - ACC | Plated through-hole 6 pin connector | Generic 0.1 inch spaced male headers connected to LIS3DH Accelerometer |
| J7 - LDO | Plated through-hole 3 pin connector | Generic 0.1 inch spaced male headers connected to 3.3V voltage regulator |

### Board Design
55.88mm x 73.66 mm single layer board design according to the design rules in the sparkfun.dru file. 


