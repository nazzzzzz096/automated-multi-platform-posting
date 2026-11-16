
import json
import re

import httpx

from app.config import settings


def create_content_nodes(message: str) -> list:
    """Convert a message into Telegraph content nodes."""

    url_pattern = r"https?://[^\s<>]+"
    match = re.search(url_pattern, message)

    if not match:
        return [
            {
                "tag": "p",
                "children": [message],
            }
        ]

    url = match.group()
    clean_url = url.rstrip(".,!?;:)")

    start = match.start()
    end = start + len(clean_url)

    children = []

    if start > 0:
        children.append(message[:start])

    children.append({
        "tag": "a",
        "attrs": {"href": clean_url},
        "children": [clean_url],
    })

    if end < len(message):
        children.append(message[end:])

    return [
        {
            "tag": "p",
            "children": children,
        }
    ]


async def post_to_telegraph(message: str) -> dict:
    """Publish a message as a Telegraph page."""

    if not settings.telegraph_access_token:
        raise ValueError(
            "Telegraph access token is not configured."
        )

    content = create_content_nodes(message)

    payload = {
        "access_token": settings.telegraph_access_token,
        "title": "Automated Social Media Update",
        "content": json.dumps(content),
        "return_content": "false",
    }

    url = "https://api.telegra.ph/createPage"

    async with httpx.AsyncClient(
        timeout=30.0,
        trust_env=True,
    ) as client:
        response = await client.post(
            url,
            data=payload,
        )

        response.raise_for_status()
        result = response.json()

    if not result.get("ok"):
        raise RuntimeError(
            result.get(
                "error",
                "Telegraph publishing failed.",
            )
        )

    page = result["result"]

    return {
        "platform": "telegraph",
        "status": "success",
        "page_path": page["path"],
        "posted_url": page["url"],
    }
