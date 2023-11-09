#!/usr/bin/python3

import os, 

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
        user_input = input("Please insert the NCBI taxon ID for the taxon of interest:\n")
        if check_integer(user_input):
            return int(user_input)


# NCBI taxon ID for taxon of interest
taxonID = get_taxonID()
print("You have entered: " + taxonID)

# the protein name of interest
protein = input("Please specify the name of the protein family of interest:\n")


