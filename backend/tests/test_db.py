from __future__ import annotations

from app.core.db import check_database, get_settings


def test_check_database_bad_url_returns_unavailable(monkeypatch) -> None:
    """A wrong DATABASE_URL must yield status=unavailable, never raise."""
    get_settings.cache_clear()
    monkeypatch.setenv(
        "DATABASE_URL", "postgresql://nope:nope@127.0.0.1:1/landmarket"
    )
    result = check_database()

    assert result["status"] == "unavailable"
    assert result["postgis_version"] is None
    assert isinstance(result["error"], str) and result["error"]
