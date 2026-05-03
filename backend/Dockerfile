FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x start.sh

# Local dev: override CMD in docker-compose to skip migrations
# Railway / production: start.sh runs alembic upgrade head first
CMD ["./start.sh"]
