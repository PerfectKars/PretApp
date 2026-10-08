# Roadmap — 8 octobre au 8 novembre 2026

Trois à cinq sessions par semaine, ajustables. Chaque session : besoin et choix expliqués, exercice étudiant, vérification, commit réel, mise à jour du suivi. Aucun travail automatique entre les sessions. Les étapes ci-dessous sont du développement réel, pas une répartition artificielle de commits.

| Période | Sessions proposées | Livrable et validation |
| --- | --- | --- |
| S1 · 8–14 octobre | Socle ; démarrage et exercice ; règles et schéma ; migration et catalogue ; première demande | Catalogue et demande persistée, validations élémentaires, tests ; aucun endpoint métier public sans garde avant les comptes |
| S2 · 15–21 octobre | Intervalles ; contraintes concurrentes ; transitions ; validation/refus ; tests PostgreSQL | Conflits testés avec deux transactions concurrentes, statuts cohérents ; accès provisoire local uniquement |
| S3 · 22–28 octobre | Comptes et hash ; sessions et permissions ; catalogue UI ; demandes et espace responsable ; retrait/retour | Parcours de bout en bout avec deux rôles, tests refus d'accès ; données fictives |
| S4 · 29 octobre–8 novembre | Historique/retards ; intégration ; corrections/accessibilité ; installation depuis clone ; vidéo et explication | CI verte, installation reproductible vérifiée, limites et vidéo, tag v1.0 après critères satisfaits |

Les fondations d'authentification peuvent remonter si nécessaire, sans avancer tout le produit. Aucun parcours complet déclaré terminé avant la dernière semaine. En avance : exercices, cas limites, corrections, répétition d'entretien. En retard : enlever filtres, pagination avancée et embellissements ; conserver comptes, permissions, conflits et cycle jusqu'au retour. Marge : quelques jours après le 8 novembre.

## Définition de terminé

Demande → décision → retrait → retour ; conflits et permissions fiables ; tests métier et intégration pertinents ; CI verte ; lancement par une autre personne depuis README ; limites écrites ; vidéo courte de données fictives ; étudiant capable d'expliquer architecture, règles, tests et décisions.
