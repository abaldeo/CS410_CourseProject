
FROM python:3.11 as requirements-stage
WORKDIR /tmp

RUN pip install pipx 

RUN pipx install pdm  

ENV PATH="/root/.local/bin:${PATH}"

COPY ./pyproject.toml ./pdm.lock* /tmp/

RUN pdm export -f requirements --output requirements.txt --without-hashes

#COPY pyproject.toml pdm.lock ./
#RUN pip install pdm && \
#    pdm install --no-ansi --no-interaction


FROM python:3.11

RUN mkdir /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && \
    apt install -y postgresql-client

COPY --from=requirements-stage /tmp/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir","app/"]
