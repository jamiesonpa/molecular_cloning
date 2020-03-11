import math as maths
import json
import os

#This tool requires that you run this python script in the same path as the restriction enzyme json file and a .txt file containing
#The CDS of the gene you would like to clone. This is meant for eukaryotic genes.

#NOTE: Change the path strings below!

#Work in progress 3_11_2020

def check_start(coding_sequence):
    if coding_sequence[0:3].strip() == "ATG":
        print("Start codon identified")
        return True
    else:
        check_start = input("No start codon was identified in this CDS. Are you certain this is correct? (y/n): ")
        if check_start == "y":
            return True
        else:
            return False

def check_stop(coding_sequence):
    TAA = True
    TAG = True
    TGA = True
    cds_len = len(coding_sequence)
    if coding_sequence[cds_len-4:cds_len-1].strip() != "TAA":
        print("TAA not found")
        TAA = False
    else:
        TAA = True
    if coding_sequence[cds_len-4:cds_len-1].strip() != "TAG":
        print("TAG not found")
        TAG = False  
    else:
        TAG = True
    if coding_sequence[cds_len-4:cds_len-1].strip() != "TGA":
        print("TGA not found")
        TGA = False
    else:
        TGA = True

    if TGA == False and TAA == False and TAG == False:
        check_stop = input("No stop codon was identified in this CDS. Did you already remove it/not include it intentionally? (y/n): ")
        if check_stop == "y":
            return True
        else:
            return False
    else:
        remove_stop = input("Stop codon identified. Remove it? (y/n): ")
        if remove_stop == "y":
            coding_sequence = coding_sequence[0:cds_len-3]
            return True
        else:
            return True

def check_5p_cutter():
    enzyme_5p = input("Which restriction enzymes do you intend to use on the 5' end of this amplicon? case sensitive (BamHI, EcoRI, KpnI, SmaI, StuI, XbaI, SpeI, NcoI): ")
    if enzyme_5p in restriction_enzymes:
        print("restriction enzyme " + enzyme_5p + " found.")
        cut_site = enzyme_data[enzyme_5p]
    else:
        print("Error: restriction enzyme not found in list.")
        exit()
    if cut_site in coding_sequence:
        print("Error: provided coding sequence contains a " + enzyme_5p + "cutsite, making it unsuitable for this cloning operation. Reconsider your strategy, then try again")
    else: 
        print(enzyme_5p + " chosen as 5' cutter.")
        return (enzyme_5p, cut_site)

def check_3p_cutter(enzyme_5p):
    enzyme_3p = input("Which restriction enzymes do you intend to use on the 3' end of this amplicon? case sensitive (BamHI, EcoRI, KpnI, SmaI, StuI, XbaI, SpeI, NcoI): ")
    if enzyme_3p == enzyme_5p:
        print("Error: you can't clone using two of the same enzyme on the five and three prime ends")
        exit()
    else:
        if enzyme_3p in restriction_enzymes:
            print("restriction enzyme " + enzyme_3p + " found.")
            cut_site = enzyme_data[enzyme_3p]
        else:
            print("Error: restriction enzyme not found in list.")
            exit()
        if cut_site in coding_sequence:
            print("Error: provided coding sequence contains a " + enzyme_3p + "cutsite, making it unsuitable for this cloning operation. Reconsider your strategy, then try again")
        else: 
            print(enzyme_3p + " chosen as 5' cutter.")
            return (enzyme_3p, cut_site)

cds_file = open("C:\\path\\to\\your\\restriction_enzymes.json","r") #CHANGE THIS FOR YOUR PATH
coding_sequence = cds_file.read()
coding_sequence.upper()

if check_start(coding_sequence) == False:
    print("Input sequence error")
    exit()
else:
    pass

if check_stop(coding_sequence) == False:
    print("Input sequence error")
    exit()
else:
    pass

restriction_enzymes = []
with open("C:\\path\\to\\your\\restriction_enzymes.json", "r") as jsonfile: #CHANGE THIS FOR YOUR PATH
    enzyme_data = json.load(jsonfile)
    for entry in enzyme_data:
        restriction_enzymes.append(entry)

fiveprimecutter = check_5p_cutter()
threeprimecutter = check_3p_cutter(fiveprimecutter[0])


#notes for primers
#DO NOT HAVE 3 of more G or C bases at 3' end
#DO NOT HAVE a 3' thymidine, since it is more prone to mispriming than the other nucleotides.
#Optimal length = 18-30BP
#Melting Temp Over 60C
#Melting Temp within 4C for each primer
#GC content between 40 and 60%
