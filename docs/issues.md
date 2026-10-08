# Issues à publier après connexion GitHub

Identifiants locaux P01–P12 ; ce ne sont pas des numéros GitHub. Chaque issue a une branche courte et une PR avec problème, changement et validation. Ne pas créer d'issues artificielles pour remplir le calendrier.

| ID | Semaine | Titre | Condition de réussite / dépendance |
| --- | --- | --- | --- |
| P01 | 1 | Valider le socle et verrouiller les dépendances | Installation réelle, formatage, lint, test, build, Compose et CI verts ; exercice expliqué |
| P02 | 1 | Définir règles et modèle relationnel | Schéma équipements/comptes/réservations, clés et transitions expliqués ; P01 |
| P03 | 1 | Créer migration initiale et catalogue | Alembic upgrade depuis base vide, catalogue/détail avec données fictives ; P02 |
| P04 | 1 | Persister une demande de réservation | Validation dates et équipement, tests ; accès local provisoire ; P03 |
| P05 | 2 | Garantir disponibilité et concurrence | Migration GiST, périodes adjacentes, deux transactions concurrentes ; P04 |
| P06 | 2 | Valider/refuser/annuler avec transitions | Tests transitions interdites et conflits ; P05 |
| P07 | 3 | Ajouter comptes et authentification | Hash standard, expiration et tests identité ; P03 |
| P08 | 3 | Appliquer les permissions serveur | Matrice rôles/propriété testée, aucun rôle public privilégié ; P06/P07 |
| P09 | 3 | Construire les écrans du parcours | Catalogue, demande, décisions, chargement/erreurs, formulaires accessibles ; P08 |
| P10 | 3–4 | Enregistrer retraits/retours et historique | Double retrait bloqué, timestamps, retards et isolation par utilisateur ; P08/P09 |
| P11 | 4 | Vérifier intégration et installation | Scénario complet PostgreSQL, CI, clone propre, dépendances verrouillées ; P10 |
| P12 | 4 | Préparer démonstration et v1.0 | Vidéo fictive, limites, README final, exercices entretien et tous critères atteints ; P11 |
