from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
import json, requests
from flask import Flask, request
import schedule

app = Flask(__name__)
ix = None

@app.route('/mytest2')
def index():
    return 'Server Works', 200

def create_index():
    global ix
    strings = 'http://13.251.5.125/exactapi/tagmeta?filter={"where":{"equipment":"Unassigned","description":{"neq":"Unassigned"}},"fields":["id","description","dataTagId"],"limit":500}'
    response = requests.get(strings).json()
    schema = Schema(id=ID(stored=True), description=TEXT(stored=True))
    ix = create_in("indexdir", schema)
    writer = ix.writer()
    for item in response:
        writer.add_document(id=str(item['id']), description=item['description'])
    writer.commit()

@app.route('/mytest', methods=["POST"])
def find_matching_sequences():
    mystring = (request.json)["searchString"]
    with ix.searcher() as searcher:
        query = QueryParser("description", ix.schema).parse(mystring)
        results = searcher.search(query)
        matching_strings = [(result['description'], result.score) for result in results]
    return json.dumps(matching_strings), 200

if __name__ == '__main__':
    create_index()
    schedule.every(1).hour.do(create_index)
app.run(port=5000,debug=True)
