# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Coleta arquivos estáticos (se necessário)
RUN python manage.py collectstatic --noinput

# Executa migrações
RUN python manage.py migrate

# Comando para iniciar o servidor
CMD ["gunicorn", "seuprojeto.wsgi:application", "--bind", "0.0.0.0:8000"]
