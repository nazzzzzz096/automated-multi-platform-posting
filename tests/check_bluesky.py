
import asyncio

import httpx

from app.config import settings


async def main():
    """Verify Bluesky authentication."""

    if not settings.bluesky_handle:
        print("Bluesky handle is missing.")
        return

    if not settings.bluesky_app_password:
        print("Bluesky app password is missing.")
        return

    url = (
        f"{settings.bluesky_pds_url.rstrip('/')}"
        "/xrpc/com.atproto.server.createSession"
    )

    payload = {
        "identifier": settings.bluesky_handle,
        "password": settings.bluesky_app_password,
    }

    async with httpx.AsyncClient(
        timeout=20.0,
        trust_env=True,
    ) as client:
        response = await client.post(
            url,
            json=payload,
        )

    if response.status_code == 200:
        account = response.json()

        print("Bluesky connection successful!")
        print("Handle:", account.get("handle"))
        print("DID:", account.get("did"))

    else:
        print("Verification failed:", response.status_code)
        print("Response:", response.text)


if __name__ == "__main__":
    asyncio.run(main())

