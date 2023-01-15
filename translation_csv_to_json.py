import json
import sys
from tqdm import tqdm

def process_file(path):
    file = open(path, 'r')
    new_file = open(path+".json", "w")
    lines = file.readlines()
    new_file.write('{"data":[\n')
    for line in tqdm(lines[:-1]):
        #line = line.replace('"', '')
        obj = line.split('","')
        new_file.write('{"translation": {"en":"' + obj[0].replace('"', '') +'", "de":"'+ obj[1][:-1].replace('"', '')+'"}},\n')
    for line in lines[-1:]:
        #line = line.replace('"', '')
        obj = line.split('","')

        new_file.write('{"translation": {"en":"' + obj[0].replace('"', '') + '", "de":"' + obj[1][:-1].replace('"', '') + '"}}\n')
    new_file.write(']}')


process_file(sys.argv[1])