
A single FastAPI process serves both the JSON API and the compiled React
presentation layer. No separate frontend server, bundler, or build step is
required — React is loaded via CDN and transpiled in-browser with Babel
standalone directly inside `templates/index.html`.

## Project Structure

```
aurvia-screening-app/
├── app.py              # FastAPI engine: /api/threshold + static asset mount
├── templates/
│   └── index.html      # React UI (CDN React + Babel standalone, no build tools)
├── requirements.txt    # fastapi, uvicorn, pydantic, pandas
└── README.md
```

## How to Run (single terminal command)

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Then open **http://127.0.0.1:8000/** in your browser. The same server
process handles both the UI and the API — there is no separate frontend
port to open.

## API

### `POST /api/threshold`

**Request body**

```json
{
  "stream_values": [10, 15, 22, 19, 8],
  "max_variance": 5
}
```

**Response body (200)**

```json
{
  "average": 14.8,
  "status": "STABLE",
  "max_variance": 5,
  "count": 5
}
```

- `status` is `"CRITICAL"` if any single value in `stream_values` deviates
  from the mean of the array by more than `max_variance`; otherwise it is
  `"STABLE"`.
- Invalid input — non-numeric values, an empty array, a missing field, or
  a malformed/blank request body — always returns a clean **HTTP 400**
  with a JSON `detail` message. The server never surfaces a raw Python
  500 traceback for dirty input.

## Frontend Behavior

- Text input accepts comma-separated numbers (e.g. `10, 15, 22, 19, 8`),
  tolerating extra spaces and trailing commas.
- A numeric field configures `max_variance`.
- "Check Metrics" calls `fetch('/api/threshold')` and is **disabled while
  the request is pending**, preventing duplicate/overlapping requests from
  rapid double-clicks.
- On success: a green **STABLE** badge or a red **CRITICAL** badge is
  rendered with the computed average, variance, and point count.
- On failure (400 or network error): a red error message box is shown
  instead of a raw crash.

## Design Notes

- `app.mount("/", StaticFiles(directory="templates", html=True))` is
  registered **after** the `/api/threshold` route so the exact-path API
  route always takes precedence over the catch-all static mount for that
  path, while `/` still serves `index.html` directly.
- A `RequestValidationError` handler converts Pydantic's default 422
  responses into the required 400 responses.
- A catch-all `Exception` handler is included as a safety net so no
  unexpected server-side error can leak a raw 500 traceback to the client.# Threshold Verification — Unified Single-App Prototype

