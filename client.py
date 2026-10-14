"""
Minimal client for exercising any of the three search services
(jaccard.py, lev.py, whooshy.py) — they all expose the same
POST /mytest contract.
"""
import requests

url = "http://127.0.0.1:5000/mytest"

data = {"searchString": "CNDR"}

response = requests.post(url, json=data)

print(response.status_code)
print(response.text)
