# Règles proposées avant implémentation

Base de discussion pour la prochaine session ; aucune règle métier codée aujourd'hui.

- Un équipement représente un exemplaire physique, sans quantité multiple.
- Dates avec fuseau obligatoire, normalisées UTC. Affichage Europe/Paris. Intervalles `[début, fin)` : début inclus, fin exclue ; deux périodes adjacentes sont compatibles. Début >= heure serveur à la demande et fin > début ; pas de réservation rétroactive. Tests avec horloge contrôlée. Durée maximale proposée : 30 jours.
- Statuts : pending, approved, rejected, cancelled, collected, returned.
- pending ne bloque pas : plusieurs demandes peuvent coexister. approved et collected bloquent les périodes qui se chevauchent. rejected, cancelled et returned ne bloquent pas. La décision responsable revérifie toujours la disponibilité.
- Transitions : pending → approved/rejected (responsable) ; pending/approved → cancelled (propriétaire ou responsable, avant retrait) ; approved → collected (responsable, à partir du début et avant la fin) ; collected → returned (responsable). Terminaux : rejected, cancelled, returned. Pas d'édition des dates : annuler puis redemander.
- Retrait refusé si l'équipement est déjà physiquement sorti, même avec une période antérieure expirée. Un retard n'annule jamais automatiquement un prêt ni ne force un retour.
- Retard calculé : collected et heure serveur > fin ; pas un statut supplémentaire. Une réservation future peut exister pendant un prêt qui deviendra en retard ; son retrait sera bloqué jusqu'au retour réel. Cette limite est explicitée à l'utilisateur.
- Emprunteur : catalogue, ses demandes et son historique. Responsable : décisions, retraits, retours et historique global. Aucun rôle privilégié accepté depuis un formulaire public.
- Réponse 422 pour données invalides, 401 pour absence d'identité, 403 pour action interdite, 404 pour ressource absente ou non visible, 409 pour conflit métier. Erreurs sans détails internes ni mots de passe.

## Concurrence prévue en S2

PostgreSQL fait autorité : contrainte d'exclusion GiST combinant équipement et `tstzrange` pour approved/collected, via `btree_gist`. Transactions pour les changements d'état ; verrou sur l'équipement lors du retrait pour empêcher deux sorties simultanées. Toutes les actions concernées suivent le même ordre de verrouillage. Une violation traduit un conflit 409 après rollback. Test avec deux connexions PostgreSQL et transactions réellement concurrentes ; SQLite ne valide pas cette garantie.

## Sécurité prévue en S3

S'appuyer sur les mécanismes documentés FastAPI et une bibliothèque de hash Argon2id standard, sans cryptographie maison. Choisir et expliquer le mécanisme de session avant code ; traiter expiration, déconnexion et protection CSRF si cookies. Validation serveur, permissions par action, aucun mot de passe brut ni token dans logs/Git. Vérifier les documentations officielles à cette étape.
