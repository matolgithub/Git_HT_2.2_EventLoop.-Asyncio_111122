import requests
from pprint import pprint
import datetime
import math

url = "https://swapi.dev/api/people"
list_names_persons = []
start_time = datetime.datetime.now()

response = requests.get(url=url)

total_quant_persons = response.json()["count"]
total_num_pages = math.ceil(total_quant_persons / 10)

for num_page in range(1, total_num_pages + 1):
    if num_page > 1:
        url = f"https://swapi.dev/api/people/?page={num_page}"
        response = requests.get(url=url)
    list_persons = [item for item in response.json()["results"]]
    for item in list_persons:
        for key, value in item.items():
            if key == "name":
                list_names_persons.append(value)

total_time = datetime.datetime.now() - start_time

print(f"Executed time: {total_time}\nTotal persons: {total_quant_persons}\nIncluding in list persons:"
      f" {len(list_names_persons)}\nList of persons: {sorted(list_names_persons)}")

# pprint(response.json())
# print(response.status_code)
# pprint(response.text)
