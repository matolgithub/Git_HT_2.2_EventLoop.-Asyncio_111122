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

        while len(dict_persons) < 3:  # change: total_quant_persons!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
                        elif key == "species":
                            species_string = ""
                            for species_link in value:
                                species_response = requests.get(url=species_link).json()["name"]
                                species_string += f"{species_response}, "
                                dict_items[key] = species_string[:-2]
                        elif key == "starships":
                            starships_string = ""
                            for starships_link in value:
                                starships_response = requests.get(url=starships_link).json()["name"]
                                starships_string += f"{starships_response}, "
                                dict_items[key] = starships_string[:-2]
                        elif key == "vehicles":
                            vehicles_string = ""
                            for vehicles_link in value:
                                vehicles_response = requests.get(url=vehicles_link).json()["name"]
                                vehicles_string += f"{vehicles_response}, "
                                dict_items[key] = vehicles_string[:-2]
                        else:
                            dict_items[key] = value
                    dict_persons[int(f"{item}")] = dict_items
            item += 1

        pprint(dict_persons)
        total_time = datetime.datetime.now() - start_time
        print(total_time)

        return dict_persons


if __name__ == "__main__":
    swapi_obj = Swapi()
    # with requests: 3 pers. - 8sec., 82 pers. - 1min. 58sec.
    swapi_obj.get_dict_persons()
