from pydantic import BaseModel

from fastapi import APIRouter, HTTPException
from .database import connect_to_database, close_database_connection

router = APIRouter()

class Emprestimo(BaseModel):
    livro_id: int
    membro_id: int
    data_emprestimo: str
    data_devolucao: str

async def get_all_emprestimos():
    connection = await connect_to_database()
    try:
        return await connection.fetch("SELECT * FROM emprestimos")
    finally:
        await close_database_connection(connection)

async def get_emprestimo_by_id(emprestimo_id: int):
    connection = await connect_to_database()
    try:
        return await connection.fetchrow("SELECT * FROM emprestimos WHERE emprestimo_id = $1", emprestimo_id)
    finally:
        await close_database_connection(connection)

async def add_emprestimo(emprestimo: Emprestimo):
    connection = await connect_to_database()
    try:
        await connection.execute("INSERT INTO emprestimos (livro_id, membro_id, data_emprestimo, data_devolucao) VALUES ($1, $2, $3, $4)",
                                 emprestimo.livro_id, emprestimo.membro_id, emprestimo.data_emprestimo, emprestimo.data_devolucao)
    finally:
        await close_database_connection(connection)

async def delete_emprestimo(emprestimo_id: int):
    connection = await connect_to_database()
    try:
        await connection.execute("DELETE FROM emprestimos WHERE emprestimo_id = $1", emprestimo_id)
    finally:
        await close_database_connection(connection)

async def update_emprestimo(emprestimo_id: int, emprestimo: Emprestimo):
    connection = await connect_to_database()
    try:
        await connection.execute("UPDATE emprestimos SET livro_id = $1, membro_id = $2, data_emprestimo = $3, data_devolucao = $4 WHERE emprestimo_id = $5",
                                 emprestimo.livro_id, emprestimo.membro_id, emprestimo.data_emprestimo, emprestimo.data_devolucao, emprestimo_id)
    finally:
        await close_database_connection(connection)

@router.get("/emprestimos")
async def listar_emprestimos():
    emprestimos = await get_all_emprestimos()
    return {"emprestimos": emprestimos}

@router.get("/emprestimos/{emprestimo_id}")
async def buscar_emprestimo_por_id(emprestimo_id: int):
    emprestimo = await get_emprestimo_by_id(emprestimo_id)
    if emprestimo:
        return emprestimo
    else:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")

@router.post("/emprestimos")
async def adicionar_emprestimo(emprestimo: Emprestimo):
    await add_emprestimo(emprestimo)
    return {"mensagem": "Empréstimo adicionado com sucesso"}

@router.delete("/emprestimos/{emprestimo_id}")
async def deletar_emprestimo(emprestimo_id: int):
    emprestimo = await get_emprestimo_by_id(emprestimo_id)
    if emprestimo:
        await delete_emprestimo(emprestimo_id)
        return {"mensagem": "Empréstimo deletado com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")

@router.put("/emprestimos/{emprestimo_id}")
async def atualizar_emprestimo(emprestimo_id: int, emprestimo: Emprestimo):
    emprestimo_existente = await get_emprestimo_by_id(emprestimo_id)
    if emprestimo_existente:
        await update_emprestimo(emprestimo_id, emprestimo)
        return {"mensagem": "Empréstimo atualizado com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
