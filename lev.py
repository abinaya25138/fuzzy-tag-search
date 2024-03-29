from flask import Flask,request
import Levenshtein
import json
import requests
app = Flask(__name__)
@app.route('/mytest2')
def index():
  return 'Server Works',200


@app.route('/mytest',methods=["POST"])
@app.route('/mytest',methods=["POST"])
def find_matching_sequences():
    mystring = (request.json)["searchString"]
    strings = 'http://13.251.5.125/exactapi/tagmeta?filter={"where":{"equipment":"Unassigned","description":{"neq":"Unassigned"}},"fields":["id","description","dataTagId"],"limit":500}'
    response = requests.get(strings).json()

    matching_strings = []
    for item in response:
        if mystring in item["description"]:
            distance = Levenshtein.distance(mystring, item["description"])
            matching_strings.append((item, distance))
            # THIS CODE BELOW IS JACCARD SIMILARITY
            #def jaccard_similarity(mystring, item["description"]):
                #intersection_cardinality = len(set.intersection(*[set(mystring), set(item["description]")]))
                #union_cardinality = len(set.union(*[set(mystring), set(item["description"])]))
                #p= intersection_cardinality/float(union_cardinality)
                #matching_strings.append((p))
                #return p

            print(matching_strings)
    return json.dumps(matching_strings),200


    
    


  #mystring= (request.json)
 
     #descriptions = []
    
     


    #for item in data2:
        #descriptions.append(item["description"])

    
    #print(descriptions)
    
    #matching_strings = []

    
#for value in data2.values():
    #if mystring in value:
           
            #distance = Levenshtein.distance(mystring, data2)
            
            #matching_strings.append((data2, distance))


        
      

    #print(matching_strings)
    #return json.dumps(matching_strings),200

app.run(port=5000,debug=True)




