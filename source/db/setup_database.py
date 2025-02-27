from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import  sessionmaker

from config.database import database_engine_string

from model import base
from model.user import User
from model.processtemplate import ProcessTemplate
from model.task import Task



# Database setup
def setup_database(db_url=database_engine_string):
    engine = create_engine(db_url, echo=True)
    base.Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

InitSession = setup_database()


# Checking what kind of objects are present in the tables

def test_database(db_url=database_engine_string):
    engine = create_engine(db_url, echo=True)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Tables in the database:", tables)
    return sessionmaker(bind=engine)

TestSession = test_database()

