import logging
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

ndb = news_db.NewsDatabase()
ndb.create_table(ndb.create_connection(ndb.DATABASE_NAME))
database = Database(f"sqlite:///{ndb.DATABASE_NAME}")


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
    Disconnect
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
    Close connection
    :return:
    """
    try:
        await ndb.delete_all_news(ndb.create_connection(ndb.DATABASE_NAME))
    except Exception as exception:
        await database.transaction().rollback()
        logging.warning("Rollback database transaction ! Purging canceled !")
        logging.error(exception)
    finally:
        await database.disconnect()


@app.post("/insert")
async def insert(data: list):
    """
    Insert data to SQLite and close connection
    :param data:
    :return:
    """
    ndb.insert_into(ndb.create_connection(ndb.DATABASE_NAME), data)
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run(app, port=8888, host="0.0.0.0")
    # uvicorn.run(app, port=8888)  # Use for local testing
