from functools import lru_cache

from pydantic import SecretStr, DirectoryPath
from pydantic_settings import BaseSettings
from environs import Env

env = Env()
env.read_env()


class Config(BaseSettings):
    bot_token: SecretStr
    models_path: DirectoryPath


@lru_cache(maxsize=1)
def parse_config() -> Config:
    return Config()  # type: ignore


if __name__ == "__main__":
    config = parse_config()
    print(config)
