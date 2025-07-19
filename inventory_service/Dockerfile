FROM python:3.11

WORKDIR /app

COPY inventory_service.py .

RUN pip install fluent-logger

CMD ["python", "inventory_service.py"]
