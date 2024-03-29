import json
import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/mytest2')
def index():
    return 'Server Works', 200

@app.route('/mytest', methods=["POST"])
def find_matching_sequences():
    mystring = (request.json)["searchString"]
    strings = 'http://13.251.5.125/exactapi/tagmeta?filter={"where":{"equipment":"Unassigned","description":{"neq":"Unassigned"}},"fields":["id","description","dataTagId"],"limit":500}'
    response = requests.get(strings).json()

    matching_strings = []
    for item in response:
        if mystring in item["description"]:
            similarity = jaccard_similarity(mystring, item["description"])
            matching_strings.append((item, similarity))

    return json.dumps(matching_strings), 200

def jaccard_similarity(string1, string2):
    intersection_cardinality = len(set.intersection(*[set(string1), set(string2)]))
    union_cardinality = len(set.union(*[set(string1), set(string2)]))
    similarity = intersection_cardinality / float(union_cardinality)
    return similarity

app.run(port=5000,debug=True)