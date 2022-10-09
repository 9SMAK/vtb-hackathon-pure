import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_URL = os.getenv("POSTGRES_URL")

IPFS_URL = os.getenv("IPFS_URL")

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
