"""Données fictives de démonstration : `python -m app.seed`."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Equipement

EQUIPEMENTS = [
    ("Appareil photo hybride", "Boîtier et objectif 24-70 mm, deux batteries."),
    ("Trépied vidéo", "Rotule fluide, hauteur maximale 1,6 m."),
    ("Micro-cravate sans fil", "Deux émetteurs, un récepteur USB-C."),
    ("Vidéoprojecteur portable", "Full HD, entrée HDMI, sacoche fournie."),
    ("Ordinateur portable de prêt", None),
    ("Casque de réalité virtuelle", "Ancien modèle, retiré du prêt."),
]
# Le dernier reste en base pour l'historique mais n'est plus réservable.
RETIRES = {"Casque de réalité virtuelle"}


def inserer_donnees_fictives(session: Session) -> int:
    """Ajoute les équipements absents ; relancer le script ne crée pas de doublon."""
    existants = set(session.scalars(select(Equipement.nom)))
    nouveaux = [
        Equipement(nom=nom, description=description, reservable=nom not in RETIRES)
        for nom, description in EQUIPEMENTS
        if nom not in existants
    ]
    session.add_all(nouveaux)
    session.commit()
    return len(nouveaux)


if __name__ == "__main__":
    with SessionLocal() as session:
        print(f"{inserer_donnees_fictives(session)} équipement(s) ajouté(s).")
