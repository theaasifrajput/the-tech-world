# Phase 1 — Backend foundation

Implemented in this increment:
- SQLAlchemy ORM entities matching the initial Alembic schema.
- Alembic metadata discovery.
- Fail-closed Firebase ID-token verification using Application Default Credentials.
- Auth profile synchronization and current-user endpoints.
- Published course list/detail endpoints with `en` / `hi` translation selection.
- Health and database readiness endpoints.

Before local auth testing:
1. Create a Firebase project and enable desired sign-in providers.
2. Set `FIREBASE_PROJECT_ID`.
3. Configure Application Default Credentials for the local environment.
4. Ensure Firebase sign-in issues ID tokens for that project.
5. Apply migrations and test `/auth/sync`.

Security note: profile sync deliberately never accepts a role from the client. New users always receive the database default `student` role. Admin role assignment must be performed through a controlled operator process.
