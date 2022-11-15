import requests
import asyncio
import datetime
import asyncpg
from more_itertools import chunked
import math
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
Base = declarative_base()

engine = create_async_engine(PG_DSN)


async def get_person():
    pass


async def get_persons():
    pass


async def db_upload():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async for item in get_persons():
        async with Session() as session:
            session.add(item)
            await session.commit()
    print("Db - success!")


async def main():
    task_get_api_persons = asyncio.create_task(get_persons())
    await task_get_api_persons

    task_upload_db = asyncio.create_task(db_upload())
    await task_upload_db


# with asyncio: 3pers. - ___sec, 82pers. - ___sec.
asyncio.run(main())
