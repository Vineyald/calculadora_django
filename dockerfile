# Imagem base
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código
COPY . .

# Comando padrão
CMD ["python", "app/manage.py", "runserver", "0.0.0.0:8000"]
