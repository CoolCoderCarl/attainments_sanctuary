FROM python:3.9-alpine as builder

COPY ["api_db.py", "/opt/"]
COPY ["news_db.py", "/opt/"]

COPY requirements-db.txt requirements-db.txt

RUN pip3 install --no-cache-dir -r requirements-db.txt

FROM builder

CMD ["python3.9", "/opt/api_db.py"]