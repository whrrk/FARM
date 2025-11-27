FROM python:3.12-slim

WORKDIR /app

# build library
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# app source code
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
