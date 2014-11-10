# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 16:12:05 2014

@author: Daniel
"""
import re

from pprint import pprint as pp

with open('MF_list.txt','r') as in_file:
    meat = in_file.read() 
    
pattern = re.compile(r'(.+)')
mf = filter(lambda x: len(x) > 0, [re.sub('\r', '', line) for line in pattern.findall(meat)])

pp(mf)