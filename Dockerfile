FROM python:3.11-slim-bullseye
ENV PYTHONUNBUFFERED=1
WORKDIR /code

RUN apt-get update && apt-get install -y curl
COPY requirements.txt ./app/requirements.txt
RUN pip install -r ./app/requirements.txt
COPY . .

ARG USER=app
ARG UID=1000
RUN groupadd $USER --gid $UID
RUN useradd $USER --uid $UID --gid $UID --no-create-home
USER app:app
EXPOSE 8000
