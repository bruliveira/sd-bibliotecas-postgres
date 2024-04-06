from fastapi import APIRouter, HTTPException
from .database import connect_to_database, close_database_connection
from pydantic import BaseModel

router = APIRouter()

class Membro(BaseModel):
    nome: str
    email: str

async def get_all_membros():
    connection = await connect_to_database()
    try:
        return await connection.fetch("SELECT * FROM membros")
    finally:
        await close_database_connection(connection)

async def get_membro_by_id(membro_id: int):
    connection = await connect_to_database()
    try:
        return await connection.fetchrow("SELECT * FROM membros WHERE membro_id = $1", membro_id)
    finally:
        await close_database_connection(connection)

async def add_membro(membro: Membro):
    connection = await connect_to_database()
    try:
        await connection.execute("INSERT INTO membros (nome, email) VALUES ($1, $2)", membro.nome, membro.email)
    finally:
        await close_database_connection(connection)

async def delete_membro(membro_id: int):
    connection = await connect_to_database()
    try:
        await connection.execute("DELETE FROM membros WHERE membro_id = $1", membro_id)
    finally:
        await close_database_connection(connection)

async def update_membro(membro_id: int, membro: Membro):
    connection = await connect_to_database()
    try:
        await connection.execute("UPDATE membros SET nome = $1, email = $2 WHERE membro_id = $3", membro.nome, membro.email, membro_id)
    finally:
        await close_database_connection(connection)

@router.get("/membros")
async def listar_membros():
    membros = await get_all_membros()
    return {"membros": membros}

@router.get("/membros/{membro_id}")
async def buscar_membro_por_id(membro_id: int):
    membro = await get_membro_by_id(membro_id)
    if membro:
        return membro
    else:
        raise HTTPException(status_code=404, detail="Membro não encontrado")

@router.post("/membros")
async def adicionar_membro(membro: Membro):
    await add_membro(membro)
    return {"mensagem": "Membro adicionado com sucesso"}

@router.delete("/membros/{membro_id}")
async def deletar_membro(membro_id: int):
    membro = await get_membro_by_id(membro_id)
    if membro:
        await delete_membro(membro_id)
        return {"mensagem": "Membro deletado com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Membro não encontrado")

@router.put("/membros/{membro_id}")
async def atualizar_membro(membro_id: int, membro: Membro):
    membro_existente = await get_membro_by_id(membro_id)
    if membro_existente:
        await update_membro(membro_id, membro)
        return {"mensagem": "Membro atualizado com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Membro não encontrado")
