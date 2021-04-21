# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 08:42:39 2021

@author: Neal
"""
def secondlargest():

    number_list = []
    number_input = eval(input("Enter a list of numbers: "))
    
    for i in number_input:
        if type(i) is int or type(i) is float:
            number_list.append(i)
        else:
            pass
        
    sorted_list = sorted(number_list)
    print("Second largest value is",sorted_list[-2])

secondlargest()