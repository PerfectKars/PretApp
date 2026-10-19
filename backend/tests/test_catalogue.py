from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Equipement, Utilisateur
from app.seed import inserer_donnees_fictives


def test_catalogue_vide(client: TestClient) -> None:
    reponse = client.get("/equipements")
    assert reponse.status_code == 200
    assert reponse.json() == []


def test_catalogue_liste_reservables_tries_par_nom(
    client: TestClient, session: Session
) -> None:
    session.add_all(
        [
            Equipement(nom="Trépied", description="Rotule fluide"),
            Equipement(nom="Casque VR", reservable=False),
            Equipement(nom="Appareil photo"),
        ]
    )
    session.flush()

    reponse = client.get("/equipements")

    assert reponse.status_code == 200
    assert [e["nom"] for e in reponse.json()] == ["Appareil photo", "Trépied"]
    assert set(reponse.json()[0]) == {"id", "nom", "description"}


def test_detail_equipement(client: TestClient, session: Session) -> None:
    equipement = Equipement(nom="Trépied", description="Rotule fluide")
    session.add(equipement)
    session.flush()

    reponse = client.get(f"/equipements/{equipement.id}")

    assert reponse.status_code == 200
    assert reponse.json() == {
        "id": equipement.id,
        "nom": "Trépied",
        "description": "Rotule fluide",
    }


def test_detail_equipement_retire_invisible(
    client: TestClient, session: Session
) -> None:
    equipement = Equipement(nom="Casque VR", reservable=False)
    session.add(equipement)
    session.flush()

    assert client.get(f"/equipements/{equipement.id}").status_code == 404


def test_detail_equipement_inexistant(client: TestClient) -> None:
    reponse = client.get("/equipements/999999")
    assert reponse.status_code == 404
    assert reponse.json() == {"detail": "Équipement introuvable"}


def test_identifiant_invalide(client: TestClient) -> None:
    assert client.get("/equipements/abc").status_code == 422


def test_donnees_fictives_sans_doublon(session: Session) -> None:
    premier = inserer_donnees_fictives(session)
    second = inserer_donnees_fictives(session)

    assert premier > 0
    assert second == 0
    lignes = sum(
        session.scalar(select(func.count()).select_from(modele))
        for modele in (Equipement, Utilisateur)
    )
    assert lignes == premier
