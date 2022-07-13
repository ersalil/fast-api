from database import Base, engine
from model import Item

print("Connecting to Data Base ... ")

Base.metadata.create_all(engine)