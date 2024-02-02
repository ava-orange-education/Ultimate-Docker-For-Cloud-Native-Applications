import os

from fastapi import FastAPI

app = FastAPI()

GREETER = os.getenv("GREETER", "Docker")


@app.get("/")
async def index(name: str = None):
    greetee = name or "Friend"
    return {"message": f"Hello {greetee}! I am {GREETER}."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
