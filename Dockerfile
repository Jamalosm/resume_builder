FROM python:3.12-slim

# Install LaTeX
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-fonts-recommended \
    && rm -rf /var/lib/apt/lists/*


# Set working directory
WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn easy_resume_builder.wsgi:application \
    --env DJANGO_SETTINGS_MODULE=easy_resume_builder.settings \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --threads 2 \
    --timeout 120

