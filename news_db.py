import json
import logging
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from sqlite3 import Error

# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.ERROR
)


class NewsDatabase:
    # SQL queries
    CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS news (
    author TEXT,
    title TEXT,
    description TEXT,
    url TEXT,
    pub_date TEXT
    );
    """

    INSERT_INTO_SQL = """
    INSERT INTO news
    (author,title,description,url,pub_date)
    VALUES(?,?,?,?,?);
    """

    SELECT_FROM_SQL = """
    SELECT * FROM news;
    """

    DELETE_FROM_SQL = """
    DELETE FROM news;
    """

    SELECT_COUNT_SQL = """
    SELECT COUNT(*) FROM news;
    """

    def __check_entities_count(self, conn):
        return conn.cursor().execute(self.SELECT_COUNT_SQL).fetchone()[0]

    def create_connection(self, db_file: Path):
        """
        Create db file
        :param db_file: path to db file to create
        :return:
        """
        try:
            conn = sqlite3.connect(db_file)
            logging.info("Connection created successfully !")
            return conn
        except Error as create_conn_err:
            logging.error(create_conn_err)
        return None

    def create_table(self, conn, create_table_query):
        """
        :param conn: Connection to the SQLite database
        :param create_table_query:
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_query)
            logging.info(f"Table created successfully !")
        except Error as create_table_err:
            logging.error(create_table_err)

    def insert_into(self, conn, data: list):
        """
        Insert data to base
        This is the load step in ETL pipeline
        :param conn: Connection to the SQLite database
        :param data:
        :return:
        """
        try:
            cur = conn.cursor()
            cur.execute(self.INSERT_INTO_SQL, data)
            conn.commit()
            logging.info(
                f"Data inserted successfully ! Entities in db for now: {self.__check_entities_count(conn)}"
            )
            return cur.lastrowid
        except Error as insert_err:
            logging.error(insert_err)

    def get_all_news(self, conn):
        """
        Query all rows in the news table
        :param conn: Connection to the SQLite database
        :return:
        """
        return conn.cursor().execute(self.SELECT_FROM_SQL).fetchall()

    async def delete_all_news(self, conn):
        """
        Delete all rows in the news table
        :param conn: Connection to the SQLite database
        :return:
        """
        conn.cursor().execute(self.DELETE_FROM_SQL)
        conn.commit()
        logging.info(
            f"Database was purged ! Entities in db for now: {self.__check_entities_count(conn)}"
        )


if __name__ == "__main__":
    # try:
    #     conn = create_connection(DB_FILE)
    #     if DB_FILE.exists():
    #         create_table(conn, CREATE_TABLE_SQL)
    #
    #     while True:
    #         CURRENT_TIME = datetime.now().strftime("%H:%M")
    #         time.sleep(1)
    #         if conn is not None:
    #             get_all_news(conn)
    #             if CURRENT_TIME == TIME_TO_PURGE:
    #                 logging.info(
    #                     f"Time to purge has come ! Entities in db for now: {__check_entities_count(conn)}"
    #                 )
    #                 delete_all_news(conn)
    #             else:
    #                 logging.info(
    #                     f"Still waiting for purging. Entities in db for now: {__check_entities_count(conn)}"
    #                 )
    # except sqlite3.Error as sql_err:
    #     logging.error(f"Cannot create the database connection. Error: {sql_err}")
    pass
