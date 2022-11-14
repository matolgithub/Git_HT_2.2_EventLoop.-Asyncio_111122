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
    def get_dict_persons(self):
        dict_persons = {}
        response = requests.get(url=self.url)
        total_quant_persons = response.json()["count"]
        start_time = datetime.datetime.now()
        item = 1

        while len(dict_persons) < total_quant_persons:
            dict_items = {}
            url = f"{self.url}/{item}"
            response = requests.get(url=url).json()

            for key, value in response.items():
                if value != "Not found":
                    if key != "created" and key != "edited":
                        if key == "films":
                            films_string = ""
                            for film_link in value:
                                film_response = requests.get(url=film_link).json()["title"]
                                films_string += f"{film_response}, "
                                dict_items[key] = films_string[:-2]
                        elif key == "species" or key == "starships" or key == "vehicles":
                            string = ""
                            for link in value:
                                response = requests.get(url=link).json()["name"]
                                string += f"{response}, "
                                dict_items[key] = string[:-2]
                        else:
                            dict_items[key] = value
                    dict_persons[int(f"{item}")] = dict_items
            item += 1

        pprint(dict_persons)
        total_time = datetime.datetime.now() - start_time
        print(total_time)

        return dict_persons


# with requests: 3 pers. - 8sec., 82 pers. - 1min. 58sec.
if __name__ == "__main__":
    swapi_obj = Swapi()
    swapi_obj.get_dict_persons()
