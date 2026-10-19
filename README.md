# PretApp

Projet personnel **en cours**, commencé le 12 octobre 2026. Cible : version 1.0 autour du 11 novembre. Application de prêts de matériel pour une association ou un club étudiant, sans commanditaire ni utilisateurs réels. Démonstrations avec données fictives. Développement accompagné par un assistant IA.

## État actuel

Socle en place : API FastAPI `/health` testée, interface React/TypeScript connectée via le proxy Vite, Ruff, ESLint, Prettier, CI GitHub Actions et Docker Compose. Schéma PostgreSQL créé par une migration Alembic (modèles SQLAlchemy, contraintes décrites dans `docs/data-model.md`). Catalogue en lecture seule : `GET /equipements` et `GET /equipements/{id}`, alimenté par des données fictives. Réservations, comptes et interface métier à venir. Toutes les dépendances sont verrouillées (`package-lock.json`, `requirements*.txt`).

## Lancer en local

Prérequis : Python 3.14, Node 24 LTS et npm. Python 3.14 utilise Pydantic v2. Node 26 détecté dans l'environnement initial ; Node 24 retenu pour CI et conteneurs.

Depuis la racine :

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements-dev.txt
cp .env.example .env
cd backend
../.venv/bin/python -m uvicorn app.main:app --reload
```

Dans un autre terminal, depuis la racine :

```bash
cd frontend
npm ci
npm run format
npm run dev
```

Ouvrir http://localhost:5173 : « API connectée » doit apparaître. API : http://localhost:8000/health, documentation : http://localhost:8000/docs. Vite transmet `/api/health` à `/health` : même origine pour le navigateur, sans configuration CORS inutile. Le frontend affiche aussi les erreurs HTTP, réponses inattendues et une indisponibilité après cinq secondes.

Le catalogue a besoin de PostgreSQL ; le plus simple est de lancer uniquement la base avec Docker, puis de créer le schéma et les données fictives, depuis `backend` :

```bash
docker compose up -d db
../.venv/bin/alembic upgrade head
../.venv/bin/python -m app.seed
```

`alembic upgrade head` applique toutes les migrations ; `alembic downgrade -1` annule la dernière. Le script de données fictives peut être relancé sans créer de doublon. Le backend lit `DATABASE_URL` dans l'environnement ; sans variable, il utilise l'adresse locale de `.env.example`. `/health` ne dépend pas de PostgreSQL : cette route mesure uniquement la vie de l'API.

## Docker Compose (développement)

Avec Docker Engine et le plugin Compose installés :

```bash
cp .env.example .env
docker compose config --quiet
docker compose up --build
```

Dans un autre terminal, au premier lancement :

```bash
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.seed
```

Mêmes adresses que ci-dessus. Les trois services sont backend, frontend et PostgreSQL 17 ; la base attendue est saine avant démarrage du backend. Frontend servi par Vite pour le développement, pas un déploiement de production. Identifiants de démonstration uniquement. Arrêt : `docker compose down` ; les données restent dans le volume. Ne pas ajouter `-v` si l'on veut conserver les données.

## Vérifier

```bash
.venv/bin/ruff check backend
.venv/bin/ruff format --check backend
cd backend
../.venv/bin/python -m pytest
```

Depuis `frontend` :

```bash
npm run lint
npm run format:check
npm run build
```

Les tests ont besoin de PostgreSQL (`docker compose up -d db`). Ils utilisent une base séparée, `pretapp_test`, créée si besoin et remise à zéro par les migrations à chaque lancement ; chaque test est annulé à la fin (transaction). `TEST_DATABASE_URL` permet de choisir une autre base. Ils vérifient `/health`, le catalogue, les contraintes de la base et l'accord entre modèles et migrations. La compilation TypeScript et le build vérifient le frontend ; le parcours visuel et les erreurs restent à vérifier manuellement. La CI reprend ces commandes.

## Dépendances

Les versions exactes sont verrouillées, dépendances transitives comprises, pour que chaque installation (poste, CI, Docker) soit identique.

- Python : les dépendances directes se modifient dans `backend/requirements.in` (production) et `backend/requirements-dev.in` (outils de développement). Les fichiers `.txt` sont générés avec pip-tools, ne pas les éditer à la main :

  ```bash
  cd backend
  ../.venv/bin/pip-compile --strip-extras requirements.in
  ../.venv/bin/pip-compile --strip-extras requirements-dev.in
  ```

- JavaScript : `npm install <paquet>` met à jour `package-lock.json` ; `npm ci` installe exactement ce qu'il contient.

## Organisation

- `backend/app` : API ; `backend/tests` : tests pytest.
- `frontend/src` : interface minimale ; `compose.yaml` : environnement local.
- [Règles métier proposées](docs/rules.md).
- Hors périmètre : paiements, mobile, IA, multi-associations, emails et cloud complexe.

## Sources officielles consultées le 8 octobre 2026

- [FastAPI : versions et Python 3.14](https://fastapi.tiangolo.com/release-notes/)
- [Vite 7 : Node requis](https://vite.dev/blog/announcing-vite7)
- [Versions React](https://react.dev/versions), [Node LTS](https://nodejs.org/en/about/previous-releases)
- [SQLAlchemy 2 et Psycopg 3](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)
- [Versions SQLAlchemy](https://www.sqlalchemy.org/download.html), [Alembic](https://alembic.sqlalchemy.org/en/latest/front.html)
- [Installation Psycopg](https://www.psycopg.org/psycopg3/docs/basic/install.html), [Ruff](https://docs.astral.sh/ruff/installation/)
- [PostgreSQL : intervalles et exclusion](https://www.postgresql.org/docs/17/rangetypes.html)

Ces sources étayent les familles compatibles ; les patches et leur résolution complète restent à confirmer par installation et tests.
