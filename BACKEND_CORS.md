# Backend CORS

Because GitHub Pages and the AI backend are different origins, the backend must permit the GitHub Pages origin.

Add FastAPI CORS middleware to the backend and allow your GitHub Pages origin, for example:

`https://YOUR-USERNAME.github.io`

For local testing you may also allow `http://localhost:5500`.

Required endpoints:
- `POST /api/assess`
- `POST /api/chat`
- `GET /health`
