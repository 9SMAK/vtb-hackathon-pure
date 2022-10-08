from email.policy import default
from sqlalchemy import ARRAY, Column, String, Boolean, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
#from sqlalchemy.dialects.postgresql import ARRAY

from .database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    nick = Column(String, nullable=False, unique=True)
    desc = Column(String, default="")
    lvl = Column(Integer, default=1)
    exp = Column(Integer, default=0)
    is_admin = Column(Boolean, default=False)
    is_editor = Column(Boolean, default=False)
    is_teamlead = Column(Boolean, default=False)
    #equipment = Column(???)
    visible_in_rating = Column(Boolean, default=True)
    cases_count = Column(Integer, default=0)
    #events = Column(???)
    #minions = Column(ARRAY(CutUser), default=[])
    #achievements = Column(???)
    
    #SOME AUTH?

    def __repr__(self):
        return f"<User(id={self.id}, " \
               f"nick=\"{self.nick}\", " \
               f"desc=\"{self.desc}\")>" \
               #f"lvl={self.lvl})>" \
               #f"exp=\"{self.nick}\", " \
               #f"is_admin=\"{self.desc}\", " \
               #f"={self.lvl})>"


class Friends(Base):

    __tablename__ = "friends"

    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, index=True)
    user_to_id = Column(Integer, index=True)
    is_friends = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Friends(id={self.id}, " \
               f"user_from_id={self.user_from_id}, " \
               f"user_to_id={self.user_to_id}, " \
               f"is_friends={self.is_friends})>"


