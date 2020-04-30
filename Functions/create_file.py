# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 10:12:47 2020
Load files
@author: eacru
"""
from CleanedFile import CleanedFile
import csv

def create_file(file_name):
    with open('ProbabilityDiscountingMaster.csv', mode='w') as file:
        writer = csv.writer(file, delimiter= ",", quotechar='"', quote= csv.QUOTE_MINIMAL)
        writer.writerow(
               ['event_type_raw', 
               'event_type', 
               'subject', 
               'date',
               'box', 
               'experiment', 
               'timestamp'])
    
def loadAll(cleanedRow, file_name):
    with open('ProbabilityDiscountingMaster.csv', mode='a') as file:
        writer = csv.writer(file, delimiter= ",", quotechar='"', quote= csv.QUOTE_MINIMAL)
        
        for cleanedRow in cleanedRow:
            writer = write.writerow(cleanedRow)
    return none


