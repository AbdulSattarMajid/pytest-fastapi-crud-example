from app import models, user
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

import os

if os.getenv("AIOPS_API_URL") and os.getenv("AIOPS_API_KEY"):
    from aiops_sdk import install

    install(
        app,
        api_url=os.environ["AIOPS_API_URL"],
        api_key=os.environ["AIOPS_API_KEY"],
        service_name="crud-example",
    )

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router, tags=["Users"], prefix="/api/users")


@app.get("/api/healthchecker")
def root():
    return {"message": "The API is LIVE!!"}
