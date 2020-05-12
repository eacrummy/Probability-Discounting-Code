# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 14:53:38 2020
Data frame get win stay shift behavior
@author: eacru
"""
#%%
import pandas as pd

test_enhanced = pd.read_csv("C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\IT_reversal")
dataset_name = 'OFC_IT_reversal_events'
root = "C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\"
#%% 
winlose_df = pd.DataFrame()
def getRelevantReversalStamps(dataset):
    return(test_enhanced.loc[test_enhanced.event_type_raw.isin([1.0, 2.0, 5.0, 33.0, 35.0])])# 35 is for reversal files only
  
presses_df = getRelevantReversalStamps(test_enhanced)
#%%
#Goal of taking new presses_df:
 #  1. get if press results in win or lose
def getWinLose(filtered_dataset):
     filtered_dataset.loc[filtered_dataset.event_type_raw == 5.0, 'WinLose'] = 'Win'
     filtered_dataset.loc[filtered_dataset.event_type_raw == 33.0, 'WinLose'] = 'Lose'
     return filtered_dataset

winLose_df = getWinLose(presses_df)
#%%
 # 2. get if after win or lose, they switched to a new lever or kept to same lever
def getStayShift(filtered_dataset):
     just_presses = filtered_dataset.loc[filtered_dataset.event_type_raw.isin([1.0,2.0])]
     mask_1 = (filtered_dataset.event_type_raw == 1.0) # left or right press
     mask_2 = (filtered_dataset.event_type_raw == 2.0) #left or right press
             
     just_presses['mask_1'] = mask_1
     just_presses['mask_2'] = mask_2
     filtered_dataset['StayShift'] = None
     for i in range(len(just_presses)):
         #print("index " + str(index))
         #print("row " + str(row))
         row_number = just_presses.index[i]
         
         if i == 0:
             filtered_dataset['StayShift'][row_number] = 'Start'
         elif just_presses.mask_1.iloc[i] == just_presses.mask_1.iloc[i-1]:
             filtered_dataset['StayShift'][row_number] = 'Stay'
         elif just_presses.mask_2.iloc[i] == just_presses.mask_2.iloc[i -1]:
             filtered_dataset['StayShift'][row_number] = 'Stay'
         else:
             filtered_dataset['StayShift'][row_number] = 'Shift'
             
     return filtered_dataset
         
stayShift_df = getStayShift(winLose_df)  
#%%
def combineStayShiftWinLose(filtered_dataset):
    filtered_dataset['WinLoseStayShift'] = None
    for i in range(len(filtered_dataset)):
        row_number = filtered_dataset.index[i]
        if i != len(filtered_dataset) -1:
            if filtered_dataset.StayShift.iloc[i] != None:
                if filtered_dataset.WinLose.iloc[i + 1] != 'NaN':
                    filtered_dataset['WinLoseStayShift'][row_number] = filtered_dataset.WinLose.iloc[i + 1]
    return filtered_dataset
        #pull row
        # if lever press and next one is result, put result in new column at lever press
        #ignore last row
 # 3. determine when a reversal occurred and what number reversal they are on
     #input is dataframe with event_type_raw, event_type, subject, date, box, experiment, timestamp, winlose, stayshift columns
     #output is datafame with column added that is reversal number -- will go from 0 to max # of reversals by that subject for each session
     
    #outline
    #load in dataframe
filtered_compiled = combineStayShiftWinLose(stayShift_df)
#%%
def trackReversalNumber(dataset):
    reversal_number = 0
    dataset['ReversalNumber'] = None
    for row in range(len(dataset)):
        row_number = dataset.index[row]
        if dataset.event_type_raw.iloc[row] == 35.0:
            reversal_number = reversal_number + 1
            
        else:
            reversal_number = reversal_number
            
        dataset['ReversalNumber'][row_number] = reversal_number
    
    return(dataset)
    
 #group by subject and session
    #for each subject and each session, take running count of event_type_raw = 35 and add 1 to reversal number column for each row    
reversal_count = test_enhanced.groupby(['subject','date']).apply(trackReversalNumber)

#join dataset with win-lose stay-shift columns and running reversal count into a dataframe - right join with an identifying name to later drop duplicate columns
test = reversal_count.join(filtered_compiled, rsuffix = 'filtered_duplicate')

#drop duplicate columns based on string identifier
final_df = test[test.columns.drop(list(test.filter(regex='filtered_duplicate')))]

final_df.to_csv(f'{root}/{dataset_name}_processed.csv')
            
            
        
        
   
    