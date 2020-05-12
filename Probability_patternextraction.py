# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 14:53:38 2020
Data frame get win stay shift behavior
@author: eacru
"""
#%%
import pandas as pd

test_enhanced = pd.read_csv("C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\IT_discounting")
dataset_name = 'OFC_IT_probability_events'
root = "C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\"
#%% 
def getRelevantProbabilityStamps(dataset):
    return(dataset.loc[dataset.event_type_raw.isin([1.0, 2.0, 5.0, 13.0 ,14.0, 32.0,33.0])])# 14 identifier for choice trials only #13 for forced trials
  
presses_df = getRelevantProbabilityStamps(test_enhanced)
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
         print("Running row " + str(i) + " out of " + str(len(just_presses)))
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
        print("Running row " + str(i) + " out of " + str(len(filtered_dataset)))
        if i != len(filtered_dataset) -1:
            if filtered_dataset.StayShift.iloc[i] != None:
                if filtered_dataset.WinLose.iloc[i + 1] != 'NaN':
                    filtered_dataset['WinLoseStayShift'][row_number] = filtered_dataset.WinLose.iloc[i + 1]
    return filtered_dataset
        #pull row
        # if lever press and next one is result, put result in new column at lever press
        #ignore last row
    #outline
    #load in dataframe
filtered_compiled = combineStayShiftWinLose(stayShift_df)
#%%
def trackBlock(dataset):
    block = 0
    block_counter = 0
    dataset['Block'] = None
    for row in range(len(dataset)):
        row_number = dataset.index[row]
        if dataset.event_type_raw.iloc[row] == 13.0:
            block=0
            block_counter = block_counter
        if dataset.event_type_raw.iloc[row] == 14.0:
            block_counter = block_counter + 1
            if block_counter <= 10:
                block = 1
            elif block_counter <= 20:
                block = 2
            elif block_counter <= 30:
                block = 3
            elif block_counter <= 40:
                block = 4              
        else:
            block_counter = block_counter
            block = block
           
            
        dataset['Block'][row_number] = block
        print(dataset.event_type_raw.iloc[row])
        print(block_counter)
        print(block)
    
    return(dataset)
#%%
groups = presses_df.groupby(['subject','date'])['event_type_raw' ].value_counts()
print(groups)
    
#%%
 #group by subject and session
    #for each subject and each session, take running count of event_type_raw = 14 and use to identify block for session. If count reaches 10, reset and put counter to next block   
probability_blocks = presses_df.groupby(['subject','date']).apply(trackBlock)


#%%
# For all blocks != zero, get the winlose, stayshift combinations
nonZeroFilter = probability_blocks[probability_blocks.Block != 0]
#presses_filter = getRelevantProbabilityStamps(nonZeroFilter)


winlose = getWinLose(nonZeroFilter)
stayshift = getStayShift(winlose)




#combine to make it easier

compiled = combineStayShiftWinLose(stayshift)

compiled.to_csv(f'{root}/{dataset_name}_processed.csv')
#%%

#join dataset with win-lose stay-shift columns and running reversal count into a dataframe - right join with an identifying name to later drop duplicate columns
test = probability_blocks.join(compiled, rsuffix = 'filtered_duplicate')

#drop duplicate columns based on string identifier
final_df = test[test.columns.drop(list(test.filter(regex='filtered_duplicate')))]

final_df.to_csv(f'{root}/{dataset_name}_processed.csv')
            
            
        
        
   
    