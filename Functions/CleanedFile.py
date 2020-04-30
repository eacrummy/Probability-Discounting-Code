# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 09:46:59 2020
CleanedFile
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
               timestamp # seconds from start of experiment, as floating number)
               ):
            
        self.event_type_raw = event_type_raw
        self.event_type = event_type
        self.subject =subject
        self.date = date
        self.box = box
        self.experiment = experiment
        self.timestamp = timestamp
        def __str__(self):
           return str(self.__class__) + ": " + str(self.__dict__)