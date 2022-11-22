FROM python:3.9-alpine as builder

WORKDIR /opt/

COPY ["api_db.py", "/opt/"]
COPY ["news_db.py", "/opt/"]

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt
RUN apk add curl jq

FROM builder

CMD ["python3.9", "api_db.py"]