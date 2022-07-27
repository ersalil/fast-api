from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://sreintern:TxSyHPDoaw44396z@34.135.5.178/sreinsights_dcl", echo=True)

Base  = declarative_base()

SessionLocal = sessionmaker(bind=engine)