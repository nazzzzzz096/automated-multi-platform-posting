
import asyncio

import httpx

from app.config import settings


async def main():
    """Verify Mastodon access token."""

    if not settings.mastodon_access_token:
        print("Mastodon access token is missing.")
        return

    instance_url = (
        settings.mastodon_instance_url.rstrip("/")
    )

    url = f"{instance_url}/api/v1/accounts/verify_credentials"

    headers = {
        "Authorization": (
            f"Bearer {settings.mastodon_access_token}"
        )
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(
            url,
            headers=headers,
        )

    if response.status_code == 200:
        account = response.json()

        print("Mastodon connection successful!")
        print("Username:", account["username"])
        print("Display name:", account["display_name"])
    else:
        print("Verification failed:", response.status_code)
        print("Response:", response.text)


if __name__ == "__main__":
    asyncio.run(main())
