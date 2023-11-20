#!/usr/bin/python3

import os, subprocess
import pandas as pd

### Start of function definition 
def dir():
    while True:
        directory = input("\nwould you like to make a new directory for any ouput files? y/n\n")
        if directory == 'y':
            name = str(input("\nwhat would you like to call your directory?\n"))
            os.mkdir(name) # make new directory based on the imputted name
            os.chdir(name) # change working directory to the new new directory
            print("you are now working in the new directory", name)
            return
        elif directory == 'n':
            print("Okay no directory will be created and any output files will be created in your present directory")
            return
        else:
            print("\nInvalid input. \nPlease enter 'y' or 'n'.\n")

# function to make sure taxonID input is an integer
def check_integer(input_variable):
    try:
        int(input_variable)
        return True
    except ValueError:
        print("The input is not an integer. Please check your input and try again.")
        return False


# function that asks the user for an input until they give an integer response
def get_taxonID():
    while True:
        user_input = input("Please insert the NCBI taxon ID number for the taxon of interest:\n")
        if check_integer(user_input):
            return int(user_input)

# function that asks the user to make sure they got the species that they wanted
def tax_name():
    while True:
        taxonID = get_taxonID()
        print("You have entered:", taxonID)
        # get the taxon name from the taxon ID
        taxon_name = subprocess.getoutput("esearch -db taxonomy -query '" + str(taxonID) +  " [uid]' | efetch")
        # checking the user is happy with the input
        if taxon_name:
            print("Taxon name: ", taxon_name)
            user_input = input("\nIs this the correct species? (y/n): ").lower()
            if user_input == 'y':
                print("\nGreat! Moving on.")
                return taxon_name,taxonID
            elif user_input == 'n': # if they are not happy, then they get the chance to enter a new taxon ID
                print("\nPlease try entering the taxon ID of interest again.")
            else:
                print("\nInvalid input. \nPlease enter 'y' or 'n'.\n")
        else:
            print("\nSpecies not found. \nPlease enter a valid Taxon ID.\n")
        continue

# function that checks the inputted protein exists
def protein_check():
    while True:
        # defining the protein name of interest
        protein = input("Please specify the name of the protein family of interest:\n")
        # checking that the protein exists by seeing if there are results fetched from the NCBI library, counting the number of lines and saving this number as the variable prot_check
        prot_check = int(subprocess.getoutput("esearch -db protein -query '" + protein +  " [PROT] NOT PARTIAL' | efetch -format uid | wc -l"))
        # checking there is at least 1 row in file
        if prot_check > 0:
            print("Great,", prot_check, "sequences were found for" , protein, "in the NCBI database.")
            return protein
        else:
            print("\nThere were no results for that protein in the NCBI database. Please make sure you entered your protein name correctly.")
        continue


# function that counts the number of sequences the query retrieves
def seq_count():
    while True:
        # retrieving the accension numbers for the defined taxon and protein family and outputting it to a file called accn.txt
        subprocess.getoutput("esearch -db protein -query '" + protein + "[PROT] AND txid" + str(taxonID) + "[Organism:exp] NOT (predicted OR hypothetical)' | esummary | xtract -pattern DocumentSummary -element AccessionVersion > accn.txt")
        # reading in the accn file
        with open("accn.txt") as accession_file:
            accession_numbers = accession_file.read()
        line_count = accession_numbers.count("\n")
        # checking the number of sequences from the query
        if line_count < 1000:
            print("\nYour query resulted in", line_count, "protein sequences.")
            return
        else:
            q = input("\nYour query resulted in over 1000 protein sequences. That is quite a few sequences, are you sure you would like to carry on with these parameters? y/n\n").lower()
            if q == 'y':
                print("Okay, if youre sure.")
                return
            elif q == 'n':
                print("\nOkay, press 'control+D' on your keyboard to escape from the script and rerun the script with a new input taxon ID and/or protei.n\n")
            else:
                print("\nInvalid input. \nPlease enter 'y' or 'n'.\n")

# function that aligns the protein sequences, plots a conservation plot based on the seqquences, and output the graph to the screen
def plot_seq():
    print("Creating conservation graphs, please wait...")
    # using clustalo to align the sequences and convert the output to .msf
    subprocess.call("clustalo -i " + query_name + ".fasta -o protein_alignment_" + query_name + ".msf --outfmt msf --threads 200 --force", shell = True )
    # plotting the conservation plot of all the sequences that were retrieved from the NCBI database and saving it as a png
    subprocess.call("plotcon -sequences protein_alignment_" + query_name + ".msf -winsize 4 -graph png -stdout > "+ query_name + "_plotcon.png", shell =True) ### TRY TO FIND OUT HOW TO CHANGE THE OUTPUT NAME FOR THE PLOTCON
    # bringing the conservation plot to the screen
    subprocess.call("gio open plotcon.1.png", shell = True)

# function that splits the fasta file into individal sequence files with the new files being named after the accession numbers
def split_seq(input_file, accn_file):
    #open accn.txt file
    with open(accn_file, 'r') as accn_file:
        accn_lines = accn_file.readlines()
    #open fasta file
    with open(input_file, 'r') as input_file:
        content = input_file.read()
    sections = content.split('>') # spilt based on the '>'
    sections = [section.strip() for section in sections if section.strip()]
    for section in sections:
        lines = section.split('\n')
        identifier = lines[0].split()[0]  # assumes the identifier is the first word after ">"
        for accn_line in accn_lines:
            accn = accn_line.strip()
            #mathcing the accession number from fasta file to accn.txt file to create output file name
            if accn == identifier:
                output_filename = f"{accn}.fasta"
                with open(output_filename, 'w') as output_file:
                    output_file.write(f">{section}")
                print(f"Match found! Created file: {output_filename}")
                break
        else:
            print(f"No match found for {identifier}")

### End of function definition

print("Ready to begin")

# asking the user if they would like to create a directory for the output files
dir()

# defining taxon name and taxonID as the outputs from the tax_name function
taxon_name, taxonID = tax_name()
# defining the protein
protein = protein_check()
# checking the number of sequences for the query
seq_count()

# retrieving the sequences for the defined taxon and protein family
query_name = protein + "_txid" + str(taxonID)

# getting the fasta sequences from the NCBI database from the query name
subprocess.getoutput("esearch -db protein -query '" + protein + " [PROT] AND txid" + str(taxonID) + " [Organism:exp] NOT (predicted OR hypothetical)' | efetch -format fasta > " + query_name + ".fasta")

#plotting conservation plot
plot_seq()

# splititng the fasta file into individual sequence files
split_seq(query_name,".fasta", "accn.txt")

# making a directory for the patmatmotifs output files to go into
os.makedirs("motifs", exist_ok=True)

# run the PROSITE motif search
with open("accn.txt", 'r') as accn_file:
    for accn in accn_file:
        accn = accn.strip()
        # Use patmatmotifs to search for motifs in the chosen sequence file
        subprocess.call("patmatmotifs -sequence " + accn + ".fasta -outfile " + accn + "_res.patmatmotifs -full -auto Yes", shell = True)

#creating an output file for the sequences with motif hits
output_file = 'motifs_hits.txt'
dir_path = 'motifs/'

# opening the output file in write mode
with open(output_file, 'w') as output:
    # loop through all files in the directory
    for filename in os.listdir(dir_path):
        # check if the file ends with .patmatmotifs
        if filename.endswith('.patmatmotifs'):
            file_path = os.path.join(dir_path, filename)
            # opening the patmatmotifs file and check for the condition
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('# HitCount:') and not line.startswith('# HitCount: 0'):
                        # If the condition is met, write the filename to the output file
                        output.write(filename + '\n')
                        break  # Break out of the loop once a match is found

# Print a message indicating the process is complete
print("Files with motif hits written to:", output_file)
with open("motifs_hits.txt", 'r') as hits:
    x = len(hits.readlines())
    print('Number of files that have one or more motif hits:', x)
