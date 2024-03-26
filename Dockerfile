FROM --platform=linux/amd64 python:3.9-slim 

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir  -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]