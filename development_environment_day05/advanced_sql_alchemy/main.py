from fastapi import FastAPI
import uvicorn
from development_environment_day05.advanced_sql_alchemy.controller import todo_route

app = FastAPI()
app.include_router(todo_route.todo_route)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)