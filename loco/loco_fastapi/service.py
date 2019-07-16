import uvicorn
import os
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
from decimal import Decimal
import loco.controller as controller

app = FastAPI()
SERVICE_PORT = int(os.environ.get('SERVICE_PORT',8000))

class Result(BaseModel):
    provider: str
    address: str
    lat: Decimal
    lon: Decimal

class SearchResult(BaseModel):
    Results:List[Result]

@app.get("/geocoding",response_model=SearchResult)
async def search(*, address= Query(...,title="Address")):
    result = controller.search(address)
    return {"Results":result}

@app.get("/ping")
async def ping():
    return "pong"

def start():
    uvicorn.run(app, host='0.0.0.0', port=SERVICE_PORT)