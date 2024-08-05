import os

def start():
    os.system('cmd /k "uvicorn app.main:app --reload"')


if __name__ == "__main__":
    start()


from . import models
from .database import engine
from .routers import posts, users, auth, votes
from .config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ============================================================

# FastAPI App
# models.Base.metadata.create_all(bind=engine) Creates all new tables. Not being used because of Alembic which can update tables and store their history 


app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
async def root():
    return {"message": "HELLO!:)"}
