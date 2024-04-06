# Use a imagem oficial do Python como base
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos de código-fonte e os arquivos de requisitos para o contêiner
COPY . .

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta em que a aplicação FastAPI será executada
EXPOSE 5000

# Comando para iniciar o servidor Uvicorn
CMD ["uvicorn", "biblioteca:app", "--host", "0.0.0.0", "--port", "5000"]
