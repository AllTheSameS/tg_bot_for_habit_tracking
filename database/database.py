from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from config.config import DB_NAME, DB_USER, DB_HOST, DB_PASSWORD, DB_PORT

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
