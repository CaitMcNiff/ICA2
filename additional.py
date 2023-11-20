#!/bin/python3

import subprocess
mport os


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
                    # make sure the item is a file (not a subdirectory)
                    print(f"Processing file: {filename}")
                    subprocess.call("pepstats -sequence " + file_path + " -outfile protein_stats/" + filename + "_seq_stats.txt -auto Yes", shell = True)
                print("\nThe pepstats output files were saved in a directory called 'protein_stats'")
                break
            elif individual_files == 'n':
                subprocess.call("pepstats -sequence " + query_name + ".fasta -outfile " + query_name + "_seq_stats.txt", shell = True)
                print("pepstats executed successfully.")
                break  # exit the loop
            else:
                print("Invalid response. Please enter 'y' or 'n'. Try again.")
        elif run_pepstats_response == 'n':
            print("Okay. Skipping pepstats.")
            break  # exit the loop
        else:
            print("Invalid response. Please enter 'y' or 'n'. Try again.")



