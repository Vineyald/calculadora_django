FROM python:3.11-slim

# Define o diretório base da aplicação
WORKDIR /app

# Copia todos os arquivos para dentro do container
COPY . .

# Instala dependências
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn

# Executa migrações
RUN python app/manage.py migrate

# Comando para rodar o Gunicorn
CMD ["gunicorn", "core.wsgi:application", "--chdir", "app", "--bind", "0.0.0.0:8000"]
