from http.client import HTTPException
from pyexpat import model
from telnetlib import STATUS
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from database import SessionLocal
import model
import uvicorn

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    description: str
    price: int
    on_offer: bool
    
    class Config:
        orm_mode = True

db = SessionLocal()

@app.get('/')
def index():
    return {'Salil': {'ROll no.': '19CS065'}}

@app.get('/items')
def get_all_items(id: int=1):
    return {'Salil': {'ROll no.': id}}


@app.get('/items/{item_id}', response_model=Item, status_code=200)
def get_an_item(item_id: int):
    item = db.query(model.Item).filter(model.Item.id == item_id).first()
    return item

@app.post('/items', response_model=Item, status_code=200)
def create_an_item():
    new_item = model.Item(name=Item.name, price=Item.price, desc=Item.description, offer=Item.on_offer)
    db_item=db.query(model.Item).filter(Item.name == new_item.name).first()

    if db_item is not None:
        raise HTTPException(status_code=400, details="The name is already registered!")

    db.add(new_item)
    db.commit()

    return new_item

@app.put('/item/{item_id}')
def update_an_item(item_id: int):
    return {'Salil': {'ROll no.': item_id}}

@app.delete('/item/{item_id}')
def delete_an_item(item_id: int):
    return {'Salil': {'ROll no.': item_id}}



@app.get('/blog')
def show(limit=10, published: bool=True, sort: Optional[str]= None):
    if not published:
        return {'Salil': f"You have {limit} blogs"}
    else:
        return "ERROR"

# @app.post('/co')
# def post_api(request: Blog):
    # return {'Salil': f"Data is {request.title}, {request.body} and {request.published_at}"}




# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)