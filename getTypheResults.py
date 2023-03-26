import firebase_admin
import json
from firebase_admin import firestore, credentials


cred = credentials.Certificate('./env/delutype-firebase-adminsdk-d20ew-b850f3a349.json');

app = firebase_admin.initialize_app(cred)
firestore_client = firestore.client()

collection_ref = firestore_client.collection("results").where("layout", '==', "QWERTY")

docs = collection_ref.stream()

results = []
for doc in docs:

    new_doc = doc.to_dict()
    new_doc.pop('createdTimeAt')
    new_doc.pop('updatedTimeAt')
    results.append(new_doc)

#print(results)

json_object = json.dumps(results, indent=4)


with open("results.json", "w") as outfile:
    outfile.write(json_object)