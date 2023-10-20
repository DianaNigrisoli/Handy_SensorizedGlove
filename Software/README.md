# Software
This folder contains all the elements related to the programming of Handy game and the machine learning part. 

Now it is necessary to install all the dependencies listed in _requirements.txt_. To do so: 
* In the command prompt execute:
    ```console
    pip install -r requirements.txt 
    ```

## Contents 
In **Software** folder:
| File | Description |
| ---- | ----------- |
| 01_Graphics | QtDesigner related folder |
| 02_Recordings | Data we recorded for ML training phase |
| 03_Recordings_game | Data recorded during game |
| all files .py | Code for GUI programming, described more in detail below |
| MachineLearning_analysis.ipynb | Code for data analysis and model training | 
| README.md | This readme file |

## Python Code 
| File | Description |
| ---- | ----------- |
| globals.py | All the global variables |
| main_GUI_GAME.py | Code for log-in window |
| Menu_Window_noCOM.py | Code for Menu window (the user can choose between Game and Statistics) |
| Game_Window.py | Code for all the game dynamics |
| Calibration_Window.py | Window for calibrating the Handy glove |
| Statistics_Window.py | Code for showing the game statistics |
| ML_manager.py | Class with all the functions for ML classification |
| Sorting_data.py | Code for organizing all the recordings into a single file used in the ML part (not part of the game) |
| main_GUI_RECORDINGS.py | Window for making the recordings used in the ML training (not part of the game) |

## Tools 
The GUI was programmed using Python in Visual Studio Code. 
The aesthetics were defined using QtDesigner. 
The machine learning part was first implemented with Google Colab. 


