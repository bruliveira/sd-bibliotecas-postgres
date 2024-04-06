from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from .database import connect_to_database, close_database_connection

router = APIRouter()

class Livro(BaseModel):
    titulo: str
    autor: str
    editora: str

async def get_all_books():
    connection = await connect_to_database()
    try:
        return await connection.fetch("SELECT * FROM livros")
    finally:
        await close_database_connection(connection)

async def get_book_by_id(livro_id: int):
    connection = await connect_to_database()
    try:
        return await connection.fetchrow("SELECT * FROM livros WHERE livro_id = $1", livro_id)
    finally:
        await close_database_connection(connection)

async def add_book(livro: Livro):
    connection = await connect_to_database()
    try:
        await connection.execute("INSERT INTO livros (titulo, autor, editora) VALUES ($1, $2, $3)", livro.titulo, livro.autor, livro.editora)
    finally:
        await close_database_connection(connection)

async def delete_book(livro_id: int):
    connection = await connect_to_database()
    try:
        await connection.execute("DELETE FROM livros WHERE livro_id = $1", livro_id)
    finally:
        await close_database_connection(connection)

async def update_book(livro_id: int, livro: Livro):
    connection = await connect_to_database()
    try:
        await connection.execute("UPDATE livros SET titulo = $1, autor = $2, editora = $3 WHERE livro_id = $4", livro.titulo, livro.autor, livro.editora, livro_id)
    finally:
        await close_database_connection(connection)

@router.get("/livros")
async def listar_livros():
    livros = await get_all_books()
    return {"livros": livros}

@router.get("/livros/{livro_id}")
async def buscar_livro_por_id(livro_id: int):
    livro = await get_book_by_id(livro_id)
    if livro:
        return livro
    else:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

@router.post("/livros")
async def adicionar_livro(livro: Livro):
    await add_book(livro)
    return {"mensagem": "Livro adicionado com sucesso"}

@router.delete("/livros/{livro_id}")
async def deletar_livro(livro_id: int):
    livro = await get_book_by_id(livro_id)
    if livro:
        await delete_book(livro_id)
        return {"mensagem": "Livro deletado com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

@router.put("/livros/{livro_id}")
async def atualizar_livro(livro_id: int, livro: Livro):
    livro_existente = await get_book_by_id(livro_id)
    if livro_existente:
        await update_book(livro_id, livro)
        return {"mensagem": "Livro atualizado com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
