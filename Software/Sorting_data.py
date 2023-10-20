import os
import pandas as pd

# Set the path to the folder containing the CSV files
folder_path = "C:\\Users\\diana\\Desktop\\02_Recordings" #DA CAMBIARE SE USATO SU ALTRI PC

# Get the list of CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

# Create an empty list to store the dataframes
# Define the column names
col = ['ID','mignolo', 'anulare', 'medio', 'indice', 'pollice', 'pres_medio', 'pres_pollice', 'x', 'y', 'z', 'target']

#Define the target values
target_list= ['open','closed', 'dummy', 'A', 'B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
target_values = pd.Series(target_list)

# Create an empty DataFrame with the specified columns
dataframes = pd.DataFrame([])

# Iterate over each CSV file
for file in csv_files:
    # Read the CSV file into a dataframe
    file_path = os.path.join(folder_path, file)
    
    df=pd.read_csv(file_path, delimiter=",", header=None)
    
    # Extract the folder name
    file_name = os.path.splitext(file)[0]
    
    # Add new colums with target and id 
    df.insert(loc=0, column='ID', value=file_name)
    df.insert(loc=11, column='target', value=target_values)
    
    # Append the dataframe to the list
    dataframes=pd.concat([dataframes, df],ignore_index=True)
   

dataframes=dataframes.set_axis(col, axis='columns')

# Save the merged dataframe to a new CSV file
dataframes.to_csv("C:\\Users\\diana\\Desktop\\02_Recordings\\00_merged_data.csv", index=False)

print('ok')