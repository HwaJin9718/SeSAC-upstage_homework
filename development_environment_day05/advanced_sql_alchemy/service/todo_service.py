from development_environment_day05.advanced_sql_alchemy.repository import todo_repo

def create_todo(content):
    result = todo_repo.create_todo(content)
    return result

def get_todos():
    result = todo_repo.get_todos()
    return result

def delete_todo(todo_id):
    result = todo_repo.delete_todo(todo_id)
    return result
