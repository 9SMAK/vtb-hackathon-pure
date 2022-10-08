import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

POSTGRES_DB = os.getenv("POSTGRES_DB")

IPFS_URL = os.getenv("IPFS_URL")
