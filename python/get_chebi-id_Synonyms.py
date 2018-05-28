import argparse
import gzip
import  datetime
# coding: utf-8

parser = argparse.ArgumentParser()
parser.add_argument("--file", help="read file")
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
write_data = ""
write_list = []
filename = args.file
today = datetime.date.today()
filename += "_id-to-synonyms-from-sdf_"+ str(today) + "_result.txt"
f = open(filename, "a", encoding="utf-8")
f.write('CHEBI\tprefLabel\taltLabel\n')
f.flush()
f.close()

for line in sdf_data:
    
    # ChEBI ID
    if "<ChEBI ID>" in line:
        chebi_id_bool = True
    if chebi_id_bool == True:
        if "<ChEBI ID>" in line:
            print (line, end='')
        else:
            if '\n' is line:   
                chebi_id_bool = False
            else:
                #print (line, end='')
                cwork=line.replace("\n", "")
                write_data += cwork + "\t"
    
    # <ChEBI Name>
    if "<ChEBI Name>" in line:
        chebi_name_bool = True
    if chebi_name_bool == True:
        if "<ChEBI Name>" in line:
            print (line, end='')
        else:
            if '\n' is line:   
                chebi_name_bool = False
            else:
                #print (line, end='')
                nwork=line.replace("\n", "")
                write_data += nwork + "\t"
    
    # <IUPAC Names>
    if "<IUPAC Names>" in line:
        chebi_iupac_bool = True
    if chebi_iupac_bool == True:
        if "<IUPAC Names>" in line:
            print (line, end='')
        else:
            if '\n' is line:   
                chebi_iupac_bool = False
            else:
                #print (line, end='')
                iwork=line.replace("\n", "")
                write_list.append(iwork)

    # <Synonyms>
    if "<Synonyms>" in line:
        chebi_synonyms_bool = True
    if chebi_synonyms_bool == True:
        if "<Synonyms>" in line:
            print (line, end='')
        else:
            if '\n' is line:   
                chebi_synonyms_bool = False
            else:
                #print (line, end='')
                swork=line.replace("\n", "")
                write_list.append(swork)

# $$$$
    if "$$$$" in line:
        f = open(filename, "a", encoding="utf-8")
        if len(write_list) is 0:
            linedata = write_data + "\n"
            f.write(linedata)
            print (linedata, end='')
            write_data = ""
            write_list = []
        else:
            for name in write_list:
                linedata = write_data + name + "\n"
                f.write(linedata)
                print (linedata, end='')
            write_data = ""
            write_list = []
        
        f.flush()
        f.close()

sdf_data.close()