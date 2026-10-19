import os
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import Utilisateur

NON_IDENTIFIE = HTTPException(status.HTTP_401_UNAUTHORIZED, "Identification requise")


def acces_provisoire_actif() -> bool:
    return os.environ.get("PRETAPP_ACCES_PROVISOIRE") == "1"


def utilisateur_courant(
    session: Annotated[Session, Depends(get_session)],
    x_utilisateur_id: Annotated[int | None, Header()] = None,
) -> Utilisateur:
    """Seul point qui répond à « qui fait la requête ? ».

    Provisoire, en attendant les comptes : l'identifiant vient de l'en-tête
    `X-Utilisateur-Id`, et seulement si `PRETAPP_ACCES_PROVISOIRE=1`. Fermé par
    défaut. Sera remplacé par l'authentification sans changer les routes.
    """
    if not acces_provisoire_actif() or x_utilisateur_id is None:
        raise NON_IDENTIFIE
    utilisateur = session.get(Utilisateur, x_utilisateur_id)
    if utilisateur is None:
        raise NON_IDENTIFIE
    return utilisateur
