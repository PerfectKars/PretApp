from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Equipement, Reservation, Role, Statut, Utilisateur


@pytest.fixture
def acces_provisoire(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PRETAPP_ACCES_PROVISOIRE", "1")


@pytest.fixture
def emprunteur(session: Session) -> Utilisateur:
    utilisateur = Utilisateur(
        role=Role.EMPRUNTEUR,
        nom="Martin",
        prenom="Alex",
        email="alex.martin@example.test",
        password_hash="!",
    )
    session.add(utilisateur)
    session.flush()
    return utilisateur


@pytest.fixture
def equipement(session: Session) -> Equipement:
    equipement = Equipement(nom="Trépied")
    session.add(equipement)
    session.flush()
    return equipement


def _demande(
    client: TestClient,
    utilisateur: Utilisateur | None,
    corps: dict,
):
    entetes = {} if utilisateur is None else {"X-Utilisateur-Id": str(utilisateur.id)}
    return client.post("/reservations", json=corps, headers=entetes)


def _corps(equipement: Equipement, debut: datetime, duree: timedelta) -> dict:
    return {
        "equipement_id": equipement.id,
        "debut": debut.isoformat(),
        "fin": (debut + duree).isoformat(),
    }


# --- Cas accepté ---------------------------------------------------------------


@pytest.mark.usefixtures("acces_provisoire")
def test_demande_enregistree_en_attente(
    client: TestClient,
    session: Session,
    emprunteur: Utilisateur,
    equipement: Equipement,
) -> None:
    # 10 h à Paris le 2 novembre = UTC+1 (heure d'hiver) = 9 h UTC.
    corps = {
        "equipement_id": equipement.id,
        "debut": "2026-11-02T10:00:00+01:00",
        "fin": "2026-11-03T10:00:00+01:00",
    }

    reponse = _demande(client, emprunteur, corps)

    assert reponse.status_code == 201
    donnees = reponse.json()
    assert donnees["statut"] == "pending"
    assert donnees["debut"] == "2026-11-02T09:00:00Z"
    assert donnees["fin"] == "2026-11-03T09:00:00Z"
    reservation = session.get(Reservation, donnees["id"])
    assert reservation is not None
    assert reservation.utilisateur_id == emprunteur.id
    assert reservation.statut == Statut.PENDING


@pytest.mark.usefixtures("acces_provisoire")
def test_demandes_en_attente_qui_se_chevauchent_acceptees(
    client: TestClient,
    emprunteur: Utilisateur,
    equipement: Equipement,
    heure_serveur: datetime,
) -> None:
    corps = _corps(equipement, heure_serveur + timedelta(days=1), timedelta(days=2))

    assert _demande(client, emprunteur, corps).status_code == 201
    assert _demande(client, emprunteur, corps).status_code == 201


@pytest.mark.usefixtures("acces_provisoire")
@pytest.mark.parametrize(
    ("decalage", "duree"),
    [
        (timedelta(0), timedelta(hours=1)),  # début = maintenant
        (timedelta(days=1), timedelta(days=30)),  # exactement 30 jours
    ],
)
def test_limites_acceptees(
    client: TestClient,
    emprunteur: Utilisateur,
    equipement: Equipement,
    heure_serveur: datetime,
    decalage: timedelta,
    duree: timedelta,
) -> None:
    corps = _corps(equipement, heure_serveur + decalage, duree)
    assert _demande(client, emprunteur, corps).status_code == 201


# --- 401 : identité absente -------------------------------------------------------


def test_acces_provisoire_ferme_par_defaut(
    client: TestClient,
    emprunteur: Utilisateur,
    equipement: Equipement,
    heure_serveur: datetime,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("PRETAPP_ACCES_PROVISOIRE", raising=False)
    corps = _corps(equipement, heure_serveur + timedelta(days=1), timedelta(days=1))

    reponse = _demande(client, emprunteur, corps)

    assert reponse.status_code == 401
    assert reponse.json() == {"detail": "Identification requise"}


@pytest.mark.usefixtures("acces_provisoire")
def test_sans_identite(
    client: TestClient, equipement: Equipement, heure_serveur: datetime
) -> None:
    corps = _corps(equipement, heure_serveur + timedelta(days=1), timedelta(days=1))
    assert _demande(client, None, corps).status_code == 401


@pytest.mark.usefixtures("acces_provisoire")
def test_utilisateur_inconnu(
    client: TestClient, equipement: Equipement, heure_serveur: datetime
) -> None:
    corps = _corps(equipement, heure_serveur + timedelta(days=1), timedelta(days=1))
    reponse = client.post(
        "/reservations", json=corps, headers={"X-Utilisateur-Id": "999999"}
    )
    assert reponse.status_code == 401


@pytest.mark.usefixtures("acces_provisoire")
def test_identite_verifiee_avant_le_contenu(client: TestClient) -> None:
    """Un anonyme n'apprend rien sur les règles de validation."""
    assert _demande(client, None, {"debut": "pas une date"}).status_code == 401


# --- 404 : équipement absent ou non visible -------------------------------------


@pytest.mark.usefixtures("acces_provisoire")
def test_equipement_inexistant(
    client: TestClient, emprunteur: Utilisateur, heure_serveur: datetime
) -> None:
    corps = {
        "equipement_id": 999999,
        "debut": (heure_serveur + timedelta(days=1)).isoformat(),
        "fin": (heure_serveur + timedelta(days=2)).isoformat(),
    }
    assert _demande(client, emprunteur, corps).status_code == 404


@pytest.mark.usefixtures("acces_provisoire")
def test_equipement_retire(
    client: TestClient,
    session: Session,
    emprunteur: Utilisateur,
    heure_serveur: datetime,
) -> None:
    retire = Equipement(nom="Casque VR", reservable=False)
    session.add(retire)
    session.flush()
    corps = _corps(retire, heure_serveur + timedelta(days=1), timedelta(days=1))

    assert _demande(client, emprunteur, corps).status_code == 404


# --- 422 : données invalides -------------------------------------------------------


@pytest.mark.usefixtures("acces_provisoire")
@pytest.mark.parametrize(
    ("decalage", "duree", "message"),
    [
        (-timedelta(minutes=1), timedelta(hours=1), "dans le passé"),
        (timedelta(days=1), timedelta(0), "après le début"),
        (timedelta(days=1), -timedelta(hours=1), "après le début"),
        (timedelta(days=1), timedelta(days=30, seconds=1), "30 jours"),
    ],
    ids=["debut-passe", "fin-egale-debut", "fin-avant-debut", "plus-de-30-jours"],
)
def test_periode_invalide(
    client: TestClient,
    emprunteur: Utilisateur,
    equipement: Equipement,
    heure_serveur: datetime,
    decalage: timedelta,
    duree: timedelta,
    message: str,
) -> None:
    corps = _corps(equipement, heure_serveur + decalage, duree)

    reponse = _demande(client, emprunteur, corps)

    assert reponse.status_code == 422
    assert message in reponse.json()["detail"][0]["msg"]


@pytest.mark.usefixtures("acces_provisoire")
def test_date_sans_fuseau(
    client: TestClient, emprunteur: Utilisateur, equipement: Equipement
) -> None:
    corps = {
        "equipement_id": equipement.id,
        "debut": "2026-11-02T10:00:00",
        "fin": "2026-11-03T10:00:00",
    }

    reponse = _demande(client, emprunteur, corps)

    assert reponse.status_code == 422
    assert reponse.json()["detail"][0]["type"] == "timezone_aware"


@pytest.mark.usefixtures("acces_provisoire")
@pytest.mark.parametrize("champ", ["statut", "utilisateur_id"])
def test_champ_reserve_a_l_api_refuse(
    client: TestClient,
    emprunteur: Utilisateur,
    equipement: Equipement,
    heure_serveur: datetime,
    champ: str,
) -> None:
    """Le client ne peut ni s'auto-valider ni réserver au nom d'un autre."""
    corps = _corps(equipement, heure_serveur + timedelta(days=1), timedelta(days=1))
    corps[champ] = "approved" if champ == "statut" else emprunteur.id + 1

    reponse = _demande(client, emprunteur, corps)

    assert reponse.status_code == 422
    assert reponse.json()["detail"][0]["type"] == "extra_forbidden"


@pytest.mark.usefixtures("acces_provisoire")
def test_champ_manquant(client: TestClient, emprunteur: Utilisateur) -> None:
    reponse = _demande(client, emprunteur, {"equipement_id": 1})
    assert reponse.status_code == 422
