# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port (optional, useful for webhooks)
EXPOSE 8080

# Run the bot
CMD ["python", "bot.py"]
