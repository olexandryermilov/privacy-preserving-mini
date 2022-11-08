import transformers

import sys
from tqdm import tqdm
import json
import numpy as np

import spacy
from transformers import pipeline

NER = spacy.load("en_core_web_sm")
#DE_NER = spacy.load("de_core_news_sm")
mask_predictor = pipeline('fill-mask')

entity_map = dict()
placeholders_map = dict()
placeholder_to_word_map = dict()

total = 0

def choose_word(original, predictions):
    for word in predictions:
        try:
            word_lemma = NER(word['token_str'].strip())[0].lemma_.lower()
        except:
            continue
        original_lemma = original.lemma_.lower()
        if word_lemma != original_lemma:
            return word['token_str']
    return original.text

def bert_mask_replacement(corpus, f, ner):
  processed = ner(corpus)
  res = []
  result = 0
  for sentence in processed.sents:
      for entity in sentence:
          if entity.ent_type_:
              result += 1
              entity_word = entity.text
              entity_type = entity.ent_type_
              sentence_with_mask = " ".join([t.text if not entity == t else '<mask>' for t in sentence])

              if entity_type not in entity_map:
                  entity_map[entity_type] = dict()
              if entity_word in entity_map[entity_type]:
                  replacement = entity_map[entity_type][entity_word]
              else:
                  predictions = mask_predictor(sentence_with_mask)
                  replacement = choose_word(entity, predictions)
                  entity_map[entity_type][entity_word] = replacement

              res.append(replacement)
          else:
              res.append(entity.text)
  write(f, " ".join(res))
  return result


def readPlaceholderMap():
    with open("placeholders_spacy.json", "r") as file:
        entities = dict()
        data = json.load(file)
        for k in tqdm(data):
            splitted = data[k].split("_")
            entity = "_".join(splitted[0:-1])
            num = int(splitted[-1])
            if entity in entities:
                entities[entity] = max(entities[entity], num)
            else:
                entities[entity] = num
        return data, entities

def readFile(filePath):
  f = open(filePath, "r")
  return f.read()

def writeFileCSV(filePath, content):
    f = open(filePath, "w")
    f.write("text,summary\n")
    for e in content:
        f.write(e[0] + ',' + e[1] + "\n")
    f.close()

def invertMap(map):
    nv_map = {v: k for k, v in map.items()}
    return nv_map

def write(f, text):
    f.write(text)
    return

def writeFileJSONAnon(filePath, content, anonFunc, task):
    f = open(filePath, "a")
    #f.write('{"data":[')
    f.close()
    result = 0
    if task == "summarization":
        ner_source = NER
        ner_target = NER
    elif task == "translation":
        ner_source = NER
        ner_target = DE_NER
    else:
        ner_source = NER
        ner_target = NER

    for e in tqdm(content[:-1]):
        f = open(filePath, "a")
        f.write('{"text": "')
        result += anonFunc(e[0].replace('"', '').replace('\\','').replace('\t',''), f, ner_source)
        f.write('","summary": "')
        result += anonFunc(e[1].replace('"', '').replace('\\','').replace('\t',''), f, ner_target)
        f.write('"},\n')
        f.close()
    f = open(filePath, "a")
    for e in content[-1:]:
        f = open(filePath, "a")
        f.write('{"text": "')
        anonFunc(e[0].replace('"', '').replace('\\', '').replace('\t', ''), f, ner_source)
        f.write('","summary": "')
        anonFunc(e[1].replace('"', '').replace('\\', '').replace('\t', ''), f, ner_target)
        f.write('"}\n')

    #f.write(']}')
    f.close()
    with open("../all_ners.txt", "w") as f1:
        f1.write(str(result/len(content)))


def writeFileJSON(filePath, content):
    f = open(filePath, "w")
    #f.write('{"data":[')
    for e in tqdm(content[:-1]):
        f.write('{"text": "' + e[0].replace('"', '').replace('\\','').replace('\t','') + '","summary": "' + e[1].replace('"', '').replace('\\','').replace('\t','') + '"}\n')
    for e in content[-1:]:
        f.write(
            '{"text": "' + e[0].replace('"', '').replace('\\', '').replace('\t', '') + '","summary": "' + e[1].replace(
                '"', '').replace('\\', '').replace('\t', '') + '"}\n')

    #f.write(']}')
    f.close()

def processFile(filePath, anonymize, methodFunc, methodName, task, name):
    if task == 'summarization':
        source = readFile(filePath+'.source').split("\n")
        target = readFile(filePath+'.target').split("\n")
    else:
        source = readFile(filePath).split("\n")
        target = readFile(filePath).split("\n")
    together = list(zip(source, target))
    if anonymize:
        writeFileJSONAnon(name+"_anonymized_spacy_"+methodName+".json", together, methodFunc, task)
    else:
        writeFileJSON(filePath.split(".")[0]+".json", together)
    return


docs = []
def main():
    print(sys.argv)
    task = sys.argv[1]
    train = sys.argv[2]
    val = sys.argv[3]
    test = sys.argv[4]
    methodName = "ner-mask"
    method = bert_mask_replacement
    processFile(train, True, method, methodName, task, 'train')
    processFile(test, True, method, methodName, task,'test')
    processFile(val, True, method, methodName, task,'val')
    with open(f'placeholders_spacy_{task}.json', 'w') as f:
        f.write(json.dumps(entity_map))
main()