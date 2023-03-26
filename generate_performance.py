import json

characters = "abcdefghijklmnopqrstuvwxyz"


char_time = {(i, j):[] for i in characters for j in characters}

documents = []

with open("formatted_results.json", "r") as infile:
    documents = json.loads(infile.read())


for doc in documents: 
    for i in range(0, len(doc) - 1):
        firstLetter = doc[i]['actualChar'].lower()
        secondLetter = doc[i + 1]['actualChar'].lower()
        difference = doc[i+1]['timestamp'] - doc[i]['timestamp']
        retVal = char_time.get((firstLetter, secondLetter))
        if retVal is not None:
            char_time[(firstLetter, secondLetter)].append(difference)


new_char_time = {}
# sum 
for key in char_time:
    #print(key)
    number_of_entries = len(char_time[key])
    sum_of_entries = sum(char_time[key])

    if number_of_entries == 0:
        new_char_time[key] =  0
    else:
        new_char_time[key] = sum_of_entries / number_of_entries



factor=1.0/sum(new_char_time.values())
normalised_d = {k: v*factor for k, v in new_char_time.items() }

#print(normalised_d)


json_serializable = {}


for key in normalised_d:
    json_serializable["{}{}".format(key[0], key[1])] = normalised_d[key]

json_object = json.dumps(json_serializable, indent=4)

#print(json_object)
with open("new_performance.json", "w") as outfile:
    outfile.write(json_object)