"""
Flask microservice that finds tag descriptions matching a search string
using Levenshtein (edit) distance.

Originally built against an internal company API during an internship;
the endpoint below has been redacted/genericized for public sharing.
Set TAG_API_URL to point at your own data source.
"""
import json
import os

import Levenshtein
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
            distance = Levenshtein.distance(mystring, item["description"])
            matching_strings.append((item, distance))

    return json.dumps(matching_strings), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
