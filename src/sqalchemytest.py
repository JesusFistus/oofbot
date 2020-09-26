from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLAlchemy-Initialisierung
engine = create_engine('sqlite:///data/bot.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)


class CalendarEntry(Base):
    __tablename__ = 'CalendarEntries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    start = Column(Integer)
    end = Column(Integer)

    def __repr__(self):
        return f'<CalendarEntry(id={self.id}, name={self.name}, start={self.start}, end={self.end})>'


session = Session()

for x in session.query(CalendarEntry).all():
    print(x)
session.commit()