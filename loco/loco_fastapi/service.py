import uvicorn
import os
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List
from decimal import Decimal
import loco.controller as controller

app = FastAPI()
app.version = 1.0


class Result(BaseModel):
    provider: str
    address: str
    lat: Decimal
    lon: Decimal


class SearchResult(BaseModel):
    Results: List[Result]


@app.get(
    "/v1/geocoding",
    response_model=SearchResult,
    responses={
        503: {
            "description": "Proxied services unaccessible"}})
async def search(*, address=Query(..., title="Address")):
    try:
        result = controller.search(address)
    except controller.NoGeoCodeServicesAvailable:
        raise HTTPException(
            status_code=503,
            detail="No proxied servies accessible at this moment")

    return {"Results": result}


@app.get("/v1/ping")
async def ping():
    return "pong"


def start():
    SERVICE_PORT = int(os.environ.get('SERVICE_PORT', 8000))
    uvicorn.run(app, host='0.0.0.0', port=SERVICE_PORT)
