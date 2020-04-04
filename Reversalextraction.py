# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 20:16:18 2019

@author: eacru
"""
#%%
import pandas as pd
import numpy
import datetime

#%%

def GetSubjectName(file):
    subjectID = file.split('_')[0]
    return(subjectID)
#%%
def GetDate(subdir):
    date = subdir.split('\\')[1]
    date_formatted = datetime.datetime.strptime(date, '%m%d%Y').strftime('%m-%d-%Y')
    return(date_formatted)
#%% 
def GetDateAboxes(subdir):
    date = subdir.split('\\')[1]
    date_formatted = datetime.datetime.strptime(date[:8], '%m%d%Y').strftime('%m-%d-%Y')
    return(date_formatted)
#%%
    # separate by row
def FilterRows(listline):
   # return boolean
   if len(listline) == 6 and listline[0] != 'Reversal':
       return True
   else: 
       return False
#%%
#index through multiple files in a directory
import os
import csv

def CompileExperimentData(rootdir, experiment):
    d = ['SubjectID', 'Date','Reversals' , 'Pre-Reversal Active Lever', 'Pre-Reversal Active Presses', 'Pre-Reversal Inactive Presses', 'Time to Reversal (s)']
    dataset = pd.DataFrame(columns=d);
    dataset.columns = d
    i=0
    for subdir, dirs, files in os.walk(rootdir):
    
        for file in files:
            if "ReversalData" in file:
                subjectID = GetSubjectName(file)
                if "Abox" in subdir:
                    date=GetDateAboxes(subdir)
                else:
                    date = GetDate(subdir)
                datafile = open(f'{subdir}/{files[2]}') 
                data= csv.reader(datafile, delimiter = '\t')             
                for row in data:
                    if FilterRows(row) == True:
                        dataset.loc[i] = [subjectID, date, row[0], row[1], row[2],row[3],row[4]]
                        i=i+1
    dataset.to_csv(f'{rootdir}/{experiment}_compiled.csv')
                        
                          #           for line in datafile:               
                    #if datalist != '\n':
                     #   datalist = line.split('\t')
                      #  print(datalist)
#%%
rootdir = 'C:/Users/eacru/OneDrive/Documents/Ferguson lab data/Reversal/OFCITPT_dual'
CompileExperimentData(rootdir,'OFC ITPT dual')