from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Category, CategoryTranslation

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("")
def list_categories(
    locale: str = Query(default="en", pattern="^(en|hi)$"),
    db: Session = Depends(get_db),
):
    rows = db.execute(
        select(Category, CategoryTranslation)
        .join(CategoryTranslation, CategoryTranslation.category_id == Category.id)
        .where(CategoryTranslation.locale == locale)
        .order_by(Category.slug.asc())
    ).all()
    return {
        "items": [
            {
                "id": str(category.id),
                "slug": category.slug,
                "name": translation.name,
                "description": translation.description,
            }
            for category, translation in rows
        ],
        "locale": locale,
    }
