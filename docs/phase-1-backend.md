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

## Phase 1.1 — Categories, curriculum and admin foundation

Added in this increment:
- `GET /v1/categories?locale=en|hi` returns translated categories.
- `GET /v1/courses/{course_id}/curriculum?locale=en|hi` returns ordered modules and lessons.
- Curriculum responses expose YouTube video IDs only for preview lessons. Non-preview IDs remain hidden until server-side subscription entitlement checks are implemented.
- `GET /v1/admin/me` verifies the signed-in user's database profile is active and has the `admin` role.
- Admin-only endpoints create categories, draft courses, modules and lessons, and publish courses.
- Admin mutations write audit-log entries.
- Profile sync now requires a Firebase-verified email address.
- Unit tests cover admin authorization and request validation.

### Promote the first administrator

There is intentionally no public API to grant admin privileges. After the first account signs in and calls `/v1/auth/sync`, promote that account through a trusted database operator session:

```sql
UPDATE users
SET role = 'admin'
WHERE email = 'YOUR_VERIFIED_ADMIN_EMAIL';
```

Do not expose this SQL operation through the mobile app or a public endpoint. Keep the database credentials restricted to trusted operators.

### API flow for publishing a course

1. `POST /v1/admin/categories` (optional)
2. `POST /v1/admin/courses` — creates a draft
3. `POST /v1/admin/courses/{course_id}/modules`
4. `POST /v1/admin/modules/{module_id}/lessons`
5. `POST /v1/admin/courses/{course_id}/publish`

All admin endpoints require `Authorization: Bearer <Firebase ID token>` and an active user whose database role is `admin`.

### Remaining before production

- Configure Firebase project credentials and verify with real ID tokens.
- Run Alembic migrations against PostgreSQL and execute integration tests.
- Implement subscription entitlement checks before returning any paid lesson playback URL or video ID.
- Add rate limiting, structured logging, deployment secrets and production CORS origins.
