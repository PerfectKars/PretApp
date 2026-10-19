from datetime import datetime
from enum import StrEnum

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Role(StrEnum):
    EMPRUNTEUR = "emprunteur"
    RESPONSABLE = "responsable"


class Statut(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    COLLECTED = "collected"
    RETURNED = "returned"


def _valeurs_sql(enum: type[StrEnum]) -> str:
    return ", ".join(f"'{membre.value}'" for membre in enum)


class Utilisateur(Base):
    __tablename__ = "utilisateur"
    __table_args__ = (CheckConstraint(f"role IN ({_valeurs_sql(Role)})", name="role"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(String(20))
    nom: Mapped[str] = mapped_column(String(100))
    prenom: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))

    # passive_deletes : l'ORM laisse la FK RESTRICT refuser la suppression
    # au lieu de vider reservation.utilisateur_id.
    reservations: Mapped[list[Reservation]] = relationship(
        back_populates="utilisateur", passive_deletes="all"
    )


class Equipement(Base):
    __tablename__ = "equipement"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    reservable: Mapped[bool] = mapped_column(default=True)

    # passive_deletes : l'ORM laisse la FK RESTRICT refuser la suppression
    # au lieu de vider reservation.equipement_id.
    reservations: Mapped[list[Reservation]] = relationship(
        back_populates="equipement", passive_deletes="all"
    )


class Reservation(Base):
    __tablename__ = "reservation"
    __table_args__ = (
        CheckConstraint(f"statut IN ({_valeurs_sql(Statut)})", name="statut"),
        CheckConstraint("fin > debut", name="fin_apres_debut"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    # RESTRICT : impossible de supprimer un utilisateur ou un équipement référencé.
    utilisateur_id: Mapped[int] = mapped_column(
        ForeignKey("utilisateur.id", ondelete="RESTRICT"), index=True
    )
    equipement_id: Mapped[int] = mapped_column(
        ForeignKey("equipement.id", ondelete="RESTRICT"), index=True
    )
    debut: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    fin: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    statut: Mapped[str] = mapped_column(String(20), default=Statut.PENDING)

    utilisateur: Mapped[Utilisateur] = relationship(back_populates="reservations")
    equipement: Mapped[Equipement] = relationship(back_populates="reservations")
