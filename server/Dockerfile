# Use an official Python slim image
FROM python:3.12.0-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Run Gunicorn
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "django_static_pages_capstone.wsgi:application"]
