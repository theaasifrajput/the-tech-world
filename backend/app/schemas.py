from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    slug: str = Field(min_length=2, max_length=140, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    name_en: str = Field(min_length=1, max_length=120)
    name_hi: str | None = Field(default=None, max_length=120)
    description_en: str | None = None
    description_hi: str | None = None


class CourseCreate(BaseModel):
    category_id: str | None = None
    slug: str = Field(min_length=2, max_length=180, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    thumbnail_url: str | None = None
    level: str | None = Field(default=None, max_length=30)
    is_free: bool = False
    title_en: str = Field(min_length=1, max_length=255)
    description_en: str | None = None
    title_hi: str | None = Field(default=None, max_length=255)
    description_hi: str | None = None


class ModuleCreate(BaseModel):
    position: int = Field(ge=1)
    title_en: str = Field(min_length=1, max_length=255)
    title_hi: str | None = Field(default=None, max_length=255)


class LessonCreate(BaseModel):
    position: int = Field(ge=1)
    title_en: str = Field(min_length=1, max_length=255)
    title_hi: str | None = Field(default=None, max_length=255)
    description_en: str | None = None
    description_hi: str | None = None
    youtube_video_id: str | None = Field(default=None, max_length=32)
    duration_seconds: int | None = Field(default=None, ge=1)
    is_preview: bool = False
