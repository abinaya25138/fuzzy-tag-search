"""
Flask microservice that finds tag descriptions matching a search string
using Jaccard similarity (character-set overlap).

Originally built against an internal company API during an internship;
the endpoint below has been redacted/genericized for public sharing.
Set TAG_API_URL to point at your own data source.
"""
import json
import os

import requests
from flask import Flask, request

app = Flask(__name__)

TAG_API_URL = os.environ.get(
    "TAG_API_URL",
    "http://<your-api-host>/api/tagmeta?filter={\"where\":{\"equipment\":\"Unassigned\"}}",
)


@app.route("/mytest2")
def index():
    return "Server Works", 200


@app.route("/mytest", methods=["POST"])
def find_matching_sequences():
    mystring = request.json["searchString"]
    response = requests.get(TAG_API_URL).json()

    matching_strings = []
    for item in response:
        if mystring in item["description"]:
            similarity = jaccard_similarity(mystring, item["description"])
            matching_strings.append((item, similarity))

    return json.dumps(matching_strings), 200


def jaccard_similarity(string1, string2):
    intersection_cardinality = len(set.intersection(*[set(string1), set(string2)]))
    union_cardinality = len(set.union(*[set(string1), set(string2)]))
    return intersection_cardinality / float(union_cardinality)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
