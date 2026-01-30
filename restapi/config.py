'''Application configuration using Pydantic Settings.'''
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    '''Application settings loaded from environment variables.'''

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
    )

    # Database
    database_host: str = 'localhost'
    database_port: int = 5432
    database_name: str = 'app'
    database_user: str = 'app'
    database_password: str = ''

    # Application
    environment: str = 'development'
    debug: bool = False

    @property
    def database_url(self) -> str:
        '''Build PostgreSQL connection URL.'''
        return f'postgresql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}'


@lru_cache
def get_settings() -> Settings:
    '''Cached settings instance.'''
    return Settings()
