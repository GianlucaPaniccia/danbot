FROM python:3.11-slim
RUN pip install --upgrade pip
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Create a folder for the database to live in
RUN mkdir -p /app/data
CMD ["python", "discord.py"]