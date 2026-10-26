from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query, status

from app.data import BOOKS
from app.models import BookCreate, BookOut, BookUpdate


# ==========================================
# KHOI TAO ROUTER
# ==========================================

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

BookId = Annotated[
    int,
    Path(gt=0, description="Mã sách")
]


# ==========================================
# HAM TIM KIEM SACH THEO ID
# ==========================================

def find_book(book_id: int) -> dict:

    for book in BOOKS:
        if book["id"] == book_id:
            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Không tìm thấy sách id={book_id}"
    )


# ==========================================
# HAM KIEM TRA ISBN TRUNG
# ==========================================

def check_isbn(
    isbn: str,
    exclude_id: int | None = None
) -> None:

    if any(
        book["isbn"] == isbn and book["id"] != exclude_id
        for book in BOOKS
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"ISBN {isbn} đã tồn tại"
        )


# ==========================================
# GET - HIEN THI DANH SACH SACH
# ==========================================

@router.get(
    "",
    response_model=list[BookOut],
    summary="Danh sách sách"
)
def list_books(
    q: Annotated[
        str | None,
        Query(max_length=50)
    ] = None,

    author: str | None = None,

    skip: Annotated[
        int,
        Query(ge=0)
    ] = 0,

    limit: Annotated[
        int,
        Query(ge=1, le=100)
    ] = 10
):

    data = BOOKS

    # Tim kiem theo ten sach
    if q:
        data = [
            book for book in data
            if q.lower() in book["title"].lower()
        ]

    # Tim kiem theo tac gia
    if author:
        data = [
            book for book in data
            if author.lower() in book["author"].lower()
        ]

    # Phan trang
    return data[skip:skip + limit]


# ==========================================
# GET - XEM CHI TIET SACH
# ==========================================

@router.get(
    "/{book_id}",
    response_model=BookOut,
    summary="Chi tiết sách"
)
def get_book(book_id: BookId):

    return find_book(book_id)


# ==========================================
# POST - THEM SACH MOI
# ==========================================

@router.post(
    "",
    response_model=BookOut,
    status_code=status.HTTP_201_CREATED,
    summary="Thêm sách"
)
def create_book(book: BookCreate):

    # Kiem tra ISBN
    check_isbn(book.isbn)

    # Tao ID tu dong
    new_id = max(
        (b["id"] for b in BOOKS),
        default=0
    ) + 1

    # Tao sach moi
    new = {
        "id": new_id,
        **book.model_dump()
    }

    # Them vao danh sach
    BOOKS.append(new)

    return new


# ==========================================
# PUT - CAP NHAT TOAN BO THONG TIN
# ==========================================

@router.put(
    "/{book_id}",
    response_model=BookOut,
    summary="Cập nhật toàn bộ"
)
def replace_book(
    book_id: BookId,
    book: BookCreate
):

    current = find_book(book_id)

    check_isbn(
        book.isbn,
        exclude_id=book_id
    )

    current.update(
        book.model_dump()
    )

    return current


# ==========================================
# PATCH - CAP NHAT MOT PHAN THONG TIN
# ==========================================

@router.patch(
    "/{book_id}",
    response_model=BookOut,
    summary="Cập nhật một phần"
)
def update_book(
    book_id: BookId,
    book: BookUpdate
):

    current = find_book(book_id)

    current.update(
        book.model_dump(exclude_unset=True)
    )

    return current


# ==========================================
# DELETE - XOA SACH
# ==========================================

@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Xóa sách"
)
def delete_book(book_id: BookId):

    BOOKS.remove(find_book(book_id))