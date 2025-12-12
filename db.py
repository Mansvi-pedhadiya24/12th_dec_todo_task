from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_USERNAME = "root"
DATABASE_PASSWORD = ""
DATABASE_HOST = "localhost"
DATABASE_NAME = "to_do"

DATABASE_URL = "mysql+pymysql://root:@localhost/library"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
