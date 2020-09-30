from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker
from pathlib import Path


Session = sessionmaker()
Column(Integer, Sequence('id'), primary_key=True)

path = 'C:/Users/Yannic Breiting/Documents/GitHub/oofbot/src/data/bot.db'
engine = create_engine(f'sqlite:///data/bot.db')

Base = declarative_base()
Session.configure(bind=engine)
session = Session()


class Calendar(Base):
    __tablename__ = 'CalendarEntries'
    id = Column(Integer, Sequence('id'), primary_key=True)
    name = Column(String(50))
    category = Column(String(50))
    start = Column(Integer)
    end = Column(Integer)
    repitation = Column(Integer)

    def add_entry(self, **kwargs):
        new_entry = Calendar(name='%s', category='%s', start='%s', end='%s', repitation='%s')
        session.add(new_entry)
        self.save_entry()

    def save_entry(self):
        session.commit()

    def show_all_entries(self):
        search = session.query(Calendar).all()
        return search

    def search_in_category(self, search_query):
        search = session.query(Calendar).filter_by(category=search_query).all()
        return search

    def __repr__(self):
        return "(id='%s', name='%s', category='%s', start='%s', end='%s', repitation='%s')\n" % (
                self.id, self.name, self.category, self.start, self.end, self.repitation)

c = Calendar()

print(c.show_all_entries())