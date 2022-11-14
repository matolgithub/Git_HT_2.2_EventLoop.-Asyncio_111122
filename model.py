import sqlalchemy as sqla
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

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


class DbClass:
    def __init__(self, url_connect):
        self.engine = sqla.create_engine(url_connect)
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()
        self.creation = Base.metadata.create_all(self.engine)

    def db_upload(self, data):
        prs_before = len(self.session.query(SwapiPeople).all())
        for item in data:
            if self.session.query(SwapiPeople).filter_by(name=item.get("name")).first() is not None:
                print(f"{item.get('name')} already exist!")
                continue
            new_data = SwapiPeople(**item)
            self.session.add(new_data)
            self.session.commit()
            print(f"{item.get('name')} was added to DataBase!")
        new_prs = len(self.session.query(SwapiPeople).all()) - prs_before
        print(f"{new_prs} added!")
