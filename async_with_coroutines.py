import asyncio
import datetime
import asyncpg
from more_itertools import chunked
from aiohttp import ClientSession
from pprint import pprint
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from async_swapi import get_qty_persons

from model import SwapiPeople

load_dotenv()

total_quant_persons = get_qty_persons()

url = "https://swapi.dev/api/people"

PG_DSN = getenv("PG_DSN")

CHUNK_SIZE = getenv("CHUNK_SIZE")

Base = declarative_base()
engine = create_async_engine(PG_DSN)
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


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
    print(f"Begin: {people_id}")
    async with session.get(f"{url}/{people_id}") as response:
        json_person_data = await response.json()
    print(f"End: {people_id}")

    return json_person_data


async def get_persons():
    async with ClientSession() as session:
        for chunk in chunked(range(1, total_quant_persons + 1), CHUNK_SIZE):
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
