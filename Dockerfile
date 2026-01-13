FROM python:3.9-alpine as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --prefix=/install -r requirements.txt

FROM python:3.9-alpine

WORKDIR /app

COPY --from=builder /install /usr/local

COPY app.py .

CMD ["python", "-u", "app.py"]
