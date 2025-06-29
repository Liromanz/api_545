FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VENV_PATH=/opt/venv

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv $VENV_PATH
ENV PATH="$VENV_PATH/bin:$PATH"

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m userfiveforfive
USER userfiveforfive

# Команда для запуска приложения с автоматическими миграциями
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 api_fivefortyfive.wsgi:application"]