import requests
import asyncio
import datetime
from aiohttp import ClientSession
from pprint import pprint
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from dotenv import load_dotenv

load_dotenv()
url = "https://swapi.dev/api/people"
PG_DSN = getenv("PG_DSN")
Base = declarative_base()

engine = create_async_engine(PG_DSN)


# get quantity of SWAPI characters
def get_qty_persons():
    response = requests.get(url=url)
    total_quant_persons = response.json()["count"]

    return total_quant_persons


# get async dict and list of persons from API
async def get_persons():
    session = ClientSession()
    total_quant_persons = get_qty_persons()
    dict_persons = {}
    list_persons = []
    start_time = datetime.datetime.now()
    item = 1
    while len(dict_persons) < total_quant_persons:
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
        list_persons.append(dict_items)
        item += 1

    # pprint(dict_persons)
    # pprint(list_persons)
    total_time = datetime.datetime.now() - start_time
    print(total_time)
    await session.close()

    return dict_persons, list_persons


async def main():
    task_get_api_persons = asyncio.create_task(get_persons())
    await task_get_api_persons


# with asyncio: 3pers. - 1,9sec, 82pers. - 26,4sec.
asyncio.run(main())
