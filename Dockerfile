FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create directory for database
RUN mkdir -p /app/data

# Set environment variable for database path
ENV DATABASE_PATH=/app/data/bot_database.db

# Run the bot
CMD ["python", "bot.py"]
