from pydantic import AmqpDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    server_host: str = "127.0.0.1"
    server_port: int = 8000
    db_host: str
    db_name: str
    collection_name: str
    llm_model: str
    embedding_model: str
    openai_api_key: str
    langchain_api_key: str
    langchain_endpoint: str
    langchain_project: str
    langchain_tracing_v2: bool
    amqp_dsn: AmqpDsn
    service_name: str = "fast_ai"
    docs_dir: str = "./documents"
    vectorstore_dir: str = "./chromadata"


fast_ai_settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
