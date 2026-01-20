import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

engin = create_engine(
    os.getenv("DATABASE_URL"),
    echo=False,
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engin)

def get_session():
    return SessionLocal()
