# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements (if you have a requirements.txt)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port 8000
EXPOSE 8000

# Start FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]