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

pattern_data = pd.read_csv("C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\OFC_PT_reversal_events_processed.csv")

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


trialsToReversal = getTrialstoFirstReversal(pattern_data)  
    
trialsToReversal.to_csv("C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\Analysis output files\\ trialsToReversal_PT_reversal_events_processed.csv")

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
    winLoseStayShift_aggregate = data_nonzero.groupby([data_nonzero.subject, data_nonzero.date])['PatternComplete'].value_counts(normalize = True)
# get counts for WinStay, LoseStay, WinShift, LoseShift
    return winLoseStayShift_counts, winLoseStayShift_frequencies, winLoseStayShift_aggregate

winLoseStayShift_counts, winLoseStayShift_frequencies, winLoseStayShift_aggregate = getWinLoseStayShiftCountsAfterReversal(pattern_data)

winLoseStayShift_counts.to_csv("C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\Analysis output files\\winLoseStayShiftafterreversal_counts_PT_reversal_events_processed.csv")
winLoseStayShift_frequencies.to_csv("C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\Analysis output files\\winLoseStayShiftafterreversal_frequencies_PT_reversal_events_processed.csv")
winLoseStayShift_aggregate.to_csv("C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\Analysis output files\\winLoseStayShiftafterreversal_aggfrequencies_PT_reversal_events_processed.csv")


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

winLoseStayShift_counts, winLoseStayShift_frequencies = getWinLoseStayShiftCountsBeforeReversal(pattern_data)
 
winLoseStayShift_counts.to_csv("C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\Analysis output files\\winLoseStayShiftbeforereversal_counts_PT_reversal_events_processed.csv")
winLoseStayShift_frequencies.to_csv("C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\Analysis output files\\winLoseStayShiftbeforereversal_frequencies_PT_reversal_events_processed.csv")
 

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
    idx_results = idx_wins + idx_losses
    test_df = just_results.loc[idx_results]
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
test_df = getRelevantWinLossIndices(pattern_data)    
megatest = addPreservativeResponses(test_df)
megatestcounts = megatest.groupby(['subject','date','ReversalNumber'])['event_type_raw'].count()
    
#%%
#everything to csv

megatestcounts.to_csv("C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\Analysis output files\\PreservativeResponses_PT_reversal_events_processed.csv")

    
    

        

