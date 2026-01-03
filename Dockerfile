FROM python:3.13-slim

RUN pip install --no-cache-dir uv==0.9.18

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    locales=2.41-12 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen \
  && dpkg-reconfigure --frontend=noninteractive locales

ENV LC_TIME="ru_RU.UTF-8"

WORKDIR /app

COPY pyproject.toml ./
COPY uv.lock ./

RUN uv sync --locked

COPY ./app ./app
COPY ./tg_bot.py ./
COPY ./tg_schedule.py ./

ENV PYTHONDONTWRITEBYTECODE=yes
ENV PYTHONUNBUFFERED=yes

CMD ["uv", "run", "tg_bot.py"]
