from fastapi import FastAPI

from app.schemas import PostingRequest


app = FastAPI(
    title="Automated Multi-Platform Posting System",
    description=(
        "An API for publishing messages across "
        "multiple platforms."
    ),
    version="1.0.0",
)


@app.get("/")
async def home():
    """Check whether the API is running."""

    return {
        "success": True,
        "message": "Automated Posting API is running.",
    }


@app.post("/posting")
async def create_post(request: PostingRequest):
    """Receive and validate a message."""

    message = request.message

    return {
        "success": True,
        "status": "received",
        "message": "Message validated successfully.",
        "message_received": message,
        "character_count": len(message),
        "publishing_status": "Not published yet",
    }