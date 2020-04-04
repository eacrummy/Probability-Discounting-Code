# -*- coding: utf-8 -*-
"""
Probability Discounting Data Extraction
Created on Fri Apr  3 10:04:39 2020

@author: eacru
"""

#%%
import pandas as pd
import numpy
import datetime
import os
import csv
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
   if len(listline) == 12 and listline[0] != 'Block':
       return True
   else: 
       return False
#%%

dataset = pd.DataFrame(columns=d);
dataset.columns = d
i=0
for subdir, dirs, files in os.walk(rootdir):
    
    for file in files:
        if "DataByBlock" in file:
            subjectID = GetSubjectName(file)
            if "Abox" in subdir:
                date=GetDateAboxes(subdir)
            else:
                date = GetDate(subdir)
            datafile = open(f'{subdir}/{files[1]}') 
            data= csv.reader(datafile, delimiter = '\t')             
            for row in data:
                print(row) 
               # if FilterRows(row) == True:
                  #  dataset.loc[i] = [subjectID, date, row[0], row[1], row[2],row[3],row[4]]
                  #i=i+1
#dataset.to_csv(f'{rootdir}/{experiment}_compiled.csv')
#%%
#index through multiple files in a directory
import os
import csv

def CompileProbabilityExperimentData(rootdir, experiment):
    d = ['SubjectID', 'Date','Block' , 'Risky Lever', 'Right Choices', 'Left Choices', 'Initial HE Latency', 'Pellet Retrieval Latency (rt)', 'Pellet Retrieval Latency (lt)', 'rt Choice Latency', 'lt Choice Latency', 'rt Forced Latency', 'lt Forced Latency']
    dataset = pd.DataFrame(columns=d);
    dataset.columns = d
    i=0
    for subdir, dirs, files in os.walk(rootdir):
    
        for file in files:
            if "DataByBlock" in file:
                subjectID = GetSubjectName(file)
                if "Abox" in subdir:
                    date=GetDateAboxes(subdir)
                else:
                    date = GetDate(subdir)
                datafile = open(f'{subdir}/{files[1]}') 
                data= csv.reader(datafile, delimiter = '\t')             
                for row in data:
                   print(FilterRows(row))
                   if FilterRows(row) == True:
                        dataset.loc[i] = [subjectID, date, row[0], row[1], row[2],row[3],row[4], row[5], row[6], row[7], row[8], row[9], row[10]]
                        i=i+1
    dataset.to_csv(f'{rootdir}/{experiment}_compiled.csv')
                        
                          #           for line in datafile:               
                    #if datalist != '\n':
                     #   datalist = line.split('\t')
                      #  print(datalist)
#%%
rootdir = 'C:/Users/eacru/OneDrive/Documents/Ferguson lab data/Probability discounting/OFCITPT_dual_prob'
CompileProbabilityExperimentData(rootdir,'OFC ITPT_dual_prob')


