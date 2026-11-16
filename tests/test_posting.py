from fastapi.testclient import TestClient

import app.main as main_module
from app.main import app

client = TestClient(app)


def test_valid_message(monkeypatch):
    """Test successful message validation and publishing."""

    async def mock_improve_message(message):
        return message.replace(
            "Grow your business!",
            "Grow your business.",
        )

    async def mock_publish_to_all_platforms(message):
        platforms = [
            "telegram",
            "mastodon",
            "telegraph",
            "devto",
            "bluesky",
        ]

        return [
            {
                "platform": platform,
                "status": "success",
                "posted_url": None,
                "public_access": False,
                "date": "2026-11-16",
                "time": "12:00:00",
                "timezone": "UTC",
                "error": None,
            }
            for platform in platforms
        ]

    monkeypatch.setattr(
        main_module,
        "improve_message",
        mock_improve_message,
    )

    monkeypatch.setattr(
        main_module,
        "publish_to_all_platforms",
        mock_publish_to_all_platforms,
    )

    response = client.post(
        "/posting",
        json={"message": "Grow your business! https://example.com"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["publishing_status"] == "success"
    assert data["total_platforms"] == 5
    assert data["successful_platforms"] == 5
    assert data["failed_platforms"] == 0

    assert data["improved_message"] == ("Grow your business. https://example.com")


def test_message_without_url():
    """Test rejection of a message without a URL."""

    response = client.post(
        "/posting",
        json={"message": "Grow your business with us!"},
    )

    assert response.status_code == 422


def test_message_with_two_urls():
    """Test rejection of a message containing two URLs."""

    response = client.post(
        "/posting",
        json={"message": ("Visit https://example.com " "and https://example.org")},
    )

    assert response.status_code == 422


def test_message_exceeds_character_limit():
    """Test rejection of a message exceeding 200 characters."""

    response = client.post(
        "/posting",
        json={"message": "A" * 201 + " https://example.com"},
    )

    assert response.status_code == 422
