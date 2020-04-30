# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 08:45:56 2020
Transform for probability discounting
@author: eacru
"""

#Transform function: the goal is to format the data so that event and time stamps for each subject are matched for each session
# 1: identify parts of text file that need to be kept, and those that can be ignored and not saved into final transform (input list, output separated list)
    # read in the line item from each csv as list, and use identifiers to extract out desired lines)
# 2: in lines that should be kept, separate out the rows based on the delineater (input is row list, output is separated values (as string?))
# 3: for timestamps, convert to seconds
# 4: restructure data so that it is organized to have in columns: subject, date, box, experiment, event (E:), converted invent types to string or numeric codes, and timestamps (F:) converted to seconds
    #for timestamps, each unit is is 10msec, so divide by 100 to get seconds.
import re
from Functions.CleanedFile import CleanedFile
 #1: get some identifiers   
def getDateOfSession(data_list):
    date_of_session = None
    for data_lines in data_list:
        for data in data_lines:
            if 'Start Date:' in data:
                date_of_session = data.split(": ")
    return date_of_session

def getSubjectName(data_list):
    subject_id = None
    for data_lines in data_list:
        for data in data_lines:
            if 'Subject:' in data:
                subject_id = data.split(": ")
    return subject_id

def getExperimentLabel(data_list):
    experiment = None
    for data_lines in data_list:
        for data in data_lines:
            if 'Experiment:' in data:
                experiment = data.split(": ")
    return experiment

def getBoxLabel(data_list):
    box = None
    for data_lines in data_list:
        for data in data_lines:
            if 'Box:' in data:
                box = data.split(": ")
    return box

def splitLines(data):
    element_list = None
    element_list = data.split(": ")
    return(element_list)
    
# make a function that goes back and gives you the most recent letter for what something is

def getCurrentLetter(line, current_letter):
    if len(line) >0 and re.search('^[A-Z]:', line[0]):
        new_letter = line[0].split(":")[0]
        return new_letter
    else:
        return current_letter

def getLineValues(line):
    
    if len(line) > 0 and re.search('^[ ]+[0-9]+:',line[0]):
        row = line[0].split(":")[1]
        return row.split()
    return []

def getByLetter(data_lines, letter):
    new_array = []
    current_letter = None
    for line in data_lines:
        current_letter = getCurrentLetter(line, current_letter)
        if current_letter == letter:
            data_list = getLineValues(line)
            for data in data_list:
                new_array.append(data)

    return new_array
# in transformer, make function(s(s) that look at read lines and see if the following matches occur:
    #Win stay: Pattern for reversal: right(1) or left(2), followed by pellet(5), followed by same 1 or 2.
        #Pattern for probability: 1,2 followed by 5, followed by 1 or 2 again, but only if after a 14 (choice trial starts)
    #Lose stay: same pattern, but instead of pellets (5), 1 or 2 is followed by green cue light (33) and same 1 or 2. For prob, only after a 14 (choice trial start)
    #Win shift: instead of same 1 or 2 after a 5, switch to the other number. In probability, only have a 14
    #Lose_shift: instead of same 1 or2 after a 33, switch to the other number. In probability, only after a 14
# If a reversal file: 
    #mark when a reversal occurs: E(35). Keep a running tally of reversal number
def leverPressLabel(data_lines, previous_number):
    if data_lines[0] is "1.000" or "2.000":
        previous_previous_number = previous_number
        previous_number = data_lines[0]
        return previous_number
        return previous_previous_number
    else:
        previous_number = previous_number
        return previous_number
        return previous_previous_number
                        
def winLoseMetricsLabel(currentEvent, previousEvent):
    if currentEvent == "5" and previous_number and previous_previous_number == previous_number:
        return 'WIN_STAY'
    if currentEvent == "5" and previous_number and previous_previous_number != previous_number:
        return 'WIN_SHIFT'
    if currentEvent =="33" and previousEvent and previous_previous_number == previous_number:
        return 'LOSE_STAY'
    if currentEvent == "33" and previousEvent and previous_previous_number != previous_number:
        return 'LOSE_SHIFT'
    
    
    
def createCleanedFile(data_lines):
    #this is for 1 file, not all the files
    # step 1: get the static stuff (subject, box, exp), store as variable
    subject = getSubjectName(data_lines)[1]
    date = getDateOfSession(data_lines)[1]
    experiment = getExperimentLabel(data_lines)[1]
    box = getBoxLabel(data_lines)[1]
    
    #print(subject)
    #print(date)
    #print(experiment)
    #print(box)
    # step 2: get the Es, get the Fs
    event_types = getByLetter(data_lines, 'E')
    timestamps = getByLetter(data_lines, 'F') #timestamps need to be divided by 100
    compiled_events_times = []
    for index in range(0, len(event_types)):
        cleanedFile = CleanedFile(
                            event_types[index], 
                            None, 
                            subject, 
                            date, 
                            box, 
                            experiment, 
                            float(timestamps[index])/100)
        
        #print("new file!")
        #print(cleanedFile.event_type_raw)
        #print(cleanedFile.event_type)
        #print(cleanedFile.subject)
        #print(cleanedFile.date)
        #print(cleanedFile.box)
        #print(cleanedFile.experiment)
        #print(cleanedFile.timestamp)
        
        compiled_events_times.append(cleanedFile)
    return compiled_events_times

def createEnhancedFile(cleanedData):
    return None;
    # step 3: iterate through all Es, Fs, and populate a list of CleanedFile
    # return list of Cleaned File
    
    #event_type_raw, # type of event, not modified from source, as string
    #           event_type, # type of event, as string
    #           subject, #subjectID, string
    #           date, # dd-mm-yyyy of event
    #           box, #box number, string
    #           experiment, # experiment name, string,
    #           timestamp # seconds from start of experiment, as floating number)
    
#    A:
#       0: jkekjlerjklerjkl
#   B:
#       0: dsflkjdfslkjdsfjkldfs
#       5: jklefkjefkjlfdsjkldsfkjl

#function returns:
#A
#A
#B
#B
#B

# def getCurrentLetter(line, existingLetter):
#       if the line is for a letter, return the letter of the line
#       otherwise, return the existing letter
#       call for each line in file      
        
    #now is other line in format digit: 1 2 3 4 5 