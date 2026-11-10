from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, catalog, health
from app.core.config import settings

app = FastAPI(title=settings.app_name, version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)
app.include_router(health.router, prefix=settings.api_v1_prefix)
app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(catalog.router, prefix=settings.api_v1_prefix)


@app.get("/")
def root():
    return {"name": settings.app_name, "version": "0.2.0", "docs": "/docs"}
