import sys
from functools import lru_cache

import httpx
from celery_app import app


@app.task(name="add")
def add(x, y):
    return x + y


@app.task(name="is_prime")
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


@app.task(name="fibo")
def fibo(n):
    return fibonacci(n)


def matrix_multiply(A, B):
    return [
        [A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
        [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]],
    ]


def matrix_power(A, n):
    if n == 1:
        return A
    if n % 2 == 0:
        half_pow = matrix_power(A, n // 2)
        return matrix_multiply(half_pow, half_pow)
    else:
        return matrix_multiply(A, matrix_power(A, n - 1))


@lru_cache(maxsize=256)
def fibonacci(n):
    if n == 0:
        return 0
    matrix = [[1, 1], [1, 0]]
    result_matrix = matrix_power(matrix, n - 1)
    return result_matrix[0][0]


@app.task(name="weather")
def get_weather(city):
    base_url = f"https://wttr.in/{city}?format=%t"  # %t represents temperature
    response = httpx.get(base_url)

    if response.status_code == 200:
        weather_data = response.text.strip()
        return weather_data
    print("Error fetching weather data.", file=sys.stderr)
