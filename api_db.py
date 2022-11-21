import logging
from pathlib import Path

import uvicorn
from databases import Database
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

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

# @app.on_event("startup")
# async def database_connect():
#     await database.connect()
#
#
# @app.on_event("shutdown")
# async def database_disconnect():
#     await database.disconnect()


@app.get("/")
async def status():
    return 0


@app.get("/news")
# async def fetch_data(id: int):
async def fetch_data():
    # ndb.create_connection(DATABASE_NAME)
    await database.connect()
    # query = "SELECT * FROM news" #.format(str(id))
    await database.execute(query=ndb.CREATE_TABLE_SQL)
    results = await database.fetch_all(query=ndb.SELECT_FROM_SQL)
    await database.disconnect()

    return results


@app.get("/purge")
async def purge():
    # await database.connect()
    try:
        await ndb.delete_all_news(ndb.create_connection(DATABASE_NAME))
    except:
        await database.transaction().rollback()
        logging.warning("Rollback database transaction ! Purging canceled !")
    else:
        await database.transaction().commit()
        # AttributeError: 'Transaction' object has no attribute '_connection'
        logging.info("Database was purged successfully !")

    await database.disconnect()


@app.post("/insert")
async def insert(data: list):
    # await database.connect()
    ndb.insert_into(ndb.create_connection(DATABASE_NAME), data)
    # try:
    #     pass
    # await ndb.delete_all_news(ndb.create_connection(DATABASE_NAME))
    # except:
    #     await database.transaction().rollback()
    # else:
    #     await database.transaction().commit()

    # result = await database.execute(query=ndb.SELECT_COUNT_SQL)

    await database.disconnect()
    # return result


if __name__ == "__main__":
    uvicorn.run(app, port=8888, host="0.0.0.0")
    # uvicorn.run(app, port=8888)
