#!/usr/bin/python3


# retrieving the sequences for the defined taxon and protein family
subprocess.getoutput("esearch -db protein -query '" + protein + " [PROT] AND txid" + str(taxonID) + " [ORGN] NOT (predicted OR hypothetical)' | efetch -format fasta > ", protein + str(taxonID),".fasta")




