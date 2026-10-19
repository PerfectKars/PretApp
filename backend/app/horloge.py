from datetime import UTC, datetime


def maintenant() -> datetime:
    """Heure serveur en UTC ; dépendance remplacée par une heure fixe en test."""
    return datetime.now(UTC)
