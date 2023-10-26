FROM python:3.11

RUN mkdir /notification_app

WORKDIR /notification_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE $PORT

CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=127.0.0.1:$PORT