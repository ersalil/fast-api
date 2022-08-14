from email.mime import application
from sqlalchemy import TIMESTAMP, Column, Integer, String, DateTime
from db.database import Base

# Create a model for the table 'embark_summary'
class Embark(Base):
    __tablename__ = 'embark_summary'
    voyage_id  = Column(String)
    added_date = Column(TIMESTAMP, primary_key=True)
    oci_completed_core = Column(Integer)
    moci_completed_core = Column(Integer)
    checkedin_couch = Column(Integer)
    onboard_couch = Column(Integer)

# Create a model for the table 'ship'
class Ship(Base):
    __tablename__ = 'ship'
    ship_id = Column(String, primary_key=True)
    name = Column(String)
    code = Column(String)

# Create a model for the table 'environment'
class Environment(Base):
    __tablename__ = 'environment'
    environment_id = Column(String, primary_key=True)
    ship_id = Column(String)

# Create a model for the table 'voyage'
class Voyage(Base):
    __tablename__ = 'voyage'
    voyage_id = Column(String)
    number = Column(String)
    environment_id = Column(String)
    embark_date = Column(DateTime)
    added_date = Column(TIMESTAMP, primary_key=True)

# Create a model for the table 'application_setting'
class ApplicationSetting(Base):
    __tablename__ = 'application_setting'
    application_setting_id = Column(String, primary_key=True)
    name = Column(String)
    value = Column(Integer)
    description = Column(String)