#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 09:11:50 2022

@author: aku048

# Plot Accumulation Curve from the data as classified by kaiju\kraken: copy only tax_id column in tsv file with sample header

test.txt: sample header with taxonomic id per line

Things to consider:
    1. fraction of sample
    samp_frac <- c(0, 0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1)
    2. Total simulation
    simulation <- 1:10
    3. Minimum occurance in a sample to claim a species
    threshold <- c(0,2,10,20, 30, 40,60,70, 80, 90, 100,150, 200)

Output:
    1. Accumulation Curve of more than one sample, default print image on the console
    2. Option to save image file and output data
    
Keep in mind:
    1. Sampling with replacement
    2. Accumulation curve: https://www.biosym.uzh.ch/modules/models/Biodiversity/MeasuresOfBioDiversity.html

"""

__author__ = "Animesh"
__version__ = '0.2.0'

import sys
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


   
def my_plot(temp_var, file, splot, format, ci):
    """
    #Plot line graph  
    """ 
    rel = sns.relplot(data = temp_var, x = 'sample_fraction', y = 'counts', ci=ci, kind= 'line', hue = 'sample', legend = "full")
    rel.fig.suptitle('Accumulation Curve')
    rel.set_axis_labels("Fraction of samples", "Species Estimated")
    plt.tight_layout()                                                  #stretch x-axis
    
    if ci:
        plt.text(0.95, 0, f'ci = {ci}')                                 #print "ci" on the plot

    if splot:
        print ("Analysis Done! \nPlease find the accumulation curve:", splot+"."+format)
        plt.savefig(splot+"."+format)
    else:        
        plt.show()

      
def simulation(my_file, sample_frac, threshold, sim_times):   
    """
    #Perform simulation on sampled data 
    """
    data_over_simulated = pd.DataFrame(columns=["sample", "counts"])    #create new dataframe
    
    for i in range(sim_times):                                          #simulate over 10 times
        sample = my_file.sample(frac= sample_frac)                      #select sample as per fraction
        
        result_classify = 0                                             #initialize
        for column_name, value in sample.iteritems():                   #iterate over columns
            result_classify = classify_count(column_name, value, threshold)
            data_over_simulated = data_over_simulated.append({"sample" : column_name, "counts" : result_classify}, ignore_index = True) #append dataframe
    
    data_over_simulated['sample_fraction'] = sample_frac                #add new column
    
    return(data_over_simulated)


def classify_count(column_name, item, threshold):
    """
    #Calculates classified taxon count
    """
    #total_species = len(item)
    count = item.value_counts(normalize=False, sort=True, dropna=True)  #sort count unique values 
    count_threshold = count.loc[lambda x : x>= threshold]               #count data greater than threshold eg. 1,2,3..
    
    fr = count_threshold.to_dict()                                      #convert to dictonary
    if 0 in fr:                                                         #if unclassified present (0), remove duirng %classified calculation
        classify = (len(fr) -1)
    else:
        classify = len(fr)
    return(classify)
    

def accumulation_curve(file, sample_frac, threshold, sim_times, ci, splot, format, sdata):
    """
    #Function to calculate percentage of classified organism
    """
    my_file = pd.read_csv(file, delimiter="\t")
      
    sampl_frac1 = sample_frac.split(",")
    sample_frac = [float(x) for x in sampl_frac1]                        #seperate sample fraction input by seperator ","

    if not type(sample_frac) == list:                                    #check if it's a list
        sample_frac = [sample_frac]
     
    all_sim_data = pd.DataFrame(columns=["sample", "counts", "sample_fraction"])  
           
    for frac in sample_frac:
        sim_frac = simulation(my_file, frac, threshold, sim_times)        #holds value over simulation dataframe
        
        all_sim_data = all_sim_data.append(sim_frac, ignore_index= True)  #append all data
    
    all_sim_data["counts"] = pd.to_numeric(all_sim_data["counts"], downcast="float")   
    all_sim_data["sample_fraction"] = pd.to_numeric(all_sim_data["sample_fraction"], downcast="float") 
    #print(all_sim_data.to_string())                                      #print all final data on screen; for testing; just ignore it 

    my_plot(all_sim_data, file, splot, format, ci)
    
    if sdata:
        all_sim_data.to_csv(f'{sdata}_final_data_to_plot.csv', index=False) #option for saving data used for plotting
        print (f'Output data saved as: {sdata}_final_data_to_plot.csv')
    

def check_ci(arg):                                                        #checks for str (sd) or int (0-100) for ci 
    if arg == "None":
        return 0
    elif arg == "sd":
        return arg
    elif 0 <= int(arg) <= 100:
        return int(arg)
    else:
        raise argparse.ArgumentTypeError(f"{arg} must be in the range 0-100")

if __name__ == '__main__':
    ##parse your arguments
    parser = argparse.ArgumentParser(description = "Accumulation curve")
    parser.add_argument("--file", help = "TSV file where samples are in column")
    parser.add_argument("--sample_frac", default = '0, 0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1', type=str, help = "comma seperated fraction of sample (without spaces), default: --sample_frac 0,0.01,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,.85,0.9,0.95,1")
    parser.add_argument("--threshold", nargs='?', const=1, default = 2, type=int, help = "Minimum occurance in a sample to claim a species, default = 2")
    parser.add_argument("--sim", nargs='?', const=1, default=10,  type=int, help = "No of times to simulate, default = 10")
    parser.add_argument("--ci", default = None, action="store", type = check_ci, help = "Size of confidence interval, ci: None (default) or sd (standard deviation) or int (95)")
    parser.add_argument("--splot", help="Save the plot as...")
    parser.add_argument("--format", choices=('png', 'jpeg', 'jpg', 'tiff', 'pdf'), default = 'png', help="Save plot output format as..., default = png")
    parser.add_argument("--sdata", help="Save the final output data used for plotting as...")
    args = parser.parse_args()    
    if len(sys.argv)==1: 
        parser.print_help()                                    # display help message when no args are passed.
        sys.exit(1)
    accumulation_curve(args.file, args.sample_frac, args.threshold, args.sim, args.ci, args.splot, args.format, args.sdata)
    
    