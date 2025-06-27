FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD ["gunicorn", "swap.wsgi:application", "--bind", "0.0.0.0:8000"]
