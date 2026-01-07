FROM python:3.12-slim-bookworm

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install FFmpeg with retries
RUN apt-get update -o Acquire::Retries=3 && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY konvert_app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY konvert_app ./konvert_app

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "konvert_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
