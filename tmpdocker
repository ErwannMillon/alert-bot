FROM python:3.8-slim

RUN pip install flask requests uvicorn

WORKDIR /app

COPY . .

EXPOSE 8000

CMD uvicorn bot:app

