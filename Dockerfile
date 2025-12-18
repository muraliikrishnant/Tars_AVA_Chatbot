FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy backend code
COPY backend/ ./backend/

# Expose port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "backend.main:app"]
