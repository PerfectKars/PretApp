from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

from app.catalogue import router as catalogue_router
from app.reservations import router as reservations_router

app = FastAPI(title="PretApp", version="0.0.1")
app.include_router(catalogue_router)
app.include_router(reservations_router)


class HealthResponse(BaseModel):
    status: Literal["ok"]


@app.get("/health", response_model=HealthResponse, tags=["Infrastructure"])
def health() -> HealthResponse:
    """Confirme que l'API répond ; ne vérifie pas encore PostgreSQL."""
    return HealthResponse(status="ok")
