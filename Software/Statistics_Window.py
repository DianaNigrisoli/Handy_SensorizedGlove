###########
# IMPORTS #
###########

import struct
import sys
import time
import csv 
import os
from datetime import datetime
import logging
import random

from PyQt5 import QtCore
from PyQt5.uic import loadUi

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtChart import QChart, QChartView, QLineSeries

import pyqtgraph as pg
from pyqtgraph import PlotWidget

from PyQt5.QtCore import (
    QObject,
    QThreadPool,
    QRunnable,
    pyqtSignal,
    pyqtSlot, 
    QTimer,
    Qt,
)
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QComboBox,
    QHBoxLayout,
    QGridLayout,
    QVBoxLayout,
    QWidget, QLabel, QFrame,
    QTextEdit,
    QMessageBox,
    QLineEdit,
    QDialog,  
)

import csv
import globals
import ResourceFiles

# Logging config
logging.basicConfig(format="%(message)s", level=logging.INFO)

#####################
# STATISTICS WINDOW #
#####################

class StatsWindow(QMainWindow): 
    
    
    def __init__(self):
        super().__init__()

        loadUi('01_Graphics/Statistics_Window.ui', self)

        self.Username_label.setText(globals.UserName) 

        self.TotalScore_button.clicked.connect(self.graphScoreplot)
        self.GlobalPerformance_button.clicked.connect(self.BarChartplot)
        self.exit_btn.clicked.connect(self.BackToMenu)
        self.stackedWidget.setCurrentIndex(0)
        
        brush = pg.mkBrush(color=pg.mkColor("#fff6eb"))
        self.graphScore.setBackgroundBrush(brush)
        self.label_2.setText("")
        
        #self.graphScore.setStyleSheet("background-color: rgb(255, 246, 235)");

        
# Plot Score for each game - line chart 

    def graphScoreplot(self):
       
       self.check_csv_presence()

       self.label_2.setText("Total Score Line Chart")

       name = globals.UserName
       data = []
       dates = []
       unique_dates = []
       sum = 0
       x = []
       y = []
  
       with open('03_Recordings_game/'+ name +'.csv','r') as csvfile:
          stats_data = csv.reader(csvfile, delimiter = ',')
          for row in stats_data:
            data.append(row)    

       for row in data:
          dates.append(row[13])

       # Create an array of unique dates  
       for j in dates:
          if j not in unique_dates:
             unique_dates.append(j)
             
       if len(unique_dates)==1: 
         msgBox = QMessageBox()
         msgBox.setIcon(QMessageBox.Warning)
         msgBox.setText("You have to play in different dates for plotting this chart")
         msgBox.setWindowTitle("Data error")
         msgBox.setStyleSheet("background-color: rgb(255, 221, 188)")
         msgBox.exec()

       for i in range(len(unique_dates)):
          for row in data:
            if row[13]==unique_dates[i]:
               sum += int(row[12])
          y.append(sum)
          x.append(i)
          sum = 0

       #Create a line chart
       self.stackedWidget.setCurrentIndex(0)
       brush = pg.mkBrush(color=pg.mkColor("#fff6eb"))
       self.graphScore.setBackgroundBrush(brush)     
       self.graphScore.plot(x, y, pen=pg.mkPen({'color':"#000000", 'width': 3}))

       # Set labels for the x-axis and the y-axis
       labelStyle = {'fontname':'Montserrat SemiBold', 'font-size': '10pt', 'color':'#000000'}

       axis1 = self.graphScore.getAxis('left')
       axis1.setPen(color=pg.mkColor("#000000"))
       axis1.setTextPen(color=pg.mkColor("#000000"))
       axis1.setLabel("Score", **labelStyle)

       axis2 = self.graphScore.getAxis('bottom')
       axis2.setPen(color=pg.mkColor("#000000"))
       axis2.setTextPen(color=pg.mkColor("#000000"))
       axis2.setLabel("Round", **labelStyle)  # Syn round -> Match o game

# Plot Global Performance data - bar chart 

    def BarChartplot(self):
       self.check_csv_presence()

       name = globals.UserName
       data = []
       tot_categories = {
          "A": 0,
          "B": 0,
          "C": 0,
          "D": 0,
          "E": 0,
          "F": 0,
          "G": 0,
          "H": 0,
          "I": 0,
          "J": 0,
          "K": 0,
          "L": 0,
          "M": 0,
          "N": 0,
          "O": 0,
          "P": 0,
          "Q": 0,
          "R": 0,
          "S": 0,
          "T": 0,
          "U": 0,
          "V": 0,
          "W": 0,
          "X": 0,
          "Y": 0,
          "Z": 0,
       }
       correct_categories = {
          "A": 0,
          "B": 0,
          "C": 0,
          "D": 0,
          "E": 0,
          "F": 0,
          "G": 0,
          "H": 0,
          "I": 0,
          "J": 0,
          "K": 0,
          "L": 0,
          "M": 0,
          "N": 0,
          "O": 0,
          "P": 0,
          "Q": 0,
          "R": 0,
          "S": 0,
          "T": 0,
          "U": 0,
          "V": 0,
          "W": 0,
          "X": 0,
          "Y": 0,
          "Z": 0,
       }
       x = []
       y1 = []
       y2 = []
       y = []
  
       with open('03_Recordings_game/'+ name +'.csv','r') as csvfile:
          stats_data = csv.reader(csvfile, delimiter = ',')
          for row in stats_data:
            data.append(row)    
             
       for row in data:
          tot_categories[row[11]] += 1
          if row[12]=='1':
             correct_categories[row[11]] += 1
   
       print(correct_categories)
       print(tot_categories)
       x = list(correct_categories.keys())
       y1 = list(correct_categories.values())
       y2 = list(tot_categories.values())

       print(enumerate(y1))

       for index, value in enumerate(y1):
          if y2[index] == 0:
             y.append(0)
          else:
             y.append(value/y2[index])     # (N° times the letter was performed well)/(N° times the letter was randomly chosen)
       
       y = [item * 100 for item in y]    #TODO: trovare un modo per fissare gli assi 

       #Create a bar plot
       self.stackedWidget.setCurrentIndex(1)
       bar_plot = pg.BarGraphItem(x=range(len(x)), height=y, width = 0.5, brush=pg.mkBrush(color=pg.mkColor("#a61e22")))
       brush = pg.mkBrush(color=pg.mkColor("#fff6eb"))
       self.graphBarChart.setBackgroundBrush(brush)
       self.graphBarChart.addItem(bar_plot)

       # Set the labels for the x-axis
       labelStyle = {'font-size': '10pt', 'color':'#000000'}

       axis1 = pg.AxisItem(orientation='bottom')
       axis1.setPen(color=pg.mkColor("#000000"))
       axis1.setTextPen(color=pg.mkColor("#000000"))
       axis1.setTicks([list(enumerate(x))])
       axis1.setLabel(**labelStyle)

       axis2 = pg.AxisItem(orientation='left')
       axis2.setPen(color=pg.mkColor("#000000"))
       axis2.setTextPen(color=pg.mkColor("#000000"))
       axis2.setLabel(**labelStyle)

       self.graphBarChart.getPlotItem().setAxisItems({'bottom': axis1})
       self.graphBarChart.getPlotItem().setAxisItems({'left': axis2})
       self.graphBarChart.getPlotItem().setLabels(bottom='Letters', left='Percentage of correct answers')


    def check_csv_presence(self): 
        folder_path='03_Recordings_game'
        count=0
        for filename in os.listdir(folder_path):
            if filename == globals.UserName + '.csv':
              count += 1
        
        if count == 0: 
            QMessageBox.warning(self, 'You have never playes', 'There are no statistics available')
            #TODO: fare message box più carino 
            return

    def BackToMenu(self):
       self.close()   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StatsWindow()
    window.show()
    sys.exit(app.exec_())