
import httpx

from app.config import settings


async def post_to_mastodon(message: str) -> dict:
    """Publish a status to Mastodon."""

    if not settings.mastodon_instance_url:
        raise ValueError(
            "Mastodon instance URL is not configured."
        )

    if not settings.mastodon_access_token:
        raise ValueError(
            "Mastodon access token is not configured."
        )

    instance_url = settings.mastodon_instance_url.rstrip("/")
    api_url = f"{instance_url}/api/v1/statuses"

    headers = {
        "Authorization": (
            f"Bearer {settings.mastodon_access_token}"
        )
    }

    payload = {
        "status": message,
        "visibility": "public",
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(
            api_url,
            headers=headers,
            data=payload,
        )

        response.raise_for_status()
        result = response.json()

    return {
        "platform": "mastodon",
        "status": "success",
        "post_id": result["id"],
        "posted_url": result.get("url"),
    }
