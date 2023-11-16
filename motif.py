#!/usr/bin/python3

# function to split the fasta sequence file into individual sequence files
def split_file(input_file):
    with open(input_file, 'r') as infile:
        sequences = infile.read()
    sections = sequences.split('>') # split file by '>'
    sections = [section.strip() for section in sections if section.strip()]
    for index, section in enumerate(sections):
        # using the accession and version number to name the new output files
        output_filename = 
        with open(output_filename, 'w') as outfile:
            outfile.write(f">{section}")


