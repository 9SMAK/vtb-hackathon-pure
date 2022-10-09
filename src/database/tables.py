from sqlalchemy import Boolean, Column, Integer, String, Float, CheckConstraint, PickleType
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    login = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, default="")
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    is_admin = Column(Boolean, default=False)
    is_editor = Column(Boolean, default=False)
    is_lead = Column(Boolean, default=False)
    case_count = Column(Integer, default=3)  # TODO maybe remove
    public_key = Column(String)
    private_key = Column(String)
    equipment = Column(PickleType, default={})

    __table_args__ = (CheckConstraint('case_count >= 0'),)

    # equipment = Column(???)
    # visible_in_rating = Column(Boolean, default=True)
    # events = Column(???)
    # minions = Column(ARRAY(CutUser), default=[])
    # achievements = Column(???)
    # SOME AUTH?
    def __repr__(self):
        return f"<User(id={self.id}, " \
               f"name=\"{self.name}\", " \
               f"login=\"{self.login}\", " \
               f"level=\"{self.level}\")>" \
            # f"lvl={self.lvl})>" \
        # f"exp=\"{self.nick}\", " \
        # f"is_admin=\"{self.desc}\", " \
        # f"={self.lvl})>"


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


class Relationships(Base):
    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True)
    lead = Column(Integer, index=True)
    worker = Column(Integer, index=True)

    def __repr__(self):
        return f"<Relationships(id={self.id}, " \
               f"lead={self.lead}, " \
               f"worker={self.worker})>"


class Achievement(Base):
    __tablename__ = "achievement"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String, default="")
    svg = Column(String)

    def __repr__(self):
        return f"<Achievements(id={self.id}, " \
               f"name={self.name}, " \
               f"description={self.description}, " \
               f"svg={self.svg})>"


class Merch(Base):
    __tablename__ = "merch"

    id = Column(Integer, primary_key=True)
    description = Column(String)
    image = Column(String)
    price = Column(Float)

    def __repr__(self):
        return f"<Merch(id={self.id}, " \
               f"description={self.description}, " \
               f"image={self.image}, " \
               f"price={self.price})>"


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, default="")
    type = Column(String)
    members = Column(ARRAY(Integer), default=[])

    def __repr__(self):
        return f"<Events(id={self.id}, " \
               f"title={self.title}, " \
               f"description={self.description}, " \
               f"type={self.type}, " \
               f"members={self.members})>"
