import json
def process_file(path):
    file = open(path, 'r')
    lines = file.readlines()
    #new_file.write('{"data":[\n')
    for line in tqdm(lines):
        try:
            json.loads(line)
        except:
            print(line)



process_file(sys.argv[1])