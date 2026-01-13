from development_environment_day05.advanced_sql_alchemy.repository.connection import get_session
from development_environment_day05.advanced_sql_alchemy.model.todo import Todo


def create_todo(content):

    conn = get_session()

    try:
        todo = Todo(content=content)
        conn.add(todo)
        conn.commit()
        conn.refresh(todo)
        return todo
    finally:
        conn.close()


def get_todos():

    conn = get_session()

    todos = conn.query(Todo).all()

    return todos


def delete_todo(todo_id):

    conn = get_session()

    try:
        todo_id = conn.query(Todo).filter(Todo.id == todo_id).first()
        conn.delete(todo_id)
        conn.commit()
        return todo_id
    except:
        return 0
    finally:
        conn.close()
