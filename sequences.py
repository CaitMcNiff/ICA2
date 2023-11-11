#!/usr/bin/python3

import os, subprocess
import pandas as pd

print("Ready to begin")

# function to make sure taxonID input is an integer
def check_integer(input_variable):
    try:
        int(input_variable)
        return True
    except ValueError:
        print("The input is not an integer. Please check your input and try again.")
        return False


# function that askes user for an input until they give an integer response
def get_taxonID():
    while True:
        user_input = int(input("Please insert the NCBI taxon ID for the taxon of interest:\n"))
        if check_integer(user_input):
            return int(user_input)
        
        if user_input  == 'exit':
            break

# NCBI taxon ID for taxon of interest
taxonID = get_taxonID()
print("You have entered: ", taxonID)

# get the taxon name from the taxon ID
taxon_name = subprocess.getoutput("esearch -db taxonomy -query '" + str(taxonID) +  " [uid]' | efetch")

# function that asks the user to make sure they got the species that they wanted
def tax_name():
    while True:
        if taxon_name:
            print("Taxon name: ", taxon_name)
            user_input = input("\nIs this the correct species? (yes/no): ").lower()
            if user_input == 'yes':
                print("\nGreat! Moving on.")
            elif user_input == 'no':
                print("\nPlease try again.")
            else:
                print("\nInvalid input. \nPlease enter 'yes' or 'no'.")
        else:
            print("\nSpecies not found. \nPlease enter a valid Taxon ID.")

tax_name(taxon_name)

# the protein name of interest
protein = input("Please specify the name of the protein family of interest:\n")




# retrieving the accension numbers for the defined taxon and protein family and counting how many lines these files have
#subprocess.getoutput("esearch -db protein -query '", protein,  " [PROT] AND ", taxonID, " [ORGN]' NOT (predicted OR hypothetical)' | esummary | xtract -pattern DocumentSummary -element AccessionVersion > accn.txt")


# retrieving the sequences for the defined taxon and protein family
#subprocess.getoutput("esearch -db protein -query '", protein,  " [PROT] AND ", taxonID, " [ORGN] NOT (predicted OR hypothetical)' | efetch -format fasta > ", protein + str(taxonID),".fasta")

















