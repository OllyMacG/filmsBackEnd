import json
import requests

input_file = open ('1001movies.json')
json_array = json.load(input_file)
store_list = []

for item in json_array:
    response = requests.post("http://omcg.ml/api/movies", json={"name": item['name'], "year": item['year']})

    
