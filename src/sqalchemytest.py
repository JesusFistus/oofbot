from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLAlchemy-Initialisierung
engine = create_engine('sqlite:///C:/Users/Martin/Documents/GitHub/oofbot/src/data/bot.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)


class CalendarEntry(Base):
    __tablename__ = 'CalendarEntries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    category = Column(String)
    start = Column(Integer)
    end = Column(Integer)
    repitation = Column(Integer)

    def __repr__(self):
        return f'<CalendarEntry(id={self.id}, name={self.name}, start={self.start}, end={self.end})>'


session = Session()

entry = CalendarEntry(name='tesst111', start=3)
session.add(entry)

for x in session.query(CalendarEntry).filter_by(start=3).all():
    print(x)

session.commit()