import asyncpg
from fastapi import  APIRouter

router = APIRouter()

# Configuração da conexão com o banco de dados PostgreSQL
DATABASE_URL = "postgresql://postgres:changeme@host.docker.internal/biblioteca"


async def connect_to_database():
    return await asyncpg.connect(DATABASE_URL)

async def close_database_connection(connection):
    await connection.close()


async def check_db_connection():
    try:
        # Tenta estabelecer uma conexão com o banco de dados
        async with asyncpg.create_pool(DATABASE_URL) as pool:
            async with pool.acquire() as connection:
                # Verifica se a conexão foi bem-sucedida
                await connection.execute("SELECT 1")
                return True
    except asyncpg.exceptions.PostgresError as e:
        # Em caso de erro, retorna False e imprime o erro
        print(f"Erro ao conectar ao banco de dados: {e}")
        return False

# Rota para verificar a conexão com o banco de dados
@router.get("/check_db_connection")
async def test_db_connection():
    if await check_db_connection():
        return {"message": "Conexão com o banco de dados estabelecida com sucesso!"}
    else:
        return {"message": "Falha ao conectar ao banco de dados."}