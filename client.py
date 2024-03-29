import requests
import json

url = "http://127.0.0.1:5000/mytest"

data = {
  'searchString':'CNDR'
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.text)