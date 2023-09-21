FROM python:3.11.2-alpine

WORKDIR /app

COPY . .

RUN apk update && \
    apk add ffmpeg gcc python3-dev build-base git linux-headers && \
    pip install -r requirements.txt && \
    apk del git gcc python3-dev linux-headers build-base && \
    rm -rf /var/cache/apk/** /tmp/* /var/tmp/*

 

# Run the bot
CMD ["python3", "start_bot.py"]
