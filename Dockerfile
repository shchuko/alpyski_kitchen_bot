FROM python:alpine3.18

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

COPY ./src /app

WORKDIR /app
CMD [ "python", "./bot.py" ]