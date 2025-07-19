FROM python:3.11

WORKDIR /app

COPY app.py .

RUN pip install aiokafka asyncio

CMD ["python", "app.py"]
