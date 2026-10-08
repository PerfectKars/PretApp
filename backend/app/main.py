from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="PretApp", version="0.0.1")


class HealthResponse(BaseModel):
    status: Literal["ok"]


@app.get("/health", response_model=HealthResponse, tags=["Infrastructure"])
def health() -> HealthResponse:
    """Confirme que l'API répond ; ne vérifie pas encore PostgreSQL."""
    return HealthResponse(status="ok")
