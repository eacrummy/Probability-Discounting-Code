# -*- coding: utf-8 -*-
"""
Reversal data processing
Created on Tue Apr 14 08:23:43 2020

@author: eacru
"""


#%%
import pandas as pd
import numpy as np

#%%

dataset = pd.read_csv("C:/Users/eacru/OneDrive/Documents/Ferguson lab data/Reversal/OFC_nonspecific/OFC Nonspecific_compiled.csv")
dataset.drop('Unnamed: 0',axis=1)
dataset['Box'] = 0
dataset['Subject']=0
#%%
#Standardize subject IDs
def StandardizeSubjectID(dataset):
    subject_list = list(set(dataset.SubjectID))
    for subject in range(len(subject_list)):
        dataset.loc[dataset['SubjectID'] == subject_list[subject], 'Subject'] = subject_list[subject][-2:]
   
    return(dataset)
    
#%%
# Add box each subject was in 
def AssignBoxNumber(dataset):
    increment = 0
    subject = list(set(dataset.Subject))
    subject.sort()
    for increment in range(len(subject)):  
    #the subject input isn't included, but it's added in to help follow along with what subject and box you are on.
        input('give me the subject: ')
        box = int(input ("give me the assigned box for this subject: "))
        dataset.loc[dataset['Subject'] == subject[increment], 'Box'] = box
    return(dataset)
    
#%%
#Assign type of session for each date
# def LabelSessionType(data, test1, test2,group1)
subject = list(set(dataset.Subject))
subject.sort()
group1 = subject[4:9]
#%%
#the group division must be generated as a new variable before implementing this function
def LabelSessionType(dataset,test1,test2,group1):
    dataset['Session']=0
    mask1 = (dataset.Date == test1)
    dataset['mask1'] = mask1
    mask2 = (dataset['Date'] == test2)
    dataset['mask2'] = mask2
    for index in range(len(dataset)):
        if dataset.mask1[index] == True:
            if dataset.Subject.isin(group1)[index]:
                dataset['Session'][index] = 'CNO'
    
            else:
                dataset['Session'][index] = 'Vehicle'
        elif dataset.mask2[index] == True:
                if dataset.Subject.isin(group1)[index]:
                    dataset['Session'][index] = "Vehicle"
                else:
                    dataset['Session'][index] = "CNO"
    
        else:
            dataset['Session'][index] = 'Baseline'
    
    return(dataset)
    
#%%
# was this a control group? Only needed for PT where there were between-subject controls
def GroupAssign(dataset,control,dreadd):
    dataset.loc[dataset['Subject'] == control]['Group'] = 'Control'
    dataset.loc[dataset['Subject']== dreadd]['Group'] = 'DREADD'
    return(dataset)


    #%%
def DropTemporaryColumns(dataset,*args,**kwargs):
    new = dataset
    for name in args:
        new = new.drop(columns = [name])
    return new
    #for name in args:
        #new = dataset.drop(columns = [name])
#%% 
        #export to csv
rootdir = 'C:/Users/eacru/OneDrive/Documents/Ferguson lab data/Reversal/OFC_nonspecific'
def ExportProcessedReversalExperimentData(dataset,rootdir, experiment):
    dataset.to_csv(f'{rootdir}/{experiment}_processed.csv')
#%%
    #groupby subject
    #do count of risky lever now
    #conditional if value for right .0 then new column risky lever is left
    count = dataset.groupby(['Subject', 'Risky Lever']).size().reset_index(name = 'totals')

    ## do the left bit!
    
    subcount = count.where(count['Risky Lever'] == 'LEFT', inplace = False).dropna()
   
    conditions = [
            (subcount['Risky Lever'] == 'LEFT') & (subcount['totals'] < 4)
        ]
    choices = ['LEFT']
    subcount['New Risky Lever'] = np.select(conditions, choices, default = 'RIGHT')
    newdf = pd.merge(dataset, subcount, left_on = ['Subject'], how = "left", right_on = ['Subject']).drop(columns = ['totals', 'Risky Lever_y'])

#%%
    # drop columns I don't need and export
    