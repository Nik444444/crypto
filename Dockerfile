# Dockerfile для Backend
FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование requirements.txt
COPY backend/requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование backend кода
COPY backend/ .

# Создание директории для SQLite базы данных
RUN mkdir -p /app/data

# Установка правильных прав
RUN chmod 755 /app && chmod 755 /app/data

# Открытие порта
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]