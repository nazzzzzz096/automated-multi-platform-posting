import asyncio

import httpx

from app.config import settings


async def main():
    """Verify the DEV.to API key."""

    if not settings.devto_api_key:
        print("DEV.to API key is missing.")
        return

    url = "https://dev.to/api/users/me"

    headers = {
        "api-key": settings.devto_api_key,
        "Accept": "application/vnd.forem.api-v1+json",
        "User-Agent": "AutomatedMultiPlatformPosting/1.0",
    }

    async with httpx.AsyncClient(
        timeout=20.0,
        trust_env=True,
    ) as client:
        response = await client.get(
            url,
            headers=headers,
        )

    if response.status_code == 200:
        user = response.json()

        print("DEV.to connection successful!")
        print("Username:", user.get("username"))
        print("Name:", user.get("name"))
    else:
        print("Verification failed:", response.status_code)
        print("Response:", response.text)


if __name__ == "__main__":
    asyncio.run(main())
