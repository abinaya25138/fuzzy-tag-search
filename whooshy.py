"""
Flask microservice that indexes tag descriptions with Whoosh and serves
full-text search over them, refreshing the index hourly.

Originally built against an internal company API during an internship;
the endpoint below has been redacted/genericized for public sharing.
Set TAG_API_URL to point at your own data source.
"""
import json
import os

import requests
import schedule
from flask import Flask, request
from whoosh.fields import ID, TEXT, Schema
from whoosh.index import create_in
from whoosh.qparser import QueryParser

app = Flask(__name__)
ix = None

TAG_API_URL = os.environ.get(
    "TAG_API_URL",
    "http://<your-api-host>/api/tagmeta?filter={\"where\":{\"equipment\":\"Unassigned\"}}",
)


@app.route("/mytest2")
def index():
    return "Server Works", 200


def create_index():
    global ix
    response = requests.get(TAG_API_URL).json()
    schema = Schema(id=ID(stored=True), description=TEXT(stored=True))
    ix = create_in("indexdir", schema)
    writer = ix.writer()
    for item in response:
        writer.add_document(id=str(item["id"]), description=item["description"])
    writer.commit()


@app.route("/mytest", methods=["POST"])
def find_matching_sequences():
    mystring = request.json["searchString"]
    with ix.searcher() as searcher:
        query = QueryParser("description", ix.schema).parse(mystring)
        results = searcher.search(query)
        matching_strings = [(r["description"], r.score) for r in results]
    return json.dumps(matching_strings), 200


if __name__ == "__main__":
    create_index()
    schedule.every(1).hour.do(create_index)
    app.run(port=5000, debug=True)
