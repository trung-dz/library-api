from pydantic import BaseModel, Field


# ==========================================
# THONG TIN CO BAN CUA SACH
# ==========================================

class BookBase(BaseModel):

    isbn: str = Field(
        pattern=r"^\d{13}$",
        examples=["9786040000011"]
    )

    title: str = Field(
        min_length=1,
        max_length=200
    )

    author: str = Field(
        min_length=1,
        max_length=100
    )

    year: int = Field(
        ge=1900,
        le=2100
    )

    quantity: int = Field(
        default=1,
        ge=0
    )


# ==========================================
# MODEL THEM SACH
# ==========================================

class BookCreate(BookBase):
    pass


# ==========================================
# MODEL CAP NHAT MOT PHAN
# ==========================================

class BookUpdate(BaseModel):

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )

    author: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    year: int | None = Field(
        default=None,
        ge=1900,
        le=2100
    )

    quantity: int | None = Field(
        default=None,
        ge=0
    )


# ==========================================
# MODEL DU LIEU TRA VE
# ==========================================

class BookOut(BookBase):

    id: int