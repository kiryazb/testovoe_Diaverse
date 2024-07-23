import time

from celery import Celery

from config import REDIS_HOST, REDIS_PORT

celery = Celery('utils', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')


@celery.task
def long_operation() -> dict:
    time.sleep(10)
    return {"status": 200,
            "details": "Очень долгая операция выполнена с помощью Celery"}
