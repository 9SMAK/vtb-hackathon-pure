import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_URL = os.getenv("POSTGRES_URL")

IPFS_URL = os.getenv("IPFS_URL")
