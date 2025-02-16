from pydantic_settings import BaseSettings


class Config(BaseSettings):
    es_url: str = "http://elasticsearch:9200"
