from datetime import UTC, datetime, timedelta

import pytest
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import Base
from app.models import Equipement, Reservation, Role, Utilisateur


def test_migrations_correspondent_aux_modeles(engine: Engine) -> None:
    """Un modèle modifié sans nouvelle migration fait échouer ce test."""
    with engine.connect() as connexion:
        differences = compare_metadata(
            MigrationContext.configure(connexion), Base.metadata
        )
    assert differences == []


def _reservation(session: Session, debut: datetime, fin: datetime) -> Reservation:
    utilisateur = Utilisateur(
        role=Role.EMPRUNTEUR,
        nom="Martin",
        prenom="Alex",
        email="alex.martin@example.test",
        password_hash="hash-fictif",
    )
    equipement = Equipement(nom="Trépied")
    return Reservation(
        utilisateur=utilisateur, equipement=equipement, debut=debut, fin=fin
    )


def test_base_refuse_fin_avant_debut(session: Session) -> None:
    debut = datetime(2026, 11, 2, tzinfo=UTC)
    session.add(_reservation(session, debut, debut - timedelta(hours=1)))
    with pytest.raises(IntegrityError, match="ck_reservation_fin_apres_debut"):
        session.flush()


def test_base_refuse_role_inconnu(session: Session) -> None:
    session.add(
        Utilisateur(
            role="admin",
            nom="X",
            prenom="Y",
            email="x@example.test",
            password_hash="hash-fictif",
        )
    )
    with pytest.raises(IntegrityError, match="ck_utilisateur_role"):
        session.flush()


def test_base_refuse_suppression_equipement_reserve(session: Session) -> None:
    debut = datetime(2026, 11, 2, tzinfo=UTC)
    reservation = _reservation(session, debut, debut + timedelta(days=1))
    session.add(reservation)
    session.flush()
    session.delete(reservation.equipement)
    with pytest.raises(IntegrityError, match="fk_reservation_equipement_id"):
        session.flush()
