from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SwapiPeople(Base):
    __tablename__ = "SwapiPeople"

    id = Column(Integer, primary_key=True)
    birth_year = Column(String(20))
    eye_color = Column(String(20))
    films = Column(String(200))
    gender = Column(String(20))
    hair_color = Column(String(20))
    height = Column(String(20))
    homeworld = Column(String(40))
    mass = Column(String(20))
    name = Column(String(80), nullable=False)
    skin_color = Column(String(40))
    species = Column(String(100))
    starships = Column(String(200))
    vehicles = Column(String(100))
