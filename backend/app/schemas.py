from datetime import UTC, datetime, timedelta

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    field_validator,
    model_validator,
)

DUREE_MAXIMALE = timedelta(days=30)


class EquipementOut(BaseModel):
    """Ce que l'API expose d'un équipement ; découplé du modèle SQLAlchemy."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    nom: str
    description: str | None


class ReservationIn(BaseModel):
    """Demande envoyée par le client : ni utilisateur, ni statut (fixés par l'API)."""

    # Un champ inconnu (`statut`, `utilisateur_id`...) est refusé, pas ignoré.
    model_config = ConfigDict(extra="forbid")

    equipement_id: int
    # AwareDatetime : une date sans fuseau est refusée (422).
    debut: AwareDatetime
    fin: AwareDatetime

    @field_validator("debut", "fin")
    @classmethod
    def en_utc(cls, valeur: datetime) -> datetime:
        return valeur.astimezone(UTC)

    @model_validator(mode="after")
    def periode_valide(self) -> ReservationIn:
        if self.fin <= self.debut:
            raise ValueError("La fin doit être après le début")
        if self.fin - self.debut > DUREE_MAXIMALE:
            raise ValueError("La durée maximale est de 30 jours")
        return self


class ReservationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    equipement_id: int
    debut: datetime
    fin: datetime
    statut: str
