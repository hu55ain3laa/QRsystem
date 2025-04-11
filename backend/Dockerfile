# Use Python 3.12 as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    fonts-dejavu \
    fonts-freefont-ttf \
    fontconfig \
    # Dependencies for Playwright and PDF generation
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libnss3 \
    libcups2 \
    libxss1 \
    libxrandr2 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium

# Create data directory for SQLite database
RUN mkdir -p /app/data

# Expose the port the app runs on
EXPOSE 8000

# Use a simple entry point that keeps the container running
CMD ["tail", "-f", "/dev/null"] 