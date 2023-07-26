FROM python:3.9-slim
RUN pip3 install --upgrade pip
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN python3 app.py
