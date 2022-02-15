FROM python:3.9-slim

COPY app/ /app
COPY requirements.txt /app/requirements.txt

EXPOSE 5000

WORKDIR /app
RUN pip install -r requirements.txt

CMD [ "python", "./app.py" ]
