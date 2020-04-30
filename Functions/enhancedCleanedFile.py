# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 15:45:23 2020
Enhanced Clean File
@author: eacru
"""

class CleanedFile:
    def __init__(self,
               event_type_raw, # type of event, not modified from source, as string
               event_type, # type of event, as string
               subject, #subjectID, string
               date, # dd-mm-yyyy of event
               box, #box number, string
               experiment, # experiment name, string,
               timestamp, # seconds from start of experiment, as floating number)
               win_lose, #did the response result in reward or not
               shift_stay,
               reversal_number
               ):
            
        self.event_type_raw = event_type_raw
        self.event_type = event_type
        self.subject =subject
        self.date = date
        self.box = box
        self.experiment = experiment
        self.timestamp = timestamp
        self.win_lose = win_lose
        self.shift_stay = shift_stay
        self.reversal_number = reversal_number
        def __str__(self):
           return str(self.__class__) + ": " + str(self.__dict__)