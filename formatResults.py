import json


document = []

with open("results.json", "r") as infile:
    document = json.loads(infile.read())

newDocument = []

# get only type logs
for doc in document:
    newDocument.append(doc['typeLog'])

document = newDocument.copy()
newDocument = []

# get only hasCorrectInput in type logs
for doc in document:
    newDocument.append(list(filter(lambda x: x['hasCorrectInput'] == True, doc)))
    
json_object = json.dumps(newDocument, indent=4)

#print(json_object)
with open("formatted_results.json", "w") as outfile:
    outfile.write(json_object)
