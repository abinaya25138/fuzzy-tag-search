"""
Flask microservice for fuzzy tag search, with the fixes from matching.py:
every tag is scored (no exact-substring filter), scores respect character
order and abbreviations, and results are cut at a threshold chosen from
labeled data (see choose_threshold.py).

Same contract as the earlier services: POST /mytest {"searchString": "..."}
returns a list of (tag, score) pairs, best first.

Set TAG_API_URL to your data source and MATCH_THRESHOLD to the value
choose_threshold.py reports for your labeled pairs.
"""
import json
import os

import requests
from flask import Flask, request

from matching import search

app = Flask(__name__)

TAG_API_URL = os.environ.get(
    "TAG_API_URL",
    "http://<your-api-host>/api/tagmeta?filter={\"where\":{\"equipment\":\"Unassigned\"}}",
)
MATCH_THRESHOLD = float(os.environ.get("MATCH_THRESHOLD", "0.8"))


@app.route("/mytest2")
def index():
    return "Server Works", 200


@app.route("/mytest", methods=["POST"])
def find_matching_sequences():
    query = request.json["searchString"]
    tags = requests.get(TAG_API_URL).json()
    return json.dumps(search(query, tags, MATCH_THRESHOLD)), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
