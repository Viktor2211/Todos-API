from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:2211@localhost/TodoApplicationDataBase'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

SECRET_KEY = 'ldghl304skfj304ifl'
ALGORITHM = 'HS256'


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
