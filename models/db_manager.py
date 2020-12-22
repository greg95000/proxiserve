from models.base import Base
from models.users import User
from models.consumptions import Consumption
from models.singleton import SingletonMeta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class dbManager(metaclass=SingletonMeta):

    def __init__(self):
        self.session = None

    def create_database(self):
        engine = create_engine('sqlite://', echo=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)
