from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session

from app.db import get_session
from app.horloge import maintenant
from app.identite import utilisateur_courant
from app.models import Equipement, Reservation, Statut, Utilisateur
from app.schemas import ReservationIn, ReservationOut

router = APIRouter(prefix="/reservations", tags=["Réservations"])


@router.post("", response_model=ReservationOut, status_code=status.HTTP_201_CREATED)
def demander_reservation(
    demande: ReservationIn,
    session: Annotated[Session, Depends(get_session)],
    utilisateur: Annotated[Utilisateur, Depends(utilisateur_courant)],
    heure_serveur: Annotated[datetime, Depends(maintenant)],
) -> Reservation:
    """Enregistre une demande `pending`. Ne bloque pas l'équipement : seule une
    réservation validée le fera."""
    if demande.debut < heure_serveur:
        # Même format que les erreurs Pydantic : un seul format côté client.
        raise RequestValidationError(
            [
                {
                    "type": "value_error",
                    "loc": ("body", "debut"),
                    "msg": "Le début ne peut pas être dans le passé",
                    "input": demande.debut.isoformat(),
                }
            ]
        )

    equipement = session.get(Equipement, demande.equipement_id)
    if equipement is None or not equipement.reservable:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Équipement introuvable")

    reservation = Reservation(
        utilisateur=utilisateur,
        equipement=equipement,
        debut=demande.debut,
        fin=demande.fin,
        statut=Statut.PENDING,
    )
    session.add(reservation)
    session.commit()
    return reservation
