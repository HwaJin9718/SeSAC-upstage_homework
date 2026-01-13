from development_environment_day05.advanced_3_layered.repository import todo_repo

def create_todo(content):
    todo_id = todo_repo.create_todo(content)
    result = todo_repo.get_todo_by_id(todo_id)
    return result

def get_todos():
    result = todo_repo.get_todos()
    return result

def delete_todo(todo_id):
    result = todo_repo.delete_todo(todo_id)
    return result
