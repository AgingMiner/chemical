import argparse
import gzip
# coding: utf-8

parser = argparse.ArgumentParser()
parser.add_argument("--file",
                    help="read file")
args = parser.parse_args()
if args.file:
    print("args.file is defined. file = " , args.file)
else:
    print("args.file is undefined.")

sdf_data =  gzip.open(args.file, "rt")

chebi_id_bool = False
chebi_name_bool = False
chebi_iupac_bool = False
chebi_synonyms_bool = False
write_list = []
filename = args.file
filename += "_result.txt"
f = open(filename, "a", encoding="utf-8")
for line in sdf_data:
    write_data = ""
    # ChEBI ID
    if "<ChEBI ID>" in line:
        chebi_id_bool = True
    if chebi_id_bool == True:
        #chebi_id_bool = False
        if "CHEBI:" in line:
            print (line, end='')
            cwork=line.replace("\n", "")
            write_data += cwork + "\t"
            chebi_id_bool = False
    # <ChEBI Name>
    if "<ChEBI Name>" in line:
        chebi_name_bool = True
    if chebi_name_bool == True:
        if '\n' is not line:
            print (line, end='')
            nwork=line.replace("\n", "")
            write_data += nwork + "\t"
        if '\n' is line:   
            chebi_name_bool = False
    
    # <IUPAC Names>
    if "<IUPAC Names>" in line:
        chebi_iupac_bool = True
    if chebi_iupac_bool == True:
        if '\n' is not line:
            print (line, end='')
            iwork=line.replace("\n", "")
            write_list.append(iwork)
        if '\n' is line:   
            chebi_iupac_bool = False

    # <Synonyms>
    if "<Synonyms>" in line:
        chebi_synonyms_bool = True
    if chebi_synonyms_bool == True:
        if '\n' is not line:
            print (line, end='')
            swork=line.replace("\n", "")
            write_list.append(swork)
        if '\n' is line:   
            chebi_synonyms_bool = False

    if "$$$$" in line:
        if len(write_list) is not 0:
            for name in write_list:
                f.write(write_data + name + "\n")
                f.flush()
        if len(write_list) is 0:
            f.write(write_data + "\n")
            f.flush()

f.close()
sdf_data.close()