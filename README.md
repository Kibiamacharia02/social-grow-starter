# Social Grow Starter

A compliant Instagram scheduler + basic analytics starter.

## What it is
Schedules image + caption posts to Instagram Business accounts using the Instagram Graph API and records publish status.

## Quick run (local dev)
1. Copy repo files into `social-grow-starter/`.
2. Create `.env` file (see `.env.example`). Set `FERNET_KEY`.
3. Build and run:
   docker compose up --build

Services:
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- Postgres: 5432 (db: socialgrow)
- Redis: 6379

## Instagram setup (developer steps)
1. Create a Meta/Facebook App and configure Instagram permissions.
2. Link an Instagram Business/Creator account to a Facebook Page.
3. Follow Meta docs to obtain a long-lived access token for the Instagram Business user ID.
4. Create an Account row in `accounts` table with encrypted token, or implement OAuth flow.

## Notes
- This starter uses encrypted tokens — in production use KMS (AWS KMS) or Vault.
- Implement OAuth account linking flow for production (not included).
- Follow rate limits and app review steps in Meta docs.
