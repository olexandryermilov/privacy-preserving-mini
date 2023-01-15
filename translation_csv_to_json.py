import json
import sys
from tqdm import tqdm

def process_file(path):
    file = open(path, 'r')
    new_file = open(path+".json", "w")
    lines = file.readlines()
    #new_file.write('{"data":[\n')
    for line in tqdm(lines):
        obj = line.split('","')
        if len(obj)<2:
            obj = line.split('",')
            if(len(obj)<2):
                obj = line.split(',"')
                if(len(obj) < 2):
                    obj = line.split(",")
        try:
            new_file.write('{"translation": {"en":"' + obj[0].replace('"', '') +'", "de":"'+ obj[1][:-1].replace('"', '')+'"}}\n')
        except:
            print(line)
            continue
    #for line in lines[-1:]:
    #    if (line[0] == '"'):
    #        obj = line.split('","')
    #        if len(obj) < 2:
    #            obj = line.split('",')
    #            if (len(obj) < 2):
    #                obj = line.split(',"')
    #    else:
    #        obj = line.split(",")

    #   new_file.write('{"translation": {"en":"' + obj[0].replace('"', '') + '", "de":"' + obj[1][:-1].replace('"', '') + '"}}\n')
    #new_file.write(']}')


process_file(sys.argv[1])