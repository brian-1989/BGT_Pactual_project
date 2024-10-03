from decouple import config

class Settings:
    DATABASE_URL = config("DATABASE_URL", cast=str)
    MONGO_INITDB_DATABASE = config("MONGO_INITDB_DATABASE", cast=str)