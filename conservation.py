#!/usr/bin/python3


# retrieving the sequences for the defined taxon and protein family
query_name = protein + "_txid" + str(taxonID)

subprocess.getoutput("esearch -db protein -query '" + protein + " [PROT] AND txid" + str(taxonID) + " [Organism:exp] NOT (predicted OR hypothetical)' | efetch -format fasta > " + query_name + ".fasta")

def plot_seq():
    print("Creating conservation graphs, please wait.")
    subprocess.call("clustalo -i " + query_name + ".fasta -o protein_alignment_" + query_name + ".msf --outfmt msf --threads 200 --force", shell = True )
    subprocess.call("plotcon -sequences protein_alignment_" + query_name + ".msf -winsize 4 -graph png -goutfile plotcon", shell =True)
    subprocess.call("gio open plotcon.1.png", shell = True)
