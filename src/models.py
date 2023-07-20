import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, ForeignKey, Table, enumerate
from sqlalchemy.orm import relationship, backref, declarative_base, sessionmaker
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

engine = create_engine('sqlite:///instagram.db')
Session = sessionmaker(bind=engine)
session = Session()

user_account_table = Table('user_id', Base.metadata,
                             Column('user_from_id', Integer, ForeignKey('users.id')),
                             Column('media_id', Integer, ForeignKey('media.id')))

class Follower(Base):
    __tablename__ = 'followers'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    user_from_id = Column(Integer)
    user_to_id = Column(Integer)

user = relationship("users",
                            secondary=user_account_table,
                            back_populates="followers")

class User(Base):
    __tablename__ = 'users'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True, ForeignKey=True)
    username = Column(String(250), unique=True, nullable=False)
    firstname = Column(String(250))
    lastname = Column(String(250))
    email = Column(String(250), unique=True, nullable=False)     


class Media(Post):
    __tablename__ = 'media'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True, ForeignKey=True)
    type = Column(enumerate)
    url = Column(String(250))
    post_id = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'media',
        'polymorphic_on': type
    }

    users = relationship("User", 
                        secondary=user_account_table,
                        back_populates="media")

class Post(Post):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, ForeignKey=True)
    user_id = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'post',
    }

class Comment(Post):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, ForeignKey=True)
    comment_text = Column(String)
    author_id = Column(id)
    post_id = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'comment',
    }

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')

Base.metadata.create_all(engine)


# Create a new user
new_user = User(username="@salomonfranco", email="salo@gmail.com")

session.add(new_user)

session.commit()
