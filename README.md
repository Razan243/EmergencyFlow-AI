# EmergencyFlow AI — NightShift MD

Custom GitHub Pages frontend for the EmergencyFlow AI multi-agent emergency triage project.

## Architecture

- GitHub Pages hosts the custom `index.html` website.
- The existing AI backend exposes `POST /api/assess`, `POST /api/chat`, and `GET /health`.
- The frontend sends PDF assessment and chat requests to the backend.

## GitHub Pages

1. Create a repository such as `EmergencyFlow-AI`.
2. Upload `index.html`, `README.md`, `.gitignore`, and `.nojekyll`.
3. Open **Settings → Pages**.
4. Select **Deploy from a branch → main → /(root)**.
5. Save.

The website URL will look like:

`https://YOUR-USERNAME.github.io/EmergencyFlow-AI/`

## Backend

The frontend is currently configured to use:

`https://razangewaily-nightshift-md-medicore-ai.hf.space`

The backend must allow CORS requests from the GitHub Pages origin.

Do not put API keys or secrets in this repository.

## Purpose

EmergencyFlow AI is an educational decision-support prototype and is not intended for clinical diagnosis or treatment decisions.
