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

chebibool = False
for line in sdf_data:
    if "ChEBI ID" in line:
        chebibool = True
    if chebibool == True:
        #chebibool = False
        if "CHEBI:" in line:
            print (line, end='')
            filename = args.file
            filename += "_result.txt"
            f = open(filename, "a", encoding="utf-8")
            f.write(line)
            f.flush()
            f.close()
            chebibool = False

sdf_data.close()