from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import Equipement
from app.schemas import EquipementOut

router = APIRouter(prefix="/equipements", tags=["Catalogue"])

SessionDep = Annotated[Session, Depends(get_session)]


@router.get("", response_model=list[EquipementOut])
def lister_equipements(session: SessionDep) -> list[Equipement]:
    """Liste les équipements réservables, triés par nom."""
    requete = (
        select(Equipement)
        .where(Equipement.reservable)
        .order_by(Equipement.nom, Equipement.id)
    )
    return list(session.scalars(requete))


@router.get("/{equipement_id}", response_model=EquipementOut)
def detail_equipement(equipement_id: int, session: SessionDep) -> Equipement:
    """Détail d'un équipement ; 404 s'il n'existe pas ou n'est plus réservable."""
    equipement = session.get(Equipement, equipement_id)
    if equipement is None or not equipement.reservable:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Équipement introuvable")
    return equipement
