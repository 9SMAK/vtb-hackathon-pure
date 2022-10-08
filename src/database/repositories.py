from contextlib import AbstractContextManager
from typing import Callable, Iterator, List

from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from .tables import User, Friends


class UserRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def create_table(self, engine):
        User.__table__.create(engine)
        
    def drop_table(self, engine):
        User.__table__.drop(engine)

    def get_all(self) -> Iterator[User]:
        with self.session_factory() as session:
            return session.query(User).all()

    def get_by_id(self, user_id: int) -> User:
        with self.session_factory() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise IdNotFoundError("User", user_id)
            return user

    def get_by_nick(self, user_nick: str) -> User:
        with self.session_factory() as session:
            user = session.query(User).filter(User.nick == user_nick).first()
            if not user:
                raise NameNotFoundError("User", user_nick)
            return user

    def add(
        self, nick: str, desc: str = "", 
        lvl: int = 1, exp: int = 0,
        is_admin: bool = False, is_editor: bool = False,
        is_teamlead: bool = False,
        #equipment = Column(???),
        visible_in_rating: bool = True, cases_count: int = 0,
        #events = Column(???), minions: List[CutUser] = []
    ) -> User:
        with self.session_factory() as session:
            user = User(
                nick=nick, desc=desc, lvl=lvl, exp=exp,
                is_admin=is_admin, is_editor=is_editor,
                is_teamlead=is_teamlead, #equipment = Column(???),
                visible_in_rating=visible_in_rating, cases_count=cases_count,
                #events = Column(???), minions=minions
            )
                
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def delete_by_id(self, user_id: int) -> None:
        with self.session_factory() as session:
            entity: User = session.query(User).filter(User.id == user_id).first()
            if not entity:
                raise IdNotFoundError("User", user_id)
            session.delete(entity)
            session.commit()

    def get_user_friends(self, user_id) -> Iterator[User]:
        with self.session_factory() as session:
            friends = session.query(User).select_from(Friends).filter(Friends.user_from_id == user_id). \
                join(User, User.id == Friends.user_to_id).filter(Friends.is_friends == True).all()
            return friends


class FriendsRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def create_table(self, engine):
        Friends.__table__.create(engine)
        
    def drop_table(self, engine):
        Friends.__table__.drop(engine)

    def get_all(self) -> Iterator[Friends]:
        with self.session_factory() as session:
            return session.query(Friends).all()

    def get_by_id(self, friends_id: int) -> Friends:
        with self.session_factory() as session:
            friends_pair = session.query(Friends).filter(Friends.id == friends_id).first()
            if not friends_pair:
                raise IdNotFoundError("Friends pair", friends_id)
            return friends_pair

    def get_user_friends(self, user_id: int) -> Iterator[User]:
        with self.session_factory() as session:
            friends = session.query(User).select_from(Friends).filter(Friends.user_from_id == user_id). \
                join(User, User.id == Friends.user_to_id).filter(Friends.is_friends == True).all()
            return friends

    def get_user_input_requests(self, user_id: int) -> Iterator[Friends]:
        with self.session_factory() as session:
            friends = session.query(Friends).filter(Friends.user_to_id == user_id, Friends.is_friends == False).all()
            #if not friends: TODO: what to do in this case?
            #    raise UserNameNotFoundError(user1_name)
            return friends
    
    def get_user_output_requests(self, user_id: int) -> Iterator[Friends]:
        with self.session_factory() as session:
            friends = session.query(Friends).filter(Friends.user_from_id == user_id, Friends.is_friends == False).all()
            #if not friends: TODO: what to do in this case?
            #    raise UserNameNotFoundError(user1_name)
            return friends

    def add(self, user_from_id: int, user_to_id: int, is_friends: bool = False) -> Friends:
        with self.session_factory() as session:
            friends = Friends(user_from_id=user_from_id, user_to_id=user_to_id, is_friends=is_friends)
            session.add(friends)
            session.commit()
            session.refresh(friends)
            return friends

    def delete_request(self, user_from_id, user_to_id) -> None:
        with self.session_factory() as session:
            entity: Friends = session.query(Friends).filter(Friends.user_from_id == user_from_id, Friends.user_to_id == user_to_id).first()
            #if not entity:
            #    raise IdNotFoundError("Friends pair", friends_id)
            session.delete(entity)
            session.commit()

    def delete_by_id(self, friends_id: int) -> None:
        with self.session_factory() as session:
            entity: Friends = session.query(Friends).filter(Friends.id == friends_id).first()
            if not entity:
                raise IdNotFoundError("Friends pair", friends_id)
            session.delete(entity)
            session.commit()



class NotFoundError(Exception):

    entity_name: str
    search_pattern: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, {self.search_pattern}: {entity_id}")


class IdNotFoundError(NotFoundError):
    def __init__(self, entity_name, entity_id):
        self.entity_name = entity_name
        super().__init__(entity_id)

    search_pattern: str = "id"

class NameNotFoundError(NotFoundError):
    def __init__(self, entity_name, entity_id):
        self.entity_name = entity_name
        super().__init__(entity_id)

    search_pattern: str = "name"
