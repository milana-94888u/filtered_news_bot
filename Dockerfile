FROM python:3.11

ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /src

COPY poetry.lock /
COPY pyproject.toml /
COPY README.md /
RUN python3.11 -m pip install --upgrade pip
RUN python3.11 -m pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only=main --no-root # install dependencies

COPY src .

CMD poetry run python telegram_bot/bot.py
