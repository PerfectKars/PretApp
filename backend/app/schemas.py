from pydantic import BaseModel, ConfigDict


class EquipementOut(BaseModel):
    """Ce que l'API expose d'un équipement ; découplé du modèle SQLAlchemy."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    nom: str
    description: str | None
