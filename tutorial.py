# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 08:18:25 2020

@author: eacru
"""


#myList -> addressInMemotry(98107)
#myList->address->head [1,addressToNextThing]
#addresstoNextThing -> [2, addressToNextThing] #this is referred to as a linked list connects things

#Best practices for writing function
# 1. Comment the datatype of the input and output of your function debugger window tells you types
# 2. Treat functions as immutable (stuff in the function doesn't change stuff out of the function)

#Core pattern for data extraction and cleaning script
# 1. have functions to do common things
# 2. Have a single main that executes everything
# 3. Stuff doesn't change in functions
# 4. Stuff changes in the main
# 5. Should be able to ignore what happens insde a function, you just care about in and out

# Pseduo-Code (outline)

#Purpose: read line item data from many files and convert to a friendly format
# ETL pattern (Extract, Transform, and Load)
# So, our script can start with three component, one for each of extract, transform, load

# def extract(path_to_CSV):
#    return file_contents
#what is our input? What is our output?
# input is path to csv file
#output is the contents of the csv

# def transform(file_contents):
#    return list[cleaned_row]
# input is full contents of one file
# output is collection of cleaned rows of a class we make
# class is called cleaned row

# def load(input):
#   return None
# input is list[cleaned_rows]
# no output
# side effect is that we write the cleaned file to disk

import os
os.chdir('C:\\Users\\eacru\\OneDrive\\PythonScripts')
import Functions.Extracter as Extracter
import Functions.Transformer as Transformer
import Functions.Loader as Loader

def transform(file_contents):
    cleaned_rows = []
    return cleaned_rows

def main():
    root_file_path = "C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Reversal\\IT_Hm4Di"
    output_file_path = "C:\\Users\\eacru\\OneDrive\\Documents\\Ferguson lab data\\Probability discounting\\compfiledFiles\\IT_reversal"
    Loader.create_file(output_file_path)
    file_path_list = Extracter.getFilePathList(root_file_path)
    for filePath in file_path_list:
        try:
            print(filePath + ": Extracting")
            extracted_data = Extracter.Extracter(filePath)
            print(filePath + ": Transforming")
            cleaned_data = Transformer.createCleanedFile(extracted_data)
            print(filePath + ": Loading")
            enhanced_data = Transformer.createEnhancedFile(cleaned_data)
            print(cleaned_data)
            Loader.loadAll(cleaned_data, output_file_path)
        except Exception as e:
            print(filePath + ": Skipping")
    
    
    #paths = get_path()
    #for path in paths:
    #    file_contents= extract(path)
    #    cleaned_rows = transform(file_contents)
    #    create_file(cleaned_rows) 

main()