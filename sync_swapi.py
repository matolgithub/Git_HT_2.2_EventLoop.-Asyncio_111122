import requests
from pprint import pprint
import datetime

url = "https://swapi.dev/api/people/"
list_names_persons = []

response = requests.get(url=url)
start_time = datetime.datetime.now()
list_persons = [item for item in response.json()["results"]]
for item in list_persons:
    for key, value in item.items():
        if key == "name":
            list_names_persons.append(value)

total_time = datetime.datetime.now() - start_time

print(f"{total_time}\n{len(list_names_persons)}\n{list_names_persons}")

# pprint(response.json())
# print(response.status_code)
# print(response.text)
