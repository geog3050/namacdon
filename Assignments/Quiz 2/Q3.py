# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 08:42:39 2021

@author: Neal
"""
def duplicates():

    number_list = []
    number_input = eval(input("Enter a list of numbers: "))
    
    for i in number_input:
        if type(i) is int or type(i) is float:
            number_list.append(i)
        else:
            pass
        
    number_set = set(number_list)
    duplicates = []
    for i in number_set:
        if number_list.count(i)>1:
            duplicates.append(i)
    
    if len(number_set) != len(number_list):
        print("This list contains duplicates of:",duplicates)
        print("The list of unique values is therefore:",list(number_set))
    else:
        print(f"The list {number_list} does not contain duplicates")

duplicates()
