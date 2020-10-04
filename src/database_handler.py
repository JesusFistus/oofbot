from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

# SQL-Alchemy initalisierung
Session = sessionmaker()
engine = create_engine(f'sqlite:///data/bot.db')
Base = declarative_base()
Session.configure(bind=engine)


class Student(Base):
    __tablename__ = 'Students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    discord_id = Column(Integer, unique=True)
    name = Column(String)
    surname = Column(String)
    study_group = Column(String)


