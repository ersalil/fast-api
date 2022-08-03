from sqlalchemy import TIMESTAMP, Column, Integer, String, DateTime
from database import Base

class Embark(Base):
    __tablename__ = 'embark_summary'
    voyage_id  = Column(String)
    added_date = Column(TIMESTAMP, primary_key=True)
    oci_completed_core = Column(Integer)
    moci_completed_core = Column(Integer)
    checkedin_couch = Column(Integer)
    onboard_couch = Column(Integer)

class Ship(Base):
    __tablename__ = 'ship'
    ship_id = Column(String, primary_key=True)
    name = Column(String)
    code = Column(String)

class Environment(Base):
    __tablename__ = 'environment'
    environment_id = Column(String, primary_key=True)
    ship_id = Column(String)

class Voyage(Base):
    __tablename__ = 'voyage'
    voyage_id = Column(String)
    number = Column(String)
    environment_id = Column(String)
    embark_date = Column(DateTime)
    added_date = Column(TIMESTAMP, primary_key=True)