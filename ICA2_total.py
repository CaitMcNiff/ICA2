#!/usr/bin/python3

import os, subprocess
import pandas as pd

### Start of function definition 
def dir():
    while True:
        directory = input("\nwould you like to make a new directory for any ouput files? y/n\n")
        if directory == 'y':
            name = str(input("\nwhat would you like to call your directory?\n"))
            os.makedirs(name, exist_ok=True) # make new directory based on the imputted name
            os.chdir(name) # change working directory to the new new directory
            print("you are now working in the new directory", name)
            return
        elif directory == 'n':
            print("Okay no directory will be created and any output files will be created in your present directory.\n")
            return
        else:
            print("\nInvalid input. \nPlease enter 'y' or 'n'.\n")


# function to make sure taxonID input is an integer
def check_integer(input_variable):
    try:
        int(input_variable)
        return True
    except ValueError:
        print("The input is not an integer. Please check your input and try again.\n")
        return False


# function that asks the user for an input until they give an integer response
def get_taxonID():
    while True:
        user_input = input("Please insert the NCBI taxon ID number for the taxon of interest:\n")
        if check_integer(user_input):
            return int(user_input)


# function that checks the NCBI database to check the taxon exists and  asks the user to make sure they got the species that they wanted
def tax_name():
    while True:
        taxonID = get_taxonID()
        print("You have entered:", taxonID)
        # get the taxon name from the taxon ID from the NCBI taxonomy database
        taxon_name = subprocess.getoutput("esearch -db taxonomy -query '" + str(taxonID) +  " [uid]' | efetch")
        # checking the user is happy with the input
        if taxon_name:
            print("Taxon name: ", taxon_name)
            user_input = input("\nIs this the correct species? (y/n): ").lower()
            if user_input == 'y':
                print("\nGreat! Moving on.")
                return taxon_name,taxonID
            elif user_input == 'n': # if they are not happy, then they get the chance to enter a new taxon ID
                print("\nPlease try entering the taxon ID of interest again.\n")
            else:
                print("\nInvalid input. \nPlease enter 'y' or 'n'.\n")
        else:
            print("\nSpecies not found. \nPlease enter a valid Taxon ID.\n")
        continue


# function that checks the inputted protein exists
def protein_check():
    while True:
        try:
            # defining the protein name of interest
            protein = input("Please specify the name of the protein family of interest:\n")
            # checking that the protein exists by seeing if there are results fetched from the NCBI library, counting the number of lines and saving this number as the variable prot_check
            prot_check = int(subprocess.getoutput("esearch -db protein -query '" + protein +  " [PROT] NOT PARTIAL' | efetch -format uid | wc -l"))
            # checking there is at least 1 row in file
            if prot_check > 0:
                print("Great,", prot_check, "sequences were found for" , protein, "in the NCBI database.\n")
                return protein
            else:
                print("\nThere were no results for that protein in the NCBI database. Please make sure you entered your protein name correctly.\n")
        except Exception as e:
            print("An error occurred: ",e)
            print("Please check your input and try again.\n")


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
            print("\nYour query of", protein, "and taxon ID", taxonID, " resulted in", line_count, "protein sequences.")
            return line_count
        else:
            q = input("\nYour query resulted in over 1000 protein sequences. That is quite a few sequences, are you sure you would like to carry on with these parameters? (y/n)\n").lower()
            if q == 'y':
                print("Okay, if youre sure.\n")
                return
            elif q == 'n':
                print("\nOkay, press 'control+D' on your keyboard to escape from the script and rerun the script with a new input taxon ID and/or protein\n")
            else:
                print("\nInvalid input. \nPlease enter 'y' or 'n'.\n")


# function that aligns the protein sequences, plots a conservation plot based on the sequences, and output the graph to the screen
def plot_seq():
    # using clustalo to align the sequences and convert the output to .msf
    if line_count == 1:
        print("Skipping sequence alignment as there is only one sequence\n")
    else:
        subprocess.call("clustalo -i " + query_name + ".fasta -o protein_alignment_" + query_name + ".msf --outfmt msf --threads 200 --force", shell = True )
        print("Protein alignment completed successfully!\n")
    print("Creating conservation graphs, please wait...\n")
    # plotting the conservation plot of all the sequences that were retrieved from the NCBI database and saving it as a png
    subprocess.call("plotcon -sequences protein_alignment_" + query_name + ".msf -winsize 4 -graph png -stdout > "+ query_name + "_plotcon.png", shell = True)
    # bringing the conservation plot to the screen
    subprocess.call("eog "+query_name+ "_plotcon.png", shell = True)


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
                output_filename = f"sequences/{accn}.fasta"
                with open(output_filename, 'w') as output_file:
                    output_file.write(f">{section}")
                print(f"Created file: {output_filename}")
                break
        else:
            print(f"No match found for {identifier}")


# function that runs pepstats
def run_pepstats():
    while True:
        # ask the user if they want to run pepstats
        run_pepstats_response = input("Would you like to run pepstats (this gives varions statistics about the protein sequences) (y/n): \t").lower()
        if run_pepstats_response == 'y':
            # asking the user if they want individual sequence files
            individual_files = input("\nDo you want individual sequence statistics files? (y/n): \nAnswering no will result in the sequence statistics being saved in the same file\n").lower()
            # modifing the command based on user's choice
            if individual_files == 'y':
                os.makedirs("protein_stats", exist_ok=True)
                # loop through every file in the sequences folder
                for filename in os.listdir("sequences"):
                    file_path = os.path.join("sequences", filename)
                    print(f"Processing file: {filename}")
                    # run pepstats for each individual sequence file
                    subprocess.call("pepstats -sequence " + file_path + " -outfile protein_stats/" + filename + "_seq_stats.txt -auto Yes", shell = True)
                print("\nThe pepstats output files were saved in a directory called 'protein_stats'.\n")
                break # exit the loop
            # if they chose no, the protein sequence statistics will all be outputted in one file
            elif individual_files == 'n':
                subprocess.call("pepstats -sequence " + query_name + ".fasta -outfile " + query_name + "_seq_stats.txt", shell = True)
                print("pepstats executed successfully.\n")
                break
            else:
                print("Invalid response. Please enter 'y' or 'n'. Try again.")
        # if they don't want to run pepstats, it will be skipped
        elif run_pepstats_response == 'n':
            print("Okay. Skipping pepstats.")
            break
        else:
            print("Invalid response. Please enter 'y' or 'n'. Try again.")


### End of function definition

print("Ready to begin")

# asking the user if they would like to create a directory for the output files
dir()

# defining taxon name and taxonID as the outputs from the tax_name function
taxon_name, taxonID = tax_name()
# defining the protein
protein = protein_check()
# checking if there is a space in the protein name and if there is, changing it to a dash
if ' ' in protein:
    protein = protein.replace(' ', '-')
# checking the number of sequences for the query
line_count = seq_count()

# retrieving the sequences for the defined taxon and protein family
#defining the query name
query_name = protein + "_txid" + str(taxonID)
# getting the fasta sequences from the NCBI database from the query name
subprocess.getoutput("esearch -db protein -query '" + protein + " [PROT] AND txid" + str(taxonID) + " [Organism:exp] NOT (predicted OR hypothetical)' | efetch -format fasta > " + query_name + ".fasta")

#plotting conservation plot
plot_seq()

# making a directory for the the individual to go into
os.makedirs("sequences", exist_ok=True)
print("Separating fasta file into individual sequences") 

# splititng the fasta file into individual sequence files
split_seq(query_name+".fasta", "accn.txt")

# making a directory for the patmatmotifs output files to go into
os.makedirs("motifs", exist_ok=True)

# run the PROSITE motif search
with open("accn.txt", 'r') as accn_file:
    for accn in accn_file:
        accn = accn.strip()
        # use patmatmotifs to search for motifs in the chosen sequence file
        subprocess.call("patmatmotifs -sequence sequences/" + accn + ".fasta -outfile motifs/" + accn + "_res.patmatmotifs -full -auto Yes", shell = True)

# creating an output file for the sequences with motif hits
output_file = 'motifs_hit.txt'
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
                    # checking if the line does not have a hit count of 0, if it doesn't the file name gets added to the new file called motif_hits.txt
                    if line.startswith('# HitCount:') and not line.startswith('# HitCount: 0'):
                        # If the condition is met, write the filename to the output file
                        output.write(filename + '\n')
                        break  # break out of the loop once a match is found

# printing a message indicating the process is complete
print("Files with motif hits written to:", output_file)
with open("motifs_hit.txt", 'r') as hits:
    x = len(hits.readlines())
    print('Number of files that have one or more motif hits:', x)

## ADDITIONAL ANALYSIS
# pepstats analysis
run_pepstats()

print("Thank you! You have reached the end of this programme :)")
