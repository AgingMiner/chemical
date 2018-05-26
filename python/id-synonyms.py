import json
import requests
import urllib
import argparse
import urllib.parse
import sys
import types
import  datetime

parser = argparse.ArgumentParser()
parser.add_argument("--file",
                    help="read file")
args = parser.parse_args()
if args.file:
    print("args.file is defined. file = " , args.file)
else:
    print("args.file is undefined.")

idlist =  open(args.file, "rt")


filename = args.file
today = datetime.date.today()
filename += "_synomyms_"+ str(today) + "_result.txt"
f = open(filename, "a", encoding="utf-8")
f.write('CHEBI\tprefLabel\taltLabel\n')

for localid in idlist:

    try:
        #chebiid = urllib.parse.urlparse('CHEBI%3A41308')
        #chebiid = urllib.parse.quote('CHEBI:41308')
        text = localid.replace('\n','')
        text = text.replace('\r','')

        chebiid = urllib.parse.quote(text)
        print(localid)
        print(chebiid)
        #url = 'https://sparqlist.glyconavi.org/api/ChEBI_Synonyms?id=CHEBI%3A41308'
        url = "https://sparqlist.glyconavi.org/api/ChEBI_Synonyms?id=" + chebiid

        r = requests.get(url)

        json_obj = r.json()
        #print(json_obj)
        line = ""
        data = ""
        #print("ID:" + json_obj['id'])
        #line = json_obj['id'] + '\t'
        # type(x) is types.NoneType
        #if type(json_obj) is not types.NoneType:

        #if json_obj['id'] is not None:
        if 'id' in json_obj:
            line = json_obj['id'] + '\t'
            #print("prefLabel:" + json_obj['prefLabel'])
            #if json_obj['prefLabel'] is not None:
            if 'prefLabel' in json_obj:
                line += json_obj['prefLabel'] + '\t'
                #if json_obj['altLabel'] is not None:
                if 'altLabel' in json_obj:
                    altlabel = json_obj['altLabel']

                    if len(altlabel) > 0:
                        for name in altlabel:
                            #print("altLabel:" + name)
                            data = line + name + '\t'
                            print(data)
                            f.write(data + '\n')
                    else:
                        print(line)
                        f.write(line + '\n')


    except OSError as err:
        print("OS error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

f.flush()
f.close()
idlist.close()