#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import random
from math import ceil

def sex_choice(num):
    if num == 1:
       print 'Suga kuk'
    elif num == 2: 
       print 'Slicka fitta'
    elif num == 3:
       print 'Doggystyle'
    elif num == 4:
       print 'Knulla hårt'
    elif num == 5:
       print '69'
    elif num == 6:
       print 'Snopp i rumpen!'

def generate_sex():
    rng_num = random.random()
    num_dice_sides = 6    
    outcome = int(ceil(num_dice_sides * rng_num))
    sex_choice(outcome)
    
    return outcome

def main():
    outcome = generate_sex() 

if __name__ == "__main__":
    main()
