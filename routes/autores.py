from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from .database import connect_to_database, close_database_connection

router = APIRouter()

class Autor(BaseModel):
    nome: str
    nacionalidade: str

async def get_all_autores():
    connection = await connect_to_database()
    try:
        return await connection.fetch("SELECT * FROM autores")
    finally:
        await close_database_connection(connection)

async def get_autor_by_id(autor_id: int):
    connection = await connect_to_database()
    try:
        return await connection.fetchrow("SELECT * FROM autores WHERE autor_id = $1", autor_id)
    finally:
        await close_database_connection(connection)

async def add_autor(autor: Autor):
    connection = await connect_to_database()
    try:
        await connection.execute("INSERT INTO autores (nome, nacionalidade) VALUES ($1, $2)", autor.nome, autor.nacionalidade)
    finally:
        await close_database_connection(connection)

async def delete_autor(autor_id: int):
    connection = await connect_to_database()
    try:
        await connection.execute("DELETE FROM autores WHERE autor_id = $1", autor_id)
    finally:
        await close_database_connection(connection)

async def update_autor(autor_id: int, autor: Autor):
    connection = await connect_to_database()
    try:
        await connection.execute("UPDATE autores SET nome = $1, nacionalidade = $2 WHERE autor_id = $3", autor.nome, autor.nacionalidade, autor_id)
    finally:
        await close_database_connection(connection)

@router.get("/autores")
async def listar_autores():
    autores = await get_all_autores()
    return {"autores": autores}

@router.get("/autores/{autor_id}")
async def buscar_autor_por_id(autor_id: int):
    autor = await get_autor_by_id(autor_id)
    if autor:
        return autor
    else:
        raise HTTPException(status_code=404, detail="Autor não encontrado")

@router.post("/autores")
async def adicionar_autor(autor: Autor):
    await add_autor(autor)
    return {"mensagem": "Autor adicionado com sucesso"}

@router.delete("/autores/{autor_id}")
async def deletar_autor(autor_id: int):
    autor = await get_autor_by_id(autor_id)
    if autor:
        await delete_autor(autor_id)
        return {"mensagem": "Autor deletado com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Autor não encontrado")

@router.put("/autores/{autor_id}")
async def atualizar_autor(autor_id: int, autor: Autor):
    autor_existente = await get_autor_by_id(autor_id)
    if autor_existente:
        await update_autor(autor_id, autor)
        return {"mensagem": "Autor atualizado com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Autor não encontrado")

