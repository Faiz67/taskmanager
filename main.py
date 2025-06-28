from fastapi import FastAPI

from routers.tasks import tasks
from routers.user_auth import user_auth
from internal.db import initialize_db


app = FastAPI()

app.include_router(user_auth, prefix="/auth", tags=["Authentication"])
app.include_router(tasks, prefix="/tasks", tags=["CRUD Operations"])


@app.get("/initalize_db")
async def initalize_db():
    try:
        initialize_db()
    except Exception as e:
        return {"error": str(e)}

    return {"message": "Database initialized successfully."}
