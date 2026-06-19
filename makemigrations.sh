#!/bin/bash
if [ -z "$1" ]
  then
    echo "Ошибка: Напиши сообщение для миграции! Пример: ./makemigrations.sh add_created_at"
    exit 1
fi

docker compose exec web alembic revision --autogenerate -m "$1"