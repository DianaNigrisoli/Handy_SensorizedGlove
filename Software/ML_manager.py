import os
import pandas as pd
import numpy as np
import joblib
import sklearn
import logging
from sklearn.preprocessing import MinMaxScaler

from PyQt5.QtCore import (
    QObject,
    QThreadPool,
    QRunnable,
    pyqtSignal,
    pyqtSlot,
)

#global variables
import globals 

# Logging config
logging.basicConfig(format="%(message)s", level=logging.INFO)

import joblib


############################
# MACHINE LEARNING MANAGER #
############################

class MLPredictor:

    def __init__(self, model_path, scaler_path):
        #upload the model
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model = None
        self.col = ['mignolo', 'anulare', 'medio', 'indice', 'pollice', 'pres_medio', 'pres_pollice', 'x', 'y', 'z']

        try:
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            logging.info("Model and scaler loaded successfully!")
        except Exception as e:
            logging.info("Error loading the model or scaler:", str(e))


    def standardize(self, open, closed, feature_list): 
        """!
        @brief 
        The function does two types of standardization: 
        - it standardizes the values from the analog sensors using the calibration data
        - it standardizes the values from the accelerometer using a minmax scaler fitted with the data used for trainig the model
        """
        values_to_correct = np.array(feature_list, dtype=float)
    
        #calibration of analog sensors 
        new_max=1
        new_min=-1 
        
        open = np.array(open, dtype=np.float32)
        closed = np.array(closed, dtype=np.float32)

        values_corrected_analog = np.empty(7)

        for i in range(len(open)):
           if(open[i]==closed[i]):
                values_corrected_analog[i] = (values_to_correct[i] - closed[i])*(new_max - new_min) / (1+open[i]-closed[i]) + new_min
                #the +1 in the denominator is necessary in case some sensor has the same values in open and closed position
           else: 
                values_corrected_analog[i] = (values_to_correct[i] - closed[i])*(new_max - new_min) / (open[i]-closed[i]) + new_min
        
        #standization of accelerometer
        df = pd.DataFrame([values_to_correct[7:10]], columns=['x','y','z'])
        values_corrected_digital= pd.DataFrame(self.scaler.transform(df))
    
        
        #concat analog + digital features 
        values_corrected = np.concatenate((values_corrected_analog, values_corrected_digital), axis=None)
        
        df_corrected = pd.DataFrame([values_corrected], columns = self.col, index=None)

        logging.info("Data standardized correctly")
        return df_corrected
    

    def predict_letter(self, feature_list, open, closed):
        """!
        @brief first it standardize the data and then predicts the letter
        """
        if self.model is None:
            logging.info("Model not loaded. Please load the model first using the 'load_model' method.")
            return None
        try:
            feature_array_normalized=self.standardize(open, closed, feature_list)
            prediction = self.model.predict(feature_array_normalized)
            return prediction[0] 
        
        except Exception as e:
            logging.info("Error occurred while predicting")
            return '?'


if __name__ == "__main__":
    #Example for debug: 
    model_path = 'RandomForest_model.sav'
    scaler_path = 'scaler_acc.sav'
    model=MLPredictor(model_path, scaler_path)
    open = [36959.0, 34791.0, 37827.0, 37268.0, 32686.0, 0.0, 0.0]
    closed = [36959.0, 18943.0, 25550.0, 22003.0, 27735.0, 39739.0, 57388.0]
    feature_list = [19249, 19784, 27164, 22263, 30187, 20479, 0, 1619, -1068, -15443]
    df_normalized=model.standardize(open, closed, feature_list)
    prediction=model.predict_letter(feature_list, open, closed)
    
    print(prediction)
    

