# -*- coding: utf-8 -*-
"""
Created on Mon May  4 13:20:20 2020
Probabability pattern analysis for choice trials
@author: eacru
"""

import pandas as pd
import numpy as np


#%% 

# load file -- this should be a processed csv file with only the lever presses, wins, and losses for choice trials in the file

pattern_data = pd.read_csv("C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\OFC_PT_probability_events_processed.csv")

#combine winlose stayshift into one column

pattern_data['PatternComplete'] = pattern_data['WinLoseStayShift'] + pattern_data['StayShift']
experiment = 'PT'


#%%
#Standardize subject IDs -- only for nonspecific and dual. IT and PT are standardized
def StandardizeSubjectID(dataset):
    subject_list = list(set(dataset.subject))
    for subject in range(len(subject_list)):
        dataset.loc[dataset.subject == subject_list[subject], 'Subject'] = subject_list[subject][-2:]
   
    return(dataset)
#%%
pattern_data = StandardizeSubjectID(pattern_data)
#%% 
#For IT and PT experiments only 
pattern_data['Subject'] = pattern_data.subject
#%%

# add labels for what each date is: training, baseline, cno, or veh -- will need to be manually entered

def LabelSessionType(dataset,baseline,test1,test2,group1):
    dataset['Session']=0
    mask1 = (dataset.date == test1)
    dataset['mask1'] = mask1
    mask2 = (dataset['date'] == test2)
    dataset['mask2'] = mask2
    mask3 = (dataset['date'].isin(baseline))
    dataset['mask3'] = mask3
    for index in range(len(dataset)):
        print("Running row " + str(index) + " out of " + str(len(dataset) - 1))
        row_number = dataset.index[index]
        if dataset.mask2.iloc[index] == True:
            if dataset.Subject.isin(group1).iloc[index]:
                dataset['Session'][row_number] = 'CNO'
    
            else:
                dataset['Session'][row_number] = 'Vehicle'
        elif dataset.mask1.iloc[index] == True:
                if dataset.Subject.isin(group1).iloc[index]:
                    dataset['Session'][row_number] = "Vehicle"
                else:
                    dataset['Session'][row_number] = "CNO"
    
        elif dataset.mask3.iloc[index] == True:
            dataset['Session'][row_number] = 'Baseline'
        else:
            dataset['Session'][row_number] = 'Training'
    dataset = dataset.drop(columns = ['mask1', 'mask2', 'mask3'])
    return(dataset)


#%%
#for nonspecific and dual experiments
#pattern_data_1= LabelSessionType(pattern_data,list(set(['02/09/20','02/10/20', '02/11/20'])),'02/12/20','02/14/20',pattern_data.Subject.loc[(pattern_data.box == 1) | (pattern_data.box == 2) | (pattern_data.box == 3) |(pattern_data.box == 4) |(pattern_data.box == 5)].unique() )
#%%
#for IT and PT experiments
pattern_data_1 = LabelSessionType(pattern_data,list(set(['08/03/18','08/06/18', '08/07/18'])),'08/08/18','08/13/18',pattern_data.Subject.loc[(pattern_data.box == 2) | (pattern_data.box == 4) | (pattern_data.box == 6) |(pattern_data.box == 8) |(pattern_data.box == 10) | (pattern_data.subject == 137)].unique() )
                                  
#%% 

# Label risky and safe levers for each subject based on reward result (5.0)

def labelLosses(data):
    data_filtered = data[data.event_type_raw != 14.0]
    data_filtered = data_filtered[data_filtered.Block != 1]
    #input is a dataframe - output should be dataframe with columns to label if a choice is risky or safe
    #look for index of losses -- you just need one loss to find risky lever. Don't use block 1, since their is always reward administered
    just_losses = data_filtered.loc[data.event_type_raw.isin([33.0])]
    
# get index of losses, but only for the first loss for each  block for each session for each subject and collect the indices in a list
    idx_losses = just_losses.groupby([just_losses.Subject, just_losses.date, just_losses.Block])['event_type_raw'].idxmax().tolist()
    
#using these indices, find out what number corresponds to a loss - that is the risky lever
    return idx_losses
label = labelLosses(pattern_data_1)
#%%
def getRowForLoss(df, index):
    return df.loc[(df['Subject'] == df.Subject.iloc[index]) & 
               (df['experiment'] == df.experiment.iloc[index]) & 
               (df['date'] == df.date.iloc[index]) & 
               (df['event_type_raw'] == 33.0)]
#%%
def addRiskyLabel(data, loss_list):
    data['LeverType'] = None
    for index in loss_list:
        print("Running row " + str(index) + " out of " + str(len(loss_list) - 1))
        row_number = data.index[index]
        loss_row_df = getRowForLoss(data, index)
        loss_lever = None;
        safe_lever = None;
        if(data.event_type_raw.iloc[row_number-1]) == 1.0:
            loss_lever = 1.0
            safe_lever = 2.0
            #data.loc[(data.subject & data.date)]['LeverType'] = 'Risky'
        elif (data.event_type_raw.iloc[row_number-1]) == 2.0:
            loss_lever = 2.0
            safe_lever = 1.0
            #data.loc[(data.subject == data.subject.iloc[row_number -1] & data.date == data.date.iloc[row_number -1])]['LeverType'] = 'Risky'
        else:
            print('Not Risky')
        if(loss_lever is not None):
            data.LeverType.loc[(data['Subject'] == data.Subject.iloc[row_number -1]) & 
                      (data['date'] == data.date.iloc[row_number -1]) &
                      (data['event_type_raw'] == loss_lever)] = 'Risky'
                      
        if(safe_lever is not None):
            data.LeverType.loc[(data['Subject'] == data.Subject.iloc[row_number -1]) & 
                      (data['date'] == data.date.iloc[row_number -1]) &
                      (data['event_type_raw'] == safe_lever)] = 'Safe'
    return data

data = addRiskyLabel(pattern_data_1, label)
#%%
# Analysis 1: Percent of win-stay, lose-stay behavior by block
    
def getWinLoseStayShiftCountsByBlock(data):
#since the pattern is matched to the press, just take the press indicators
    just_presses = data.loc[data.event_type_raw.isin([1.0,2.0])]
#group by subject, date, and block
    winLoseStayShift_counts = just_presses.groupby([just_presses.Subject, just_presses.date, just_presses.Block, just_presses.LeverType, just_presses.Session])['PatternComplete'].value_counts()
    winLoseStayShift_frequencies = just_presses.groupby([just_presses.Subject, just_presses.date, just_presses.Block, just_presses.LeverType, just_presses.Session])['PatternComplete'].value_counts(normalize = True)
    winLoseStayShift_aggregate = just_presses.groupby([just_presses.Subject, just_presses.date, just_presses.LeverType, just_presses.Session])['PatternComplete'].value_counts(normalize = True)
    
# get counts for WinStay, LoseStay, WinShift, LoseShift
    return winLoseStayShift_counts, winLoseStayShift_frequencies, winLoseStayShift_aggregate

winLoseStayShift_counts, winLoseStayShift_frequencies, winLoseStayShift_aggregate = getWinLoseStayShiftCountsByBlock(data)

#%%
winLoseStayShift_counts.to_csv(f'C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\Analysis output files\\{experiment}\\winLoseStayShiftchoicetrials_counts_probability_events_processed.csv')
winLoseStayShift_frequencies.to_csv(f'C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\Analysis output files\\{experiment}\\winLoseStayShiftchoicetrial_frequencies_probability_events_processed.csv')
winLoseStayShift_aggregate.to_csv(f'C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\Analysis output files\\{experiment}\\winLoseStayShiftchoicetrial_aggfrequencies_probability_events_processed.csv')


    
#%%

just_presses = data.loc[data.event_type_raw.isin([1.0,2.0])]
count = just_presses.groupby([just_presses.Subject, just_presses.date, just_presses.Block, just_presses.Session])['LeverType'].value_counts().unstack(fill_value = 0).stack().to_frame().reset_index()
count = count.rename(columns = {0:'counts'})

#%%
def getOptimalAndDiscount(data):
    choice_1 = count[(count.Block == 1) & (count.LeverType == 'Risky')].reset_index()
    choice_2 = count[(count.Block == 2) & (count.LeverType == 'Risky')].reset_index()
    choice_4_safe = count[(count.Block ==4) & (count.LeverType == 'Safe')].reset_index()
    choice_4_risky = count[(count.Block == 4) & (count.LeverType == 'Risky')].reset_index()
    choice_compile = choice_1.merge(choice_2, on = ['Subject', 'date', 'Session'], how = 'inner').merge(choice_4_safe, on=['Subject', 'date', 'Session'], how = 'inner').rename({'counts_x': 'counts_block1', 'counts_y': 'counts_block2', 'counts':'counts_block4_safe'}, axis='columns')
    choice_compile = choice_compile.merge(choice_4_risky, on=['Subject', 'date', 'Session']).rename({'counts':'counts_block4_risky'}, axis = 'columns')
    choice_compile['percent_choice'] =(choice_compile.counts_block2/10 + choice_compile.counts_block2/10 + choice_4_safe.counts/10)/3
    choice_compile['discount_rate'] =abs((choice_compile.counts_block1/10 + choice_compile.counts_block2/10)/2 - choice_compile.counts_block4_risky/10)/3
    
    return choice_compile
#%%
optimalanddiscount = getOptimalAndDiscount(count)

optimalanddiscount.to_csv(f'C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\Analysis output files\\{experiment}\\optimalchoiceanddiscount_probability_events_processed.csv')


