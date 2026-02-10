FROM python:3.12-slim

# Install LaTeX
RUN apt-get update && apt-get install -y \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-xetex \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Railway uses PORT env
CMD ["gunicorn", "resume_builder.wsgi:application", "--bind", "0.0.0.0:$PORT"]
