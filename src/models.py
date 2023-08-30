import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Table
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), unique=True, nullable=False)
    firstname = Column(String(250))
    lastname = Column(String(250))
    email = Column(String(250), unique=True, nullable=False)

class Follower(Base):
    __tablename__ = 'followers'
    user_from_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250))
    author_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))

class MediaType(Enum):
    image = "image"
    video = "video"

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(MediaType, nullable=False)
    url = Column(String(250))
    post_id = Column(Integer, ForeignKey('posts.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type.value,
            "url": self.url,
            "post_id": self.post_id
        }

engine = create_engine('sqlite:///instagram.db', echo=True)  # Set echo to False to suppress SQLAlchemy logs
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Create a new user
new_user = User(username="@salomonfranco", email="salo@gmail.com")
session.add(new_user)
session.commit()

try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
