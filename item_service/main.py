# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 17:45:29 2025

@author: aruni1
"""

# microservices_demo_fastapi/
# ├── item_service/
# │   ├── main.py
# │   └── items.db
# ├── log_service/
# │   ├── main.py
# │   └── logs.db
# └── test_client.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()
engine = create_engine("sqlite:///items.db", connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    total = Column(Integer)
    available = Column(Integer)

Base.metadata.create_all(engine)

# --- TEMP: Add dummy items only once ---
db = Session()
if db.query(Item).count() == 0:
    db.add_all([
        Item(name="Pen", total=10, available=10),
        Item(name="Notebook", total=5, available=5),
    ])
    db.commit()
db.close()


@app.get("/items", response_model=List[dict])
def get_items():
    db = Session()
    items = db.query(Item).all()
    return [{"id": i.id, "name": i.name, "total": i.total, "available": i.available} for i in items]

@app.post("/items/{item_id}/checkout")
def checkout(item_id: int):
    db = Session()
    item = db.query(Item).get(item_id)
    if not item or item.available <= 0:
        raise HTTPException(status_code=400, detail="Item not available")
    item.available -= 1
    db.commit()
    return {"item": item.name}

@app.post("/items/{item_id}/checkin")
def checkin(item_id: int):
    db = Session()
    item = db.query(Item).get(item_id)
    if not item or item.available >= item.total:
        raise HTTPException(status_code=400, detail="Cannot checkin")
    item.available += 1
    db.commit()
    return {"item": item.name}