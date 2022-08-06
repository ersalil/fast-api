from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# create engine
engine = create_engine(os.getenv("ENGINE"))

# create base class
Base  = declarative_base()

# create session
SessionLocal = sessionmaker(bind=engine)