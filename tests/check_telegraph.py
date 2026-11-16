
import asyncio

import httpx

from app.config import settings


async def main():
    """Verify the Telegraph access token."""

    if not settings.telegraph_access_token:
        print("Telegraph access token is missing.")
        return

    url = "https://api.telegra.ph/getAccountInfo"

    payload = {
        "access_token": settings.telegraph_access_token,
        "fields": ["short_name", "author_name"],
    }

    async with httpx.AsyncClient(
        timeout=20.0,
        trust_env=True,
    ) as client:
        response = await client.post(
            url,
            json=payload,
        )

    response.raise_for_status()
    result = response.json()

    if result.get("ok"):
        account = result["result"]

        print("Telegraph connection successful!")
        print("Account:", account["short_name"])
        print("Author:", account.get("author_name"))
    else:
        print("Verification failed:", result)


if __name__ == "__main__":
    asyncio.run(main())
