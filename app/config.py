from decouple import config

class Settings:
    DATABASE_URL = config("DATABASE_URL", cast=str)
    MONGO_INITDB_DATABASE = config("MONGO_INITDB_DATABASE", cast=str)
    SMTP_SERVER = config("SMTP_SERVER", cast=str)
    SMTP_PORT = config("SMTP_PORT", cast=int)
    SENDER_EMAIL = config("SENDER_EMAIL", cast=str)
    PASSWORD_EMAIL = config("PASSWORD_EMAIL", cast=str)
    VONAGE_KEY = config("VONAGE_KEY", cast=str)
    VONAGE_SECRET = config("VONAGE_SECRET", cast=str)
