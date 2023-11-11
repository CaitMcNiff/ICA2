#!/usr/bin/python3

import os, subprocess
import pandas as pd


#### PUT THE FUNCTIONS AT THE TOP OF THE SCRIPT

print("Ready to begin")

# function to make sure taxonID input is an integer
def check_integer(input_variable):
    try:
        int(input_variable)
        return True
    except ValueError:
        print("The input is not an integer. Please check your input and try again.")
        return False

# Function that asks the user for an input until they give an integer response
def get_taxonID():
    while True:
        user_input = input("Please insert the NCBI taxon ID number for the taxon of interest:\n")
        if check_integer(user_input):
            return int(user_input)

# NCBI taxon ID for taxon of interest
taxonID = get_taxonID()
print("You have entered:", taxonID)

# get the taxon name from the taxon ID
taxon_name = subprocess.getoutput("esearch -db taxonomy -query '" + str(taxonID) +  " [uid]' | efetch")

# function that asks the user to make sure they got the species that they wanted
def tax_name(taxon_name):
    while True:
        if taxon_name:
            print("Taxon name: ", taxon_name)
            user_input = input("\nIs this the correct species? (yes/no): ").lower()
            if user_input == 'yes':
                print("\nGreat! Moving on.")
            elif user_input == 'no':
                print("\nPlease try entering the taxon ID of interest again.")
            else:
                print("\nInvalid input. \nPlease enter 'yes' or 'no'.\n")
        else:
            print("\nSpecies not found. \nPlease enter a valid Taxon ID.\n")
        continue

tax_name(taxon_name)

# defining the protein name of interest
protein = input("Please specify the name of the protein family of interest:\n")

# checking that the protein exists by seeing if there are results fetched from the NCBI library, counting the number of lines and saving this number as the variable prot_check
prot_check = int(subprocess.getoutput("esearch -db protein -query '" + protein +  " [PROT] NOT PARTIAL' | efetch -format uid | wc -l"))

if prot_check > 0:
    print("Great,", prot_check, "sequences were found for" , protein, "in the NCBI database.")
else: 
    print("\nThere were no results for that protein in the NCBI database. Please make sure you entered your protein name correctly.")


# retrieving the accension numbers for the defined taxon and protein family and outputting it to a file called accn.txt
subprocess.getoutput("esearch -db protein -query '" + protein + " [PROT] AND txid" + taxonID + " [ORGN]' NOT (predicted OR hypothetical)' | esummary | xtract -pattern DocumentSummary -element AccessionVersion > accn.txt")
# reading in the accn file 
with open("accn.txt") as accession_file:
    accession_numbers = accession_file.read()

# function that counts the lines in the 
def seq_count():
    While True:

        if accession_numbers.count("\n") < 1000:
            print("\nYour query resulted in", accession_numbers.count("\n"), "protein sequences.")
        else:
            input("\nYour query resulted in", accession_numbers.count("\n"), "protein sequences. That is quite a few sequences, are you sure you would like to carry on with these parameters? y/n")

# retrieving the sequences for the defined taxon and protein family
subprocess.getoutput("esearch -db protein -query '", protein,  " [PROT] AND txid", taxonID, " [ORGN] NOT (predicted OR hypothetical)' | efetch -format fasta > ", protein + str(taxonID),".fasta")

















