import requests
import asyncio
import datetime
from more_itertools import chunked
from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

from model import SwapiPeople

load_dotenv()

url = "https://swapi.dev/api/people"  # 15.11.22 - damaged!
reserve_url = "https://www.swapi.tech/api/people"  # another structure and fields, not as swapi.dev

PG_DSN = getenv("PG_DSN")

CHUNK_SIZE = 10

Base = declarative_base()
engine = create_async_engine(PG_DSN)
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def get_qty_persons():
    response = requests.get(url=reserve_url)
    total_quant_persons = response.json()["total_records"]

    return total_quant_persons  # 82


async def chunked_async(async_iter, size):
    buffer_chunk = []
    while True:
        try:
            item = await async_iter.__anext__()
        except StopAsyncIteration:
            break
        buffer_chunk.append(item)
        if len(buffer_chunk) == size:
            yield buffer_chunk
            buffer_chunk = []


async def get_person(people_id: int, session: ClientSession):
    print(f"Begin of procedure: {people_id}")
    dict_person = {}
    async with session.get(f"{reserve_url}/{people_id}") as response:
        json_person_data = await response.json()
        for key, value in json_person_data["result"]["properties"].items():
            if key != "created" and key != "edited":
                dict_person[key] = value
    print(f"End of procedure: {people_id} finished.")

    return dict_person


async def get_persons():
    max_range = get_qty_persons() + 1
    async with ClientSession() as session:
        for chunk in chunked(range(1, max_range), CHUNK_SIZE):
            coroutines = [get_person(people_id=item, session=session) for item in chunk]
            results = await asyncio.gather(*coroutines)
            for person_data in results:
                yield person_data


async def upload_people(people_chunk):
    async with Session() as session:
        session.add_all([SwapiPeople(json=item) for item in people_chunk])
        await session.commit()


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()

    async for chunk in chunked_async(get_persons(), CHUNK_SIZE):
        asyncio.create_task(upload_people(chunk))

    tasks = set(asyncio.all_tasks()) - {asyncio.current_task()}
    for task in tasks:
        await task


start_time = datetime.datetime.now()
asyncio.run(main())
total_time = datetime.datetime.now() - start_time
print(f"Executed total time: {total_time}")
