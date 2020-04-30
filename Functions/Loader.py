# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 10:37:27 2020
Loader
@author: eacru
"""

import csv

def create_file(file_name):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting = csv.QUOTE_MINIMAL)
        writer.writerow(
                ['event_type_raw',
                 'event_type',
                 'subject',
                 'date',
                 'box',
                 'experiment',
                 'timestamp'
                 ])
    
def cleanedLoadAll(cleanedRows, file_name):
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting = csv.QUOTE_MINIMAL)
        
        for cleanedRow in cleanedRows:
            writer.writerow([
                    cleanedRow.event_type_raw,
                    cleanedRow.event_type,
                    cleanedRow.subject,
                    cleanedRow.date,
                    cleanedRow.box,
                    cleanedRow.experiment,
                    cleanedRow.timestamp
                    ])
            
    return None
def ehnahncedCleanedLoadAll(cleanedRows, file_name):
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting = csv.QUOTE_MINIMAL)
        
        for cleanedRow in cleanedRows:
            writer.writerow([
                    cleanedRow.event_type_raw,
                    cleanedRow.event_type,
                    cleanedRow.subject,
                    cleanedRow.date,
                    cleanedRow.box,
                    cleanedRow.experiment,
                    cleanedRow.timestamp,
                    cleanedRow.win_lose,
                    cleanedRow.shift_stay,
                    cleanedRow.reversal_number
                    ])
            
    return None