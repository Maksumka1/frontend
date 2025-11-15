# Use official slim Python image
FROM python:3.11-slim
LABEL maintainer="sakovskoho12@gmail.com"
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN chown -R appuser:appgroup /app
USER appuser
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--worker-class", "gthread", "--threads", "2", "app:app", "--timeout", "30"]
