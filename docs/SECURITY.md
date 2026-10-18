# Security considerations

This document describes the current local-development implementation. It is not a production security certification.

## Authentication and authorization

- Passwords are hashed by the backend. Login returns a signed JWT access token; protected API calls validate the access-token type and resolve the user.
- The frontend stores the access token in `localStorage`. A cross-site scripting flaw could expose it, so keep dependencies current and avoid unsafe HTML rendering.
- Registration permits driver and passenger roles, not admin. Backend dependencies enforce role requirements, with ownership checks on user-owned resources.
- Google/GitHub OAuth is optional and disabled until server credentials are configured. The callback uses a short-lived state cookie, requests identity-only scopes, requires verified provider email, and stores unique provider subjects. It links only to an existing CommuteShare account with that verified email; OAuth does not create accounts.
- Password-reset links use random tokens whose SHA-256 digest and expiration are stored in the user record. Requests use a generic response for known and unknown accounts, and are throttled per account. SMTP credentials must stay in the ignored local `.env`; mail is delivered only when SMTP is configured. Reset does not send SMS.
- Resetting a password does not revoke already-issued stateless JWTs; those remain valid until their configured expiration.

## Secrets and local configuration

- Never commit a real `.env`, JWT key, database password, private key, user upload, or database dump.
- `backend/.env.example` is a local Compose example. It includes `DEBUG=True`, a placeholder `SECRET_KEY`, and development database credentials. Do not deploy those values.
- For any deployment, supply a strong unique secret and database credential through a deployment-specific secret mechanism. This repository does not provision one.

## Uploads, maps, and safety

- Avatar images are stored on the backend filesystem and served by the `/uploads` mount. A production multi-instance storage and retention policy is not configured.
- The map sends requests to the configured tile service; the default is OpenStreetMap's public tile endpoint. Follow its [tile policy](https://operations.osmfoundation.org/policies/tiles/), retain visible attribution, and do not bulk-download tiles.
- SOS creates an in-app record and notifies configured admin users. It does not contact emergency services; the UI should not be treated as an emergency dispatch channel.
- Payment rows are status tracking only. There is no payment processor or card-data handling flow.

## Deployment boundary

The Compose file binds local ports to loopback, but its development settings, credentials, and reload server are not suitable for public deployment. The repository has no AWS infrastructure or production TLS, backup, monitoring, or network configuration. See [Deployment notes](DEPLOYMENT.md).

No private security contact is configured in the repository. If reporting a vulnerability, contact the maintainer privately rather than publishing exploit details in a public issue.
