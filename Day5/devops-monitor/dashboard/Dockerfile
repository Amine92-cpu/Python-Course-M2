# dashboard/Dockerfile — single-stage build
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir streamlit httpx pandas

COPY dashboard/ ./dashboard/

ENV PYTHONUNBUFFERED=1
ENV API_BASE_URL="http://api:8000"
ENV API_KEY=""

EXPOSE 8501

CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
