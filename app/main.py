from fastapi import FastAPI

from app.routers import books


# ==========================================
# KHOI TAO UNG DUNG FASTAPI
# ==========================================

app = FastAPI(

    title="Library API – Khoa CNTT",

    version="1.0.0",

    description="API quản lý sách của Thư viện số Khoa CNTT"

)


# ==========================================
# DANG KY ROUTER
# ==========================================

app.include_router(books.router)


# ==========================================
# KIEM TRA TRANG THAI SERVER
# ==========================================

@app.get(
    "/health",
    tags=["System"]
)
def health():

    return {
        "status": "ok"
    }