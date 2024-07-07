from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
