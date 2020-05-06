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

#%% 

# Label risky and safe levers for each subject based on reward result (5.0)

def labelLosses(data):
    data_filtered = data[data.event_type_raw != 14.0]
    data_filtered = data_filtered[data_filtered.Block != 1]
    #input is a dataframe - output should be dataframe with columns to label if a choice is risky or safe
    #look for index of losses -- you just need one loss to find risky lever. Don't use block 1, since their is always reward administered
    just_losses = data_filtered.loc[data.event_type_raw.isin([33.0])]
    
# get index of losses, but only for the first loss for each  block for each session for each subject and collect the indices in a list
    idx_losses = just_losses.groupby([just_losses.subject, just_losses.date, just_losses.Block])['event_type_raw'].idxmax().tolist()
    
#using these indices, find out what number corresponds to a loss - that is the risky lever
    return idx_losses
label = labelLosses(pattern_data)
#%%
def getRowForLoss(df, index):
    return df.loc[(df['subject'] == df.subject.iloc[index]) & 
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
                data.LeverType.loc[(data['subject'] == data.subject.iloc[row_number -1]) & 
                          (data['date'] == data.date.iloc[row_number -1]) &
                          (data['event_type_raw'] == loss_lever)] = 'Risky'
                          
            if(safe_lever is not None):
                data.LeverType.loc[(data['subject'] == data.subject.iloc[row_number -1]) & 
                          (data['date'] == data.date.iloc[row_number -1]) &
                          (data['event_type_raw'] == safe_lever)] = 'Safe'
        return data

data = addRiskyLabel(pattern_data, label)
#%%
# Analysis 1: Percent of win-stay, lose-stay behavior by block
    
def getWinLoseStayShiftCountsByBlock(data):
#since the pattern is matched to the press, just take the press indicators
    just_presses = data.loc[data.event_type_raw.isin([1.0,2.0])]
#group by subject, date, and block
    winLoseStayShift_counts = just_presses.groupby([just_presses.subject, just_presses.date, just_presses.Block, just_presses.LeverType])['PatternComplete'].value_counts()
    winLoseStayShift_frequencies = just_presses.groupby([just_presses.subject, just_presses.date, just_presses.Block, just_presses.LeverType])['PatternComplete'].value_counts(normalize = True)
    winLoseStayShift_aggregate = just_presses.groupby([just_presses.subject, just_presses.date, just_presses.LeverType])['PatternComplete'].value_counts(normalize = True)
    
# get counts for WinStay, LoseStay, WinShift, LoseShift
    return winLoseStayShift_counts, winLoseStayShift_frequencies, winLoseStayShift_aggregate

winLoseStayShift_counts, winLoseStayShift_frequencies, winLoseStayShift_aggregate = getWinLoseStayShiftCountsByBlock(data)

#%%
winLoseStayShift_counts.to_csv("C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\Analysis output files\\winLoseStayShiftchoicetrials_counts_PT_probability_events_processed.csv")
winLoseStayShift_frequencies.to_csv("C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\Analysis output files\\winLoseStayShiftchoicetrial_frequencies_PT_probability_events_processed.csv")
winLoseStayShift_aggregate.to_csv("C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\Analysis output files\\winLoseStayShiftchoicetrial_aggfrequencies_PT_probability_events_processed.csv")

#%%
def getPercentChoice(data):
    just_presses = data.loc[data.event_type_raw.isin([1.0,2.0])]
    
    choice_counts = just_presses.groupby([just_presses.subject, just_presses.date, just_presses.Block])['LeverType'].value_counts()
    choice_frequencies = just_presses.groupby([just_presses.subject, just_presses.date, just_presses.Block])['LeverType'].value_counts(normalize = True)
    
    choice_1 = just_presses[just_presses.Block == 1] 
    choice_1 = choice_1[choice_1.LeverType == 'Risky']                           
    choice_2 = just_presses[just_presses.Block ==2]
    choice_2 = choice_2[choice_2.LeverType == 'Risky']
    choice_4 = just_presses [just_presses.Block == 4]
    choice_4 = choice_4[choice_4.LeverType == 'Safe']
    percent_optimal = choice_1.groupby([choice_1.subject, choice_1.date])['LeverType' == 'Risky'].count
    return choice_counts, choice_frequencies

choice_counts, choice_frequencies = getPercentChoice(data)
    
#%%

    just_presses = data.loc[data.event_type_raw.isin([1.0,2.0])]
    count = just_presses.groupby([just_presses.subject, just_presses.date, just_presses.Block])['LeverType'].value_counts().unstack(fill_value = 0).stack().to_frame().reset_index()
    count = count.rename(columns = {0:'counts'})

#%% 
    #Use the extracted datafile from scott for the following functions
extracted_data = pd.read_csv("C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\OFC nonspecific\\OFC nonspecific_prob_processed.csv")
#%%
def percentOptimal(data):
    percent_optimal = pd.DataFrame(columns = ['subject','date','percent_optimal_choice'])
    for index, date in enumerate(data.date.unique()):
        for index, subject in enumerate(data.subject.unique()):
            choice_1 =count.loc[(count.Block == 1) & (count.LeverType == 'Risky') & (data.subject == subject) & (data.date == date)].counts.reset_index()
            choice_2 =count.loc[(count.Block == 2) & (count.LeverType == 'Risky') & (data.subject == subject) & (data.date == date)].counts.reset_index()
            choice_4_safe =count.loc[(count.Block == 4) & (count.LeverType == 'Safe') & (data.subject == subject) & (data.date == date)].counts.reset_index()
            percent_choice =(choice_1.counts/10 + choice_2.counts/10 + choice_4_safe.counts/10)/3
            print(percent_choice)
            print(subject)
            print(date)
            percent_optimal = percent_optimal.append({'subject': subject, 'date': date, 'percent_optimal_choice': percent_choice}, ignore_index = True)
    return percent_optimal
#%% 

percent_optimalchoice = percentOptimal(count)
percent_optimalchoice.to_csv("C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\Analysis output files\\optimalchoice_PT_probability_events_processed.csv")

#%%
def discountRate(date):
    discount_rate = pd.DataFrame(columns = ['subject','date','discount_rate'])
    for index, date in enumerate(data.date.unique()):
            for index, subject in enumerate(data.subject.unique()):
                choice_1 =count.loc[(count.Block == 1) & (count.LeverType == 'Risky') & (data.subject == subject) & (data.date == date)].counts.reset_index()
                choice_2 =count.loc[(count.Block == 2) & (count.LeverType == 'Risky') & (data.subject == subject) & (data.date == date)].counts.reset_index()
                choice_4_risky =count.loc[(count.Block == 4) & (count.LeverType == 'Risky') & (data.subject == subject) & (data.date == date)].counts.reset_index()
                discount = abs((choice_1.counts/10 + choice_2.counts/10)/2 - choice_4_risky.counts/10)/3
                print(discount)
                print(subject)
                print(date)
                discount_rate = discount_rate.append({'subject': subject, 'date': date, 'discount_rate': discount}, ignore_index = True)
    return discount_rate

#%%

discount_rate = discountRate(count)
discount_rate.to_csv("C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\Analysis output files\\discountrate_PT_probability_events_processed.csv")