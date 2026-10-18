# Known limitations and roadmap

This list distinguishes current limitations from implemented application behavior. It is not a committed delivery schedule.

## Current limitations

- Google and GitHub OAuth are not implemented; account sign-in uses the existing backend password/JWT flow.
- The frontend has no verified QR scanning interface. QR token generation and verification exist at the backend API level.
- SOS events are stored and exposed for admin triage; no emergency service is contacted.
- Payment features track records and status; no money is collected or transferred.
- The map draws a straight line using provided coordinates. It does not geocode addresses, calculate road distance, or estimate travel time.
- Public OpenStreetMap tiles have usage requirements, limited capacity, and no service-level guarantee. A production mapping option has not been selected.
- Avatar files are stored on the backend filesystem; shared durable storage is not configured for multi-instance hosting.
- Browser-driven end-to-end tests and visual verification across phone, tablet, and desktop sizes are not configured.
- There is no AWS deployment setup, production observability, or recovery documentation based on a tested deployment.
- `LICENSE` is empty, so no explicit reuse/redistribution license has been selected. Screenshots are not currently checked in.

## Suggested next work

1. Add end-to-end tests for registration, ride creation/search, booking, cancellation, waitlist promotion, and role-denied requests.
2. Add browser viewport checks for the most important journeys and accessibility review.
3. Decide whether to implement OAuth and a frontend QR scanning flow, including provider setup and failure handling.
4. Review production configuration, uploaded-image storage, backups, monitoring, and migration operations before considering hosting.
5. Select and add a project license and a private vulnerability-reporting contact before presenting the repository as an open-source release.

Keep cost review separate for any external mapping, identity, hosting, or operational service. Do not assume that public endpoints offer unlimited use.
