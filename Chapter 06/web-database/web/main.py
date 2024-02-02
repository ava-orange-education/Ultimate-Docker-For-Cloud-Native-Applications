#!/usr/bin/env python

import os

import psycopg2
from fastapi import FastAPI

app = FastAPI()

DSN = os.getenv(
    "DSN", "postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable"
)


@app.on_event("startup")
async def startup():
    app.state.db = psycopg2.connect(DSN)


@app.get("/")
async def index():
    with app.state.db.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        return {"message": result[0]}


@app.on_event("shutdown")
async def shutdown():
    app.state.db.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
