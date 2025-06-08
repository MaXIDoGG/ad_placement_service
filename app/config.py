from dotenv import load_dotenv
from os import getenv

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL", "postgresql+asyncpg://postgres:pass@postgres:5432/postgres_db")
SECRET_KEY = getenv("SECRET_KEY", "SECRET_KEY")
ALGORITHM = getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

ADMIN_LOGIN = getenv("ADMIN_LOGIN", "admin")
ADMIN_NAME = getenv("ADMIN_NAME", "admin")
ADMIN_PASSWORD = getenv("ADMIN_PASSWORD", "admin")