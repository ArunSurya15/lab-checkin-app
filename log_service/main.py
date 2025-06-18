# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 17:45:48 2025

@author: aruni1
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

app = FastAPI()
engine = create_engine("sqlite:///logs.db", connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    person = Column(String)
    item = Column(String)
    action = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

class LogEntry(BaseModel):
    person: str
    item: str
    action: str

@app.post("/logs")
def create_log(entry: LogEntry):
    db = Session()
    log = Log(**entry.dict())
    db.add(log)
    db.commit()
    return {"status": "logged"}

@app.get("/logs/{person}", response_model=List[dict])
def get_logs(person: str):
    db = Session()
    logs = db.query(Log).filter_by(person=person).order_by(Log.timestamp.desc()).all()
    return [{"item": log.item, "action": log.action, "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S")} for log in logs]

