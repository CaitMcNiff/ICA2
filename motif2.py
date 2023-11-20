#!/bin/python3

import os 
import subprocess

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

split_seq("glucose-6-phosphatase_txid8782.fasta", "accn.txt")

# making a directory for the patmatmotifs output files to go into
os.makedirs("motifs", exist_ok=True)

# run the PROSITE motif search using patmatmotifs
with open("accn.txt", 'r') as accn_file:
    for accn in accn_file:
        accn = accn.strip()
        # Use patmatmotifs to search for motifs in the chosen sequence file
        subprocess.call("patmatmotifs -sequence " + accn + ".fasta -outfile motifs/" + accn + "_res.patmatmotifs -full -auto Yes", shell = True)
        # You can add additional processing steps or print statements here if needed
        print(f"Motif search for {accn} completed.")

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

