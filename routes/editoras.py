from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from .database import connect_to_database, close_database_connection

router = APIRouter()

class Editora(BaseModel):
    nome: str
    endereco: str

async def get_all_editoras():
    connection = await connect_to_database()
    try:
        return await connection.fetch("SELECT * FROM editoras")
    finally:
        await close_database_connection(connection)

async def get_editora_by_id(editora_id: int):
    connection = await connect_to_database()
    try:
        return await connection.fetchrow("SELECT * FROM editoras WHERE editora_id = $1", editora_id)
    finally:
        await close_database_connection(connection)

async def add_editora(editora: Editora):
    connection = await connect_to_database()
    try:
        await connection.execute("INSERT INTO editoras (nome, endereco) VALUES ($1, $2)", editora.nome, editora.endereco)
    finally:
        await close_database_connection(connection)

async def delete_editora(editora_id: int):
    connection = await connect_to_database()
    try:
        await connection.execute("DELETE FROM editoras WHERE editora_id = $1", editora_id)
    finally:
        await close_database_connection(connection)

async def update_editora(editora_id: int, editora: Editora):
    connection = await connect_to_database()
    try:
        await connection.execute("UPDATE editoras SET nome = $1, endereco = $2 WHERE editora_id = $3", editora.nome, editora.endereco, editora_id)
    finally:
        await close_database_connection(connection)

@router.get("/editoras")
async def listar_editoras():
    editoras = await get_all_editoras()
    return {"editoras": editoras}

@router.get("/editoras/{editora_id}")
async def buscar_editora_por_id(editora_id: int):
    editora = await get_editora_by_id(editora_id)
    if editora:
        return editora
    else:
        raise HTTPException(status_code=404, detail="Editora não encontrada")

@router.post("/editoras")
async def adicionar_editora(editora: Editora):
    await add_editora(editora)
    return {"mensagem": "Editora adicionada com sucesso"}

@router.delete("/editoras/{editora_id}")
async def deletar_editora(editora_id: int):
    editora = await get_editora_by_id(editora_id)
    if editora:
        await delete_editora(editora_id)
        return {"mensagem": "Editora deletada com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Editora não encontrada")

@router.put("/editoras/{editora_id}")
async def atualizar_editora(editora_id: int, editora: Editora):
    editora_existente = await get_editora_by_id(editora_id)
    if editora_existente:
        await update_editora(editora_id, editora)
        return {"mensagem": "Editora atualizada com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Editora não encontrada")


