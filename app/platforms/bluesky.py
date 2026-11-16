
from datetime import datetime, timezone

import httpx

from app.config import settings


async def post_to_bluesky(message: str) -> dict:
    """Publish a post to Bluesky."""

    if not settings.bluesky_handle:
        raise ValueError(
            "Bluesky handle is not configured."
        )

    if not settings.bluesky_app_password:
        raise ValueError(
            "Bluesky app password is not configured."
        )

    base_url = settings.bluesky_pds_url.rstrip("/")

    session_url = (
        f"{base_url}/xrpc/com.atproto.server.createSession"
    )

    session_payload = {
        "identifier": settings.bluesky_handle,
        "password": settings.bluesky_app_password,
    }

    async with httpx.AsyncClient(
        timeout=30.0,
        trust_env=True,
    ) as client:
        session_response = await client.post(
            session_url,
            json=session_payload,
        )

        session_response.raise_for_status()
        session = session_response.json()

        post_url = (
            f"{base_url}/xrpc/com.atproto.repo.createRecord"
        )

        post_payload = {
            "repo": session["did"],
            "collection": "app.bsky.feed.post",
            "record": {
                "$type": "app.bsky.feed.post",
                "text": message,
                "createdAt": datetime.now(
                    timezone.utc
                ).isoformat().replace("+00:00", "Z"),
            },
        }

        headers = {
            "Authorization": (
                f"Bearer {session['accessJwt']}"
            )
        }

        post_response = await client.post(
            post_url,
            headers=headers,
            json=post_payload,
        )

        post_response.raise_for_status()
        result = post_response.json()

    post_id = result["uri"].split("/")[-1]

    posted_url = (
        f"https://bsky.app/profile/"
        f"{session['handle']}/post/{post_id}"
    )

    return {
        "platform": "bluesky",
        "status": "success",
        "post_id": post_id,
        "posted_url": posted_url,
    }
