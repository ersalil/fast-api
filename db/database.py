from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# create engine
engine = create_engine("postgresql://sreintern:TxSyHPDoaw44396z@34.135.5.178/sreinsights_dcl")

# create base class
Base  = declarative_base()

# create session
SessionLocal = sessionmaker(bind=engine)

db = SessionLocal()

def executeSQL(sql):
    """
    Execute SQL query and return result
    """
    conn = engine.connect()
    data = conn.execute(sql)
    result = []
    for row in data:
        result.append(dict(row))
    return result