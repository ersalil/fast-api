from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://postgres:1234@localhost/item_db", echo=True)

Base  = declarative_base()

SessionLocal = sessionmaker(bind=engine)