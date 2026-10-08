# Suivi des sessions

## 8 octobre 2026 — session 01

Objectif : uniquement socle et cadrage. Sources/configuration préparées avec assistance IA, aucune fonctionnalité métier. Étudiant : exercice encore à réaliser ; aucune compréhension supposée acquise.

Constats : dossier vide, aucune consigne locale ; Python 3.14.7, Node 26.10.0, npm 12.2.0 ; Docker absent ; GitHub gh avec authentification invalide ; .git en lecture seule. Registres PyPI/npm inaccessibles (erreur DNS). Aucun secret ni fichier privé ajouté. Auteur Git générique pour préserver l'adresse personnelle.

Livré : API /health et test HTTP, frontend connecté via proxy, configurations lint/format/CI/Compose, README, règles proposées, planning, issues locales, brouillon PR. Versions directes proposées, sans verrou transitif.

Validation exécutée : compilation syntaxique Python, lecture JSON de configuration, syntaxe shell/JS, diff Git sans erreurs d'espaces. Validation impossible ici : installation, pytest, Ruff, ESLint, Prettier, build, lancement web, Docker et CI. Ne pas merger le socle avant résolution de ces points.

### Exercice étudiant — 30 à 45 minutes

1. Installer et lancer les deux services selon README ; constater API connectée.
2. Expliquer avec ses mots `/api/health` vs `/health`, requête HTTP, réponse JSON et proxy. Lire main.py et test_health.py ; expliquer chaque assertion.
3. Arrêter l'API : observer l'erreur frontend ; redémarrer puis recharger.
4. Ajouter soi-même une assertion sur le schéma OpenAPI de `/health` (statut 200 et présence de la route), lancer pytest et expliquer sa valeur.
5. Exécuter formatage, lint et build ; partager les sorties utiles sans secrets.

Réussite : parcours réel et panne vérifiés, test ajouté et expliqué, vérifications vertes. Cet exercice fera son propre commit ; aucune contribution étudiante inventée aujourd'hui.

### Prochaine reprise

Lire ce fichier et git log. Traiter P01 d'abord : accès réseau, installation, correction versions si nécessaire, formatage, verrous, tests et Docker. Reconnecter GitHub personnel, créer dépôt public sans collision, publier branche et PR. Puis seulement P02 : revue des règles et exercice schéma relationnel. Ne pas développer les fonctionnalités complètes avant cette étape.

À chaque session suivante : date réelle, objectif limité, explication technique, partie réalisée par l'étudiant, vérifications et résultats, commit/PR, état et prochaine tâche. CV actuel : « PretApp — projet personnel en cours : préparation d'une application de prêts avec FastAPI, React/TypeScript et PostgreSQL ». Ne pas annoncer une application opérationnelle ou des utilisateurs réels.
