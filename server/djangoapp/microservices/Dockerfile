FROM python:3.9.18-slim-bookworm

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Let Flask know which app to run
ENV FLASK_APP=sentiment_analyzer.py

# Optional: prevent caching NLTK downloads
ENV PYTHONUNBUFFERED=1

# Run Flask
CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]
