# ==========================================
# Stage 1: Build Frontend (React + Vite + Tailwind)
# ==========================================
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# ==========================================
# Stage 2: Production Python Backend
# ==========================================
FROM python:3.11-slim

WORKDIR /app

# Prevent Python from writing .pyc and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY backend/ ./backend/
COPY run_newsletter_agent.py .env.example ./

# Copy built frontend from Stage 1 into /app/frontend/dist
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Ensure outputs directory exists
RUN mkdir -p /app/outputs

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
