import requests
import asyncio
import datetime
import more_itertools
import math
from aiohttp import ClientSession
from pprint import pprint

from model import DbClass

url = "https://swapi.dev/api/people"


# get quantity of SWAPI characters
def get_qty_persons():
    response = requests.get(url=url)
    total_quant_persons = response.json()["count"]

    return total_quant_persons


# get async dictionary of persons from API
async def get_dict_persons():
    session = ClientSession()
    total_quant_persons = get_qty_persons()
    dict_persons = {}
    start_time = datetime.datetime.now()
    item = 1

    while len(dict_persons) < 3:  # change: total_quant_persons !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        dict_items = {}
        url_pers = f"{url}/{item}"
        response = await session.get(url=url_pers)
        response = await  response.json()

        for key, value in response.items():
            if value != "Not found":
                if key != "created" and key != "edited":
                    if key == "films":
                        films_string = ""
                        for film_link in value:
                            film_response = await session.get(url=film_link)
                            film_response = await film_response.json()
                            film_response = film_response["title"]
                            films_string += f"{film_response}, "
                            dict_items[key] = films_string[:-2]
                    elif key == "species" or key == "starships" or key == "vehicles":
                        string = ""
                        for link in value:
                            response = await session.get(url=link)
                            response = await response.json()
                            response = response["name"]
                            string += f"{response}, "
                            dict_items[key] = string[:-2]
                    else:
                        dict_items[key] = value
                dict_persons[int(f"{item}")] = dict_items
        item += 1

    pprint(dict_persons)
    total_time = datetime.datetime.now() - start_time
    print(total_time)
    await session.close()

    return dict_persons


async def main():
    print(await get_dict_persons())

# with asyncio: 3pers. -2sec, 82pers. - 29sec.
asyncio.run(main())
