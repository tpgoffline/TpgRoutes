import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String

Base = declarative_base()
Session = sessionmaker()

engine = create_engine(
    os.environ.get("TPGROUTES_DATABASE_URL") or os.environ.get("DATABASE_URL")
)
Session.configure(bind=engine)
session = Session()


class MondayTimetables(Base):
    __tablename__ = "monday"
    id = Column(Integer, primary_key=True)
    departure_stop = Column(String)
    arrival_stop = Column(Integer)
    departure_time = Column(Integer)
    arrival_time = Column(Integer)
    line = Column(String)
    trip_id = Column(Integer)
    destination_stop = Column(Integer)

    def __str__(self):
        return f"{self.departure_stop} / {self.arrival_stop} / {self.departure_time} / {self.arrival_time} / {self.line} / {self.trip_id} / {self.destination_stop}"


class FridayTimetables(Base):
    __tablename__ = "friday"
    id = Column(Integer, primary_key=True)
    departure_stop = Column(String)
    arrival_stop = Column(Integer)
    departure_time = Column(Integer)
    arrival_time = Column(Integer)
    line = Column(String)
    trip_id = Column(Integer)
    destination_stop = Column(Integer)

    def __str__(self):
        return f"{self.departure_stop} / {self.arrival_stop} / {self.departure_time} / {self.arrival_time} / {self.line} / {self.trip_id} / {self.destination_stop}"


class SaturdayTimetables(Base):
    __tablename__ = "saturday"
    id = Column(Integer, primary_key=True)
    departure_stop = Column(String)
    arrival_stop = Column(Integer)
    departure_time = Column(Integer)
    arrival_time = Column(Integer)
    line = Column(String)
    trip_id = Column(Integer)
    destination_stop = Column(Integer)

    def __str__(self):
        return f"{self.departure_stop} / {self.arrival_stop} / {self.departure_time} / {self.arrival_time} / {self.line} / {self.trip_id} / {self.destination_stop}"


class SundayTimetables(Base):
    __tablename__ = "sunday"
    id = Column(Integer, primary_key=True)
    departure_stop = Column(String)
    arrival_stop = Column(Integer)
    departure_time = Column(Integer)
    arrival_time = Column(Integer)
    line = Column(String)
    trip_id = Column(Integer)
    destination_stop = Column(Integer)

    def __str__(self):
        return f"{self.departure_stop} / {self.arrival_stop} / {self.departure_time} / {self.arrival_time} / {self.line} / {self.trip_id} / {self.destination_stop}"
