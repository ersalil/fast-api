from sqlite3 import Timestamp
from uuid import UUID
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Embark(Base):
    __tablename__ = 'embark_summary'
    voyage_id  = Column(String)
    added_date = Column(TIMESTAMP, primary_key=True)
    oci_completed_core = Column(Integer)
    moci_completed_core = Column(Integer)
    checkedin_couch = Column(Integer)
    onboard_couch = Column(Integer)


class Voyage(Base):
    __tablename__ = 'voyage'
    voyage_id = Column(String)
    number = Column(String)
    added_date = Column(TIMESTAMP, primary_key=True)