
import requests
import json

data = [[1, i] for i in range(35)]
r = requests.post('http://localhost:8000', data={'data' : json.dumps(data)})
print r.status_code
print r.text