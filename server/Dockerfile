# Use official Python image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY .server/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /app/

# Make entrypoint executable
RUN chmod +x .server/entrypoint.sh

# Set entrypoint
ENTRYPOINT [".server/entrypoint.sh"]

# Start gunicorn server
CMD ["gunicorn", "django_static_pages_capstone.wsgi:application", "--bind", "0.0.0.0:8000"]


