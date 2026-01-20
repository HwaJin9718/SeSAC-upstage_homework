from fastapi import APIRouter, Request, HTTPException
from network_and_cloud.day01.advanced.service import todo_service

todo_route = APIRouter()

# ---------------------------
# CREATE
# ---------------------------
@todo_route.post("/todos")
async def create_todo(request: Request):
    body = await request.json()
    content = body.get("content")

    if not content:
        raise HTTPException(status_code=400, detail="content is required")

    result = todo_service.create_todo(content)

    return result

# ---------------------------
# READ
# ---------------------------
@todo_route.get("/todos")
def get_todos():

    result = todo_service.get_todos()

    return result

# ---------------------------
# DELETE
# ---------------------------
@todo_route.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    result = todo_service.delete_todo(todo_id)

    if result == 0:
        raise HTTPException(status_code=404, detail="Todo not found")

    return {"message": "Todo deleted"}
