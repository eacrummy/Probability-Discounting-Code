# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 16:10:11 2020
Pattern Analysis
@author: eacru
"""
import pandas as pd
import numpy as np

#%% 

# load file

pattern_data = pd.read_csv("C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\OFC_nonspecific_reversal_events_processed.csv")

#combine winlose stayshift into one column

pattern_data['PatternComplete'] = pattern_data['WinLoseStayShift'] + pattern_data['StayShift']

#%% 

#Analysis 1 get trials to first reversal

#input is dataframe
def getTrialstoFirstReversal(data):
    #filter data to just be the presses:
    just_presses = data.loc[data.event_type_raw.isin([1.0,2.0])]
#select only reversal number zero
    data_zero = just_presses[just_presses.ReversalNumber == 0]
#group by subject and date
#get count of number of 1 and 2's (presses)
    trialsToReversal = data_zero.groupby([data_zero.subject, data_zero.date])['event_type_raw'].sum()
    return trialsToReversal


    
    


#output is list group of counts for each subject in each session
#%%
# Analysis 2: Percent of win-stay, lose-stay behavior after first reversal
    
def getWinLoseStayShiftCountsAfterReversal(data):
#since the pattern is matched to the press, just take the press indicators
    just_presses = data.loc[data.event_type_raw.isin([1.0,2.0])]
# exclude the block before the first reversal
    data_nonzero = just_presses[just_presses.ReversalNumber != 0]
#group by subject, date, and reversal block
    winLoseStayShift_counts = data_nonzero.groupby([data_nonzero.subject, data_nonzero.date, data_nonzero.ReversalNumber])['PatternComplete'].value_counts()
    winLoseStayShift_frequencies = data_nonzero.groupby([data_nonzero.subject, data_nonzero.date, data_nonzero.ReversalNumber])['PatternComplete'].value_counts(normalize = True)
# get counts for WinStay, LoseStay, WinShift, LoseShift
    return winLoseStayShift_counts, winLoseStayShift_frequencies

#%%
# Analysis 3: Percent win-stay, lose-stay behavior before first reversal
    
def getWinLoseStayShiftCountsBeforeReversal(data):
    just_presses= data.loc[data.event_type_raw.isin([1.0,2.0])]
# take only the trials before the first reversal occurred
    data_zero = just_presses[just_presses.ReversalNumber == 0]
#group by subject and date
#get winstaylosestaywinshiftloseshift counts raw and frequencies
    winLoseStayShift_counts = data_zero.groupby([data_zero.subject, data_zero.date])['PatternComplete'].value_counts()
    winLoseStayShift_frequencies = data_zero.groupby([data_zero.subject, data_zero.date])['PatternComplete'].value_counts(normalize = True)
# get counts for WinStay, LoseStay, WinShift, LoseShift
    return winLoseStayShift_counts, winLoseStayShift_frequencies

    #%%
def getIndexPositionsByCondition(listOfElements, condition):
    ''' Returns the indexes of items in the list that returns True when passed
    to condition() '''
    indexPosList = []
    for i in range(len(listOfElements)): 
        if condition(listOfElements[i]) == True:
            indexPosList.append(i)
    return indexPosList

#%%

# Analysis 4: Get perseverative responses after reversal

def getRelevantWinLossIndices(data):
    
#exlcude blocks before the first reversal and focus on reward or loss (5 or 33)
    just_results = data[data.ReversalNumber != 0].loc[data.event_type_raw.isin([5.0, 33.0])]
    just_wins = data[data.ReversalNumber != 0].loc[data.event_type_raw.isin([5.0])]
    just_losses = data[data.ReversalNumber != 0].loc[data.event_type_raw.isin([33.0])]
    
# get index of wins, but only for the first win for each reversal block for each session for each subject and collect the indices in a list
    idx_wins = just_wins.groupby([just_wins.subject, just_wins.date, just_wins.ReversalNumber])['event_type_raw'].idxmax().tolist()
# get all of the losses and collect in a list
    idx_losses = just_results[just_results.event_type_raw == 33.0].index.values.tolist()
# using indices, select in dataframe where these losses and wins occurred
    test_df = just_results.loc[idx_losses or idx_wins]
# output should be dataframe with relevant wins and losses    
   return test_df
#%%
#using dataframe with selected indices, make function with data input and look up row in each reversal number where the first win occurred
   def getRowForWin(df, index):
    return df.loc[(df['subject'] == df.subject.iloc[index]) & 
               (df['experiment'] == df.experiment.iloc[index]) & 
               (df['date'] == df.date.iloc[index]) & 
               (df['event_type_raw'] == 5) &
               (df['ReversalNumber'] == df.ReversalNumber.iloc[index])]
#%%
    #%%
#input is dataframe filtered to be all losses and no other event types, as well as list of indexes where a first win occurs in each reversal 
#output should be either dataframe or list of indices of all losses with indexes lower than first win for each Reversal block number
#for each Reversal number
def addPreservativeResponses(df):
    new_df = pd.DataFrame(columns = df.columns)
    for i in range(len(df)):
        print("Running row " + str(i) + " out of " + str(len(df) - 1))
        row_number = df.index[i]
        winning_row_df = getRowForWin(df, i)
        if((df.event_type_raw.iloc[i]) != 5 and len(winning_row_df) > 0 and row_number < winning_row_df.index[0]):
            new_df.loc[i] = df.iloc[i]
        else:
            print('after first win')
            
    return new_df

#%%

just_results = pattern_data[pattern_data.ReversalNumber != 0].loc[pattern_data.event_type_raw.isin([5.0, 33.0])]
just_wins = pattern_data[pattern_data.ReversalNumber != 0].loc[pattern_data.event_type_raw.isin([5.0])]
just_losses = pattern_data[pattern_data.ReversalNumber != 0].loc[pattern_data.event_type_raw.isin([33.0])]

idx_wins = just_wins.groupby([just_wins.subject, just_wins.date, just_wins.ReversalNumber])['event_type_raw'].idxmax().tolist()
idx_losses = just_results[just_results.event_type_raw == 33.0].index.values.tolist()
idx_losses_mini = idx_losses[:50]
idx_wins_mini = idx_wins[:50]
#combines relevant wins and losses indices into one list 
indices_list = idx_losses + idx_wins
#sort in ascending order
indices_list.sort()
#use the indices list to filter out dataframe for relevant rows

test_df = pattern_data.loc[indices_list]

#%%
    test_df = just_results.loc[idx_losses or idx_wins]
    grouped_presresponses = test_index.groupby([test_index.subject,test_index.date,test_index.ReversalNumber])['event_type_raw']
    
    
    #compare to when you just have sum of losses grouped by subject, date and reversal number
    
    grouped_alllosses = just_losses.groupby([just_losses.subject, just_losses.date, just_losses.ReversalNumber])['event_type_raw'].count()
#%%

    
    

        

