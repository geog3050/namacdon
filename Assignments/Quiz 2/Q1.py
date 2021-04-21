# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 08:42:39 2021

@author: Neal
"""
import string

def stringcheck():

    input_string = input("Enter a string: ")
    acceptable_letters = list(string.ascii_lowercase) \
                        +list(string.ascii_uppercase)
    while True:
        try:
            letter = input("Enter a letter to search for: ")
            if len(letter) != 1 or letter not in acceptable_letters:
                raise Exception
        except Exception:
            print("Error, please enter a single letter")
        else:
            break
    
    if letter.lower() in input_string.lower():
        print("Yes")
    else:
        print("No")

stringcheck()