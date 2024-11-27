from typing import Tuple, Optional, Union, List, Dict, Any

import pymysql

from config import Database


def get_connection():
    connection = pymysql.connect(
        host=Database.HOST,
        user=Database.USER,
        password=Database.PASSWORD,
        database=Database.DATABASE,
        cursorclass=Database.CURSOR_CLASS
    )
    return connection


def execute_query(
    query: str,
    params: Union[Tuple[Any], Any] = (),
    fetch_one: bool = False,
    fetch_all: bool = False
) -> Optional[Union[List[Dict[str, str]], Dict[str, str]]]:
    result = None

    with get_connection() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(query, params)
                if fetch_one:
                    result = cursor.fetchone()
                elif fetch_all:
                    result = cursor.fetchall()
                else:
                    connection.commit()
            except Exception as e:
                connection.rollback()
                raise ValueError(e.args[1])

    return result
