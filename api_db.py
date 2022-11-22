import logging
from pathlib import Path
from typing import Dict, List

import uvicorn
from databases import Database
from fastapi import FastAPI, status

import news_db

# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.WARNING
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.ERROR
)


app = FastAPI()

DATABASE_NAME = Path("news_database.db")

database = Database(f"sqlite:///{DATABASE_NAME}")

ndb = news_db.NewsDatabase()


@app.get("/healthcheck", status_code=status.HTTP_200_OK)
async def healthcheck() -> Dict:
    """
    Healthcheck of API
    :return:
    """
    return {"healthcheck": "True"}


@app.get("/news")
async def news() -> List:
    """
    Get data from DB and return it to API client
    :return:
    """
    await database.connect()
    await database.execute(query=ndb.CREATE_TABLE_SQL)
    results = await database.fetch_all(query=ndb.SELECT_FROM_SQL)
    await database.disconnect()

    return results


@app.get("/purge")
async def purge():
    """
    Delete all data from news db, commit changes into delete_all_news() method
    In case of err rollback
    :return:
    """
    try:
        await ndb.delete_all_news(ndb.create_connection(DATABASE_NAME))
    except:
        await database.transaction().rollback()
        logging.warning("Rollback database transaction ! Purging canceled !")

    await database.disconnect()


@app.post("/insert")
async def insert(data: list):
    """
    Insert data to SQLite and close connection
    :param data:
    :return:
    """
    ndb.insert_into(ndb.create_connection(DATABASE_NAME), data)
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run(app, port=8888, host="0.0.0.0")
    # uvicorn.run(app, port=8888)  # Use for local testing
