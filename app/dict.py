import json

def returnDef(inputword):
  dict = open('dictionary/dictionary.json')
  dictdata = json.load(dict)
  for key, value in dictdata.items():
    if key == inputword:
      return key.encode('utf-8') + ": " + value.encode('utf-8')
