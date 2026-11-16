# Automated Multi-Platform Posting System

A Python-based REST API built with **FastAPI** that automatically improves and publishes a single message across five platforms using their official APIs.

The application accepts a message containing exactly one URL, validates the input, uses Google Gemini to improve the message, and publishes it to all configured platforms independently.

## Features

- **FastAPI REST API:** A single endpoint for multi-platform publishing.
- **Input validation:** Enforces a 200-character limit and exactly one valid URL.
- **AI-powered message improvement:** Uses Google Gemini to improve grammar and readability while preserving the original meaning and URL.
- **Multi-platform publishing:** Integrates five third-party platforms.
- **Asynchronous execution:** Publishes to multiple platforms concurrently using `asyncio`.
- **Independent error handling:** A failure on one platform does not stop publishing to the others.
- **Detailed results:** Returns publishing status, content URL, public accessibility, date, time, and error information.
- **Secure configuration:** Stores API credentials in environment variables.

## Supported Platforms

| Platform | Integration | Purpose |
|---|---|---|
| Telegram | Telegram Bot API | Sends messages to a configured chat |
| Mastodon | Mastodon REST API | Publishes public statuses |
| Telegraph | Telegraph API | Creates public Telegraph pages |
| DEV.to | DEV.to API | Publishes articles |
| Bluesky | AT Protocol API | Creates feed posts |

## Technology Stack

- Python 3.x
- FastAPI
- Uvicorn
- Pydantic
- Pydantic Settings
- HTTPX
- Google Gemini API (`google-genai`)
- Pytest
- Ruff
- Black

## Project Structure

```text
automated-multi-platform-posting/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   ├── config.py
│   │
│   ├── platforms/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── telegram.py
│   │   ├── mastodon.py
│   │   ├── telegraph.py
│   │   ├── devto.py
│   │   └── bluesky.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── llm_service.py
│       └── posting_service.py
│
├── tests/
│   ├── test_posting.py
│   ├── test_llm_service.py
│   ├── check_telegram.py
│   ├── check_mastodon.py
│   ├── check_telegraph.py
│   ├── check_devto.py
│   ├── check_bluesky.py
│   └── ...
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## How It Works

The application follows this workflow:

1. The client submits a message to the `/posting` endpoint.
2. Pydantic validates the message.
3. The application checks that the message:
   - Is not empty.
   - Does not exceed 200 characters.
   - Contains exactly one valid URL.
4. Google Gemini improves the message while preserving its original meaning and URL.
5. The improved message is sent to all five platforms concurrently.
6. Each platform independently handles its API request and errors.
7. The API returns a consolidated response containing the result from each platform.

If Gemini fails to improve the message, the original message is used as a fallback when the service is configured to handle the failure.

## Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd automated-multi-platform-posting
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a reference.

Add the credentials for the platforms you want to use:

```env
# Google Gemini
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite

# Telegram
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

# Mastodon
MASTODON_INSTANCE_URL=https://mastodon.social
MASTODON_ACCESS_TOKEN=your_mastodon_access_token

# Telegraph
TELEGRAPH_ACCESS_TOKEN=your_telegraph_access_token

# DEV.to
DEVTO_API_KEY=your_devto_api_key

# Bluesky
BLUESKY_HANDLE=your_bluesky_handle
BLUESKY_APP_PASSWORD=your_bluesky_app_password
BLUESKY_PDS_URL=https://bsky.social
```

**Important:** Replace the example values with your own credentials. Never commit your `.env` file or share your API keys publicly.

The `.env.example` file can be committed with placeholder values.

## Running the Application

Start the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 4000
```

The API will be available at:

```text
http://localhost:4000
```

### Interactive API Documentation

Open the following URL in your browser:

```text
http://localhost:4000/docs
```

Use the Swagger UI to test the API endpoint.

## API Usage

### Endpoint

```http
POST /posting
```

### Request Body

```json
{
  "message": "Grow your business! https://example.com"
}
```

### Example Request Using cURL

```bash
curl -X POST "http://localhost:4000/posting" \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"Grow your business! https://example.com\"}"
```

### Sample Response

The following is an example of a successful publishing response from a live execution:

```json
{
  "success": true,
  "publishing_status": "success",
  "message": "Publishing process completed.",
  "original_message": "smarter ways to grow your business and improve your online presence. https://example.com",
  "improved_message": "Discover smarter ways to grow your business and improve your online presence. https://example.com",
  "character_count": 97,
  "total_platforms": 5,
  "successful_platforms": 5,
  "failed_platforms": 0,
  "results": [
    {
      "platform": "telegram",
      "status": "success",
      "posted_url": null,
      "public_access": false,
      "date": "2026-11-16",
      "time": "11:49:49.247485",
      "timezone": "UTC",
      "error": null
    },
    {
      "platform": "mastodon",
      "status": "success",
      "posted_url": "https://mastodon.social/@nazina/117625965111468973",
      "public_access": true,
      "date": "2026-11-16",
      "time": "11:49:49.069772",
      "timezone": "UTC",
      "error": null
    },
    {
      "platform": "telegraph",
      "status": "success",
      "posted_url": "https://telegra.ph/Automated-Social-Media-Update-11-16-4",
      "public_access": true,
      "date": "2026-11-16",
      "time": "11:49:49.069511",
      "timezone": "UTC",
      "error": null
    },
    {
      "platform": "devto",
      "status": "success",
      "posted_url": "https://dev.to/nazina_n_1d96e4a84a2947a4/automated-multi-platform-posting-403a",
      "public_access": true,
      "date": "2026-11-16",
      "time": "11:49:48.844626",
      "timezone": "UTC",
      "error": null
    },
    {
      "platform": "bluesky",
      "status": "success",
      "posted_url": "https://bsky.app/profile/nazi01.bsky.social/post/3n2ghk3yypc2f",
      "public_access": true,
      "date": "2026-11-16",
      "time": "11:49:49.910792",
      "timezone": "UTC",
      "error": null
    }
  ]
}
```

**Note:** Telegram publishing in this implementation targets a configured chat. Therefore, its result may not include a public URL, and `public_access` is reported as `false`.

The API uses the following overall publishing statuses:

| Status | Meaning |
|---|---|
| `success` | All platforms published successfully |
| `partial_success` | At least one platform succeeded and another failed |
| `failed` | All platform publishing attempts failed |

The individual platform results contain the outcome of each publishing attempt.

## Testing

Run the automated test suite:

```bash
python -m pytest -q
```

Run code-quality checks:

```bash
ruff check app/ tests/
```

Check code formatting:

```bash
black --check app/ tests/
```

The automated tests cover successful message processing and invalid input scenarios, including:

- Messages without a URL.
- Messages containing multiple URLs.
- Messages exceeding the character limit.
- Successful API processing using mocked publishing services.

Some `check_*.py` scripts are manual integration checks. Be aware that publishing checks can create real content on external platforms.

## API Documentation and References

The integrations use the following official API documentation:

1. **Telegram Bot API:** https://core.telegram.org/bots/api
2. **Mastodon API:** https://docs.joinmastodon.org/methods/statuses/
3. **Telegraph API:** https://telegra.ph/api
4. **DEV.to API:** https://developers.forem.com/api
5. **Bluesky AT Protocol:** https://docs.bsky.app/
6. **Google Gemini API:** https://ai.google.dev/gemini-api/docs

## Security Considerations

- API credentials are stored in environment variables.
- The `.env` file is excluded through `.gitignore`.
- The `.env.example` file contains placeholders only.
- API credentials should never be hardcoded into source files.
- Publishing errors are logged for troubleshooting.
- Public publishing actions should be tested carefully to avoid duplicate posts.

## Future Improvements

- Add configurable platform selection.
- Improve retry and timeout handling.
- Add structured logging and monitoring.
- Introduce persistent publishing history.
- Add more platform integrations.
- Improve URL validation and CTA detection.

## Author

**Developed as part of the Python Practical Test for Dxora Technologies / Chivox AI.**

---

**Project:** Automated Multi-Platform Posting System  
**Framework:** FastAPI  
**Language:** Python  
**Submission:** Python Practical Test – 2026
