from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
  PORT: int
  DATABASE: str
  COLLECTION: str
  MONGO_URI: str

  class Config:
    env_file = '.env'

settings = Settings()
