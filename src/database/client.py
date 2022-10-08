from typing import List

from .database import Database
from .tables import User, Friends
from .repositories import UserRepository, FriendsRepository
from src import config as cfg

url = f"postgresql+psycopg2://{cfg.POSTGRES_USER}:{cfg.POSTGRES_PASSWORD}@{cfg.POSTGRES_URL}/{cfg.POSTGRES_DB}"

db = Database(url)
# db.create_database()

engine = db.get_engine()

users = UserRepository(db.session)

users.create_table(engine)
users.add("Masstermax")
users.add("Dangl")

friends = FriendsRepository(db.session)

friends.create_table(engine)
friends.add(1, 2, True)

users.get_user_friends(1)