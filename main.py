from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="API Data Mahasiswa",
    description="REST API untuk mengelola data mahasiswa",
    version="1.0.0"
)


# =========================
# MODEL DATA MAHASISWA
# =========================

class Mahasiswa(BaseModel):
    nama: str
    alamat: str
    ipk: float = Field(..., ge=0, le=4)
    semester: int = Field(..., ge=1)
    hobi: str


# =========================
# SIMULASI DATABASE
# =========================

mahasiswa_db = {}


# =========================
# CREATE - POST
# =========================

@app.post("/mahasiswa/{mahasiswa_id}")
async def create_mahasiswa(mahasiswa_id: int, mahasiswa: Mahasiswa):

    if mahasiswa_id in mahasiswa_db:
        raise HTTPException(
            status_code=400,
            detail="Data mahasiswa sudah ada"
        )

    mahasiswa_db[mahasiswa_id] = mahasiswa.model_dump()

    return {
        "message": "Data mahasiswa berhasil ditambahkan",
        "mahasiswa_id": mahasiswa_id,
        "data": mahasiswa_db[mahasiswa_id]
    }


# =========================
# READ - GET
# =========================

@app.get("/mahasiswa")
async def get_all_mahasiswa():

    return {
        "message": "Data seluruh mahasiswa",
        "data": mahasiswa_db
    }


@app.get("/mahasiswa/{mahasiswa_id}")
async def get_mahasiswa(mahasiswa_id: int):

    if mahasiswa_id not in mahasiswa_db:
        raise HTTPException(
            status_code=404,
            detail="Data mahasiswa tidak ditemukan"
        )

    return {
        "mahasiswa_id": mahasiswa_id,
        "data": mahasiswa_db[mahasiswa_id]
    }


# =========================
# UPDATE - PUT
# =========================

@app.put("/mahasiswa/{mahasiswa_id}")
async def update_mahasiswa(
    mahasiswa_id: int,
    mahasiswa: Mahasiswa
):

    if mahasiswa_id not in mahasiswa_db:
        raise HTTPException(
            status_code=404,
            detail="Data mahasiswa tidak ditemukan"
        )

    mahasiswa_db[mahasiswa_id] = mahasiswa.model_dump()

    return {
        "message": "Data mahasiswa berhasil diperbarui",
        "mahasiswa_id": mahasiswa_id,
        "data": mahasiswa_db[mahasiswa_id]
    }


# =========================
# DELETE - DELETE
# =========================

@app.delete("/mahasiswa/{mahasiswa_id}")
async def delete_mahasiswa(mahasiswa_id: int):

    if mahasiswa_id not in mahasiswa_db:
        raise HTTPException(
            status_code=404,
            detail="Data mahasiswa tidak ditemukan"
        )

    deleted_data = mahasiswa_db.pop(mahasiswa_id)

    return {
        "message": "Data mahasiswa berhasil dihapus",
        "mahasiswa_id": mahasiswa_id,
        "deleted_data": deleted_data
    }