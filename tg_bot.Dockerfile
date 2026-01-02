FROM python:3.13-slim

RUN pip install --no-cache-dir uv==0.9.18

WORKDIR /app

COPY pyproject.toml ./
COPY uv.lock ./

RUN uv sync --locked

COPY ./app ./app
COPY ./tg_bot.py ./

CMD ["uv", "run", "tg_bot.py"]
