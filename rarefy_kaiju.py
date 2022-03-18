#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 09:11:50 2022

@author: aku048

Rarefy the data as classified by kaiju\kraken

test.txt: one taxonomic id per line

things to consider:
    1. fraction of sample
    samp_frac <- c(0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1)
    2. Total simulation
    simulation <- 1:10
    3. Minimum occurance in a sample to claim a species
    threshold <- c(0,2,10,20, 30, 40,60,70, 80, 90, 100,150, 200)

output:
    1. rarefaction curve of more than one sample

todo:
    1. line 77 check for non classified organisms
    2. samp_frac in list
    3. Option for printing output file
    4. box plot if possible
    
flaws, should be:
    1. sample without replacement, by excluding
    2. repeating of sample is not allowed: chances are it will jeopardise the abundences of lower species count

"""

import sys
import random
import argparse
import pandas as pd
import matplotlib.pyplot as plt

     
def line_plot(temp_var, output_file):
    """
    Plot line graph  
    """
    for k, v in temp_var.items():
        plt.plot( v, label=k)
        plt.legend()  # To draw legend
    
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show() 


def average(samplefrac_classify):
    """
    Iterate over dictonary to get average out of list
    """
    for k1,v1 in samplefrac_classify.items():
        for k2, v2 in v1.items():
            v1[k2]= sum(v2)/(len(v2))
        #print(v1[k2])
    return(samplefrac_classify)
    

      
def simulation(df, sample_frac, threshold, sim_times):   
    """
    Perform simulation on sampled data 
    """
    sim_data = {} 

    for i in range(sim_times):                                           #simulate over 10 times

        sample = df.sample(frac= sample_frac)                           #sample as per fraction
        result_classify = 0                                             #initialize

        for column_name, item in sample.iteritems():                    #iterate over columns
            result_classify = classify_per(column_name, item, threshold)
            
            if column_name not in sim_data:                             #save iterative value
                sim_data[column_name] = [result_classify]
            else:
                sim_data[column_name].append(result_classify)
    return(sim_data)



def classify_per(column_name, item, threshold):
    """
    Calculates classification percentage
    """
    #total_species = len(item)
    
    count = item.value_counts(normalize=False, sort=True, dropna=True)  #sort count unique values 
    count_threshold = count.loc[lambda x : x>= threshold]               #count data greater than threshold eg. 1,2,3..

    
    fr = count_threshold.to_dict()                                      #convert to dictonary
    #print(len(fr))
    #print(total_species)
    #print(len(fr)/total_species)
    
    if 0 in fr:                                                         #if unclassified present (0), remove duirng %classified calculation
        per_classify = (len(fr) -1)
    else:
        per_classify = len(fr)
        
    """
    if 0 in fr:                                                         #if unclassified present (0), remove duirng %classified calculation
        per_classify = ((len(fr) -1)/total_species) * 100
    else:
        per_classify = (len(fr)/total_species) * 100 
    """
    #print(per_classify)
    return(per_classify)
    


def rarefy_curve(file, sample_frac, threshold, sim_times, output_file):
    """
    Function to calculate percentage of classified organism
    """
    df = pd.read_csv(file, delimiter="\t")
      
    sampl_frac1 = sample_frac.split(",")
    sample_frac = [float(x) for x in sampl_frac1]

    if not type(sample_frac) == list:                           #check if it's a list
        sample_frac = [sample_frac]
           
    samplefrac_classify = {}
    for frac in sample_frac:
        sim_frac = simulation(df, frac, threshold, sim_times)   #holds value over simulation
        samplefrac_classify[frac] = sim_frac
    
    #print(samplefrac_classify[0.95])
    avg = average(samplefrac_classify)

    my_index = list(samplefrac_classify.keys())
    #print("new key", list(samplefrac_classify.keys()) )    
    
    temp_var = {}   
    for k1,v1 in avg.items():
        for k2, v2 in v1.items():
            if k2 not in temp_var:                              #save iterative value
                temp_var[k2] = [v2]
            else:
                temp_var[k2].append(v2)
        #return(temp_var)
    
    line_plot(temp_var, output_file)    
    return(temp_var, my_index)


if __name__ == '__main__':
    ##parse your arguments
    parser = argparse.ArgumentParser(description = "Rarefaction curve")
    parser.add_argument("--file", help = "TSV file where samples are in column")
    parser.add_argument("--sample_frac", default = '0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1', type=str, help = "comma seperated fraction of sample (without spaces). Example: --sample_frac 0.01,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,.85,0.9,0.95,1")
    parser.add_argument("--threshold", nargs='?', const=1, default = 2, type=int, help = "Minimum occurance in a sample to claim a species, default = 2")
    parser.add_argument("--sim", nargs='?', const=1, default=10,  type=int, help = "No of times to simulate, default = 10")
    parser.add_argument("-o", "--output", help="Save to a file, default: Prints Rarefaction curve on the console")
    args = parser.parse_args()    
    if len(sys.argv)==1:
    # display help message when no args are passed.
        parser.print_help()
        sys.exit(1)
    rarefy_curve(args.file, args.sample_frac, args.threshold, args.sim, args.output)
    
    




   


    

