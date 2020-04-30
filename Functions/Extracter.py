# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:02:20 2020
Extracter Probability Discounting Raw Data
@author: eacru
"""
import csv
import os

def Extracter(file_name):
    with open(file_name, mode='r', newline='') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"', quoting = csv.QUOTE_MINIMAL)
        data = [row for row in reader]
        #data.pop(0)
    return data

def getFilePathList(path):
    data = []
    for subdir, dirs, files in os.walk(path):

    
        for file in files:
            #if os.path.splitext(file)[-1] == '.csv':
            extracted_data = str(os.path.join(subdir,file))
            data.append(extracted_data)
    return data
          #datafile=open(os.path.join(subdir, file))
          #data = Extracter(os.path.join(subdir,file))
          #return data
          
    