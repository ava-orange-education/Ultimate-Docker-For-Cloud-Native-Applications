import asyncio
from functools import lru_cache

from asgiref.sync import sync_to_async
from celery import Celery
from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException
from httpx import AsyncClient, Response
from pydantic import BaseModel, BaseSettings
from redis import Redis


class Settings(BaseSettings):
    PORT: int = 8000
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None

    CELERY_REDIS_DB: int = 1

    EXCHANGE_RATE_API_URL: str = "https://api.exchangerate.host/latest"

    BASE_CURRENCIES: list[str] = ["USD", "EUR", "GBP"]

    UPDATE_FREQUENCY_SECONDS: float = 60.0


settings = Settings()
app = FastAPI()


worker = Celery(
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.CELERY_REDIS_DB}"
)


@worker.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(settings.UPDATE_FREQUENCY_SECONDS, update_redis.s())


@worker.task
def update_redis():
    sync_to_async(do_update_redis)()


async def do_update_redis():
    async with AsyncClient() as client:
        tasks = []
        for currency in settings.BASE_CURRENCIES:
            tasks.append(
                client.get(f"{settings.EXCHANGE_RATE_API_URL}?base={currency}")
            )

        responses: list[Response] = await asyncio.gather(*tasks)

    redis = get_redis()
    pipeline = redis.pipeline()

    for response in responses:
        data = response.json()

        pipeline.hset(
            data["base"],
            mapping=data["rates"],
        )

    pipeline.execute()


@lru_cache(maxsize=1)
def get_redis():
    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        decode_responses=True,
    )


class ExchangeRate(BaseModel):
    base_currency: str
    target_currency: str
    exchange_rate: float


class BaseException_(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=self.status_code, detail=detail)


class RateNotFound(BaseException_):
    status_code = 404


@app.on_event("startup")
async def populate_redis():
    await do_update_redis()


@app.get("/{base_currency}/{target_currency}", response_model=ExchangeRate)
async def get_exchange_rate(
    base_currency: str, target_currency: str, redis: Redis = Depends(get_redis)
) -> dict[str, float]:
    exchange_rate = redis.hget(base_currency, target_currency)

    if exchange_rate is None:
        raise RateNotFound(
            detail=f"Exchange rate for {base_currency} to {target_currency} not found"
        )

    return {
        "base_currency": base_currency,
        "target_currency": target_currency,
        "exchange_rate": exchange_rate,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
