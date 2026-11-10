# Architecture

```text
Flutter Android/iOS ─┐
                     ├── FastAPI ── PostgreSQL
Next.js Admin ───────┘      │
                            ├── Firebase Authentication
                            ├── Google Play Developer API
                            ├── App Store Server API
                            ├── Razorpay (eligible web checkout only)
                            ├── YouTube IFrame Player
                            └── Firebase Cloud Messaging
```

## Trust boundaries
- Firebase ID tokens authenticate callers; backend maps Firebase UID to an application user.
- Backend owns roles, subscription state, entitlements, and progress.
- Never accept subscription or role claims from an untrusted mobile request.
- Verify purchases with the relevant provider before granting entitlements.
- Webhook event IDs and provider transaction IDs must be unique and idempotent.
- YouTube unlisted videos are not private content protection.
