  
FROM python:3.11

RUN mkdir /app
WORKDIR /app

RUN apt update && \
    apt install -y postgresql-client


#COPY pyproject.toml pdm.lock ./
#RUN pip install pdm && \
#    pdm install --no-ansi --no-interaction

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt



COPY . .