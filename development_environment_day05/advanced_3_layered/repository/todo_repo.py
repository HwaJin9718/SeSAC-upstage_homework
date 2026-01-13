import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

def get_db():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )


def create_todo(content):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "insert into todo (content) values (%s)",
        (content,)
    )
    conn.commit()

    todo_id = cursor.lastrowid

    return todo_id


def get_todo_by_id(todo_id):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "select * from todo where id = %s",
        (todo_id,)
    )
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "id": row[0],
        "content": row[1],
        "created_at": str(row[2])
    }


def get_todos():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "select * from todo"
    )
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": r[0],
            "content": r[1],
            "created_at": str(r[2])
        }
        for r in rows
    ]


def delete_todo(todo_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "delete from todo where id = %s",
        (todo_id,)
    )
    conn.commit()

    affected = cursor.rowcount

    cursor.close()
    conn.close()

    return affected
