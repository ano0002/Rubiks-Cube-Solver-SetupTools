import pickle
import json

with open(r"GenerateDB\cornerDict.json", "r") as f:
    dicta = json.loads(f.read())

with open(r"cornerDB.pickle", "wb") as f:
    pickle.dump(dicta, f, protocol=pickle.HIGHEST_PROTOCOL)

with open(r"cornerDB.pickle", "rb") as f:
    dictb = pickle.load(f)

print(dicta == dictb)