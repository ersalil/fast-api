from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# create engine
engine = create_engine("postgresql://sreintern:TxSyHPDoaw44396z@34.135.5.178/sreinsights_dcl")

# create base class
Base  = declarative_base()

# create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()