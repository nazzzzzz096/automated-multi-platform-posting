
import httpx

from app.config import settings


async def post_to_devto(message: str) -> dict:
    """Create a draft article on DEV.to."""

    if not settings.devto_api_key:
        raise ValueError(
            "DEV.to API key is not configured."
        )

    api_url = "https://dev.to/api/articles"

    headers = {
        "api-key": settings.devto_api_key,
        "Accept": "application/vnd.forem.api-v1+json",
        "User-Agent": "AutomatedMultiPlatformPosting/1.0",
    }

    payload = {
        "article": {
            "title": "Automated Multi-Platform Posting Test",
            "body_markdown": message,
            "published": False,
        }
    }

    async with httpx.AsyncClient(
        timeout=30.0,
        trust_env=True,
    ) as client:
        response = await client.post(
            api_url,
            headers=headers,
            json=payload,
        )

        response.raise_for_status()
        result = response.json()

    return {
        "platform": "devto",
        "status": "success",
        "article_id": result["id"],
        "posted_url": result.get("url"),
        "published": result.get("published"),
    }
