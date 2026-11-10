# The Tech World

Subscription-based learning platform for India. MVP: English + Hindi, monthly subscription, Flutter Android/iOS, FastAPI backend, Next.js admin.

## Layout
- `mobile/` Flutter Android/iOS app
- `backend/` FastAPI, SQLAlchemy, Alembic
- `admin/` Next.js admin portal (scaffold planned)
- `infra/` local development infrastructure
- `docs/` product and architecture notes

## Backend quick start
1. Copy `backend/.env.example` to `backend/.env`.
2. Start PostgreSQL: `docker compose -f infra/docker-compose.yml up -d db`
3. `cd backend && python -m venv .venv`
4. Activate the venv and run `pip install -r requirements.txt`
5. Run `alembic upgrade head`
6. Run `uvicorn app.main:app --reload`
7. Open `http://localhost:8000/docs`.

## Flutter quick start
Install Flutter stable, then:
```bash
cd mobile
flutter create --platforms=android,ios .
flutter pub get
flutter run
```
Run `flutter create` before the first platform build; preserve the provided `lib/` and `pubspec.yaml`.

## Decisions
- Market: India; currency: INR.
- Monthly subscription only.
- Locales: `en` and `hi`.
- Mobile digital subscriptions must follow Google Play Billing and Apple In-App Purchase rules as applicable.
- Razorpay is reserved for eligible web checkout flows.
- YouTube embed does not provide DRM; unlisted video links can be shared.
- Never commit production secrets.

## Scaffold status
This is a foundation, not a production payment/authentication implementation. Firebase token verification, provider purchase verification, webhook processing, admin UI, and production deployment remain to be implemented and tested.
