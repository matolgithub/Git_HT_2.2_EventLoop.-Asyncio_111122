import requests
from pprint import pprint
import datetime
import math


class Swapi:
    def __init__(self, url="https://swapi.dev/api/people"):
        self.url = url

    # create list of Star Wars persons
    def get_list_persons(self):
        list_names_persons = []
        response = requests.get(url=self.url)
        pprint(response.json())
        start_time = datetime.datetime.now()
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

        return list_names_persons

    # create dictionary of Star Wars persons
    # def get_dict_persons(self):
    #     dict_persons = {}
    #     start_time = datetime.datetime.now()
    #     for item in range(1, total_quant_persons + 1):
    #         url = f"{url}/{item}"
    #         response = requests.get
    #
    #     total_time = datetime.datetime.now() - start_time


if __name__ == "__main__":
    swapi_obj = Swapi()
    swapi_obj.get_list_persons()
