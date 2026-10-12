# PretApp

Projet personnel **en cours**, commencé le 12 octobre 2026. Cible : version 1.0 autour du 11 novembre. Application de prêts de matériel pour une association ou un club étudiant, sans commanditaire ni utilisateurs réels. Démonstrations avec données fictives. Développement accompagné par un assistant IA.

## État actuel

Socle en place : API FastAPI `/health` testée, interface React/TypeScript connectée via le proxy Vite, Ruff, ESLint, Prettier, CI GitHub Actions et Docker Compose. Aucune fonctionnalité métier implémentée pour l'instant. SQLAlchemy, Psycopg et Alembic sont déclarés ; modèles et migrations arrivent à l'étape suivante.

Docker Compose n'a pas encore été validé. Les dépendances transitives ne sont pas encore verrouillées.

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
npm install
npm run format
npm run dev
```

Ouvrir http://localhost:5173 : « API connectée » doit apparaître. API : http://localhost:8000/health, documentation : http://localhost:8000/docs. Vite transmet `/api/health` à `/health` : même origine pour le navigateur, sans configuration CORS inutile. Le frontend affiche aussi les erreurs HTTP, réponses inattendues et une indisponibilité après cinq secondes.

PostgreSQL n'est pas utilisé par `/health` : cette route mesure uniquement la vie de l'API. Aucun schéma ni jeu de données aujourd'hui. `.env` prépare la connexion future ; le backend actuel n'en a pas besoin.

## Docker Compose (développement)

Avec Docker Engine et le plugin Compose installés :

```bash
cp .env.example .env
docker compose config --quiet
docker compose up --build
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

Le test `/health` vérifie HTTP 200, type JSON et contrat exact. La compilation TypeScript et le build vérifient le frontend ; le parcours visuel et les erreurs restent à vérifier manuellement. La CI reprend ces commandes.

Après première installation réussie : committer `frontend/package-lock.json`, utiliser `npm ci` dans CI/Docker, générer des verrous Python complets (ex. pip-tools), puis installer ces verrous dans CI/Docker. Les installations actuelles ne garantissent pas encore une résolution transitive identique.

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
