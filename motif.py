#!/usr/bin/python3

# function to split the fasta sequence file into individual sequence files
def split_file(imput_file = "accn.txt"):
    with open(input_file, 'r') as infile:
        sequences = infile.read()
    sections = sequences.split('>') # split file by '>'
    sections = [section.strip() for section in sections if section.strip()]
    for index, section in enumerate(sections):
        # using the accession and version number to name the new output files
        output_filename =
        with open(output_filename, 'w') as outfile:
            outfile.write(f">{section}")


import subprocess

subprocess.call("/localdisk/data/BPSM/ICA2/pullseq -i" + query +  ".fasta -n " + accn )

with open("accn.txt", 'r') as accn_file:
    for accn in accn_file:
        accn = accn.strip()
        # Use pullseq to extract sequence based on accession number
        subprocess.call("/localdisk/data/BPSM/ICA2/pullseq -i" + query_name +  ".fasta -n " + accn + " -o " + accn + ".fasta", shell = True )
        # Use patmatmotif to search for motifs in the extracted sequence
        subprocess.call("patmatmotif -sequence " + accn + ".fasta -outfile " + accn + "_motif_results.out")
        # You can add additional processing steps or print statements here if needed
        print(f"Motif search for {accn} completed.")

