from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import hashlib

engine = create_engine("sqlite:///database.db", connect_args={"check_same_thread": False})
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = scoped_session(Session)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

Base.metadata.create_all(engine)

def username_taken(username):
    
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user is not None:
        return True 
    return False

def add_user(username, password):
    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    # Add the user to the database
    new_user = User(username=username, password=hashed_password)
    session.add(new_user)
    session.commit()
    return 0

def get_user_password(username):
    user = session.query(User).filter_by(username=username).first()
    if user is None:
        return None
    else:
        return user.password
