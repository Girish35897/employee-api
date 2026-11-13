FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Set a default port environment variable and metadata
ENV PORT=5000
EXPOSE 5000

# Recommended security practice: run as a non-root user
RUN useradd -u 10001 appuser && chown -R appuser:appuser /app
USER appuser

CMD ["python", "app.py"]