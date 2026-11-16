
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_valid_message():
    response = client.post(
        "/posting",
        json={
            "message": "Grow your business! https://example.com"
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True


def test_message_without_url():
    response = client.post(
        "/posting",
        json={
            "message": "Grow your business with us!"
        },
    )

    assert response.status_code == 422


def test_message_with_two_urls():
    response = client.post(
        "/posting",
        json={
            "message": (
                "Visit https://example.com "
                "and https://example.org"
            )
        },
    )

    assert response.status_code == 422


def test_message_exceeds_character_limit():
    response = client.post(
        "/posting",
        json={
            "message": "A" * 201 + " https://example.com"
        },
    )

    assert response.status_code == 422
