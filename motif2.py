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

# run the PROSITE motif search 
with open("accn.txt", 'r') as accn_file:
    for accn in accn_file:
        accn = accn.strip()
        # Use patmatmotifs to search for motifs in the chosen sequence file
        subprocess.call("patmatmotifs -sequence " + accn + ".fasta -outfile " + accn + "_res.patmatmotifs -full -auto Yes", shell = True)
        # You can add additional processing steps or print statements here if needed
        print(f"Motif search for {accn} completed.")



