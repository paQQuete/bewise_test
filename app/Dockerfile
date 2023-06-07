FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
WORKDIR /opt/app/src
COPY requirements.txt ./requirements.txt
COPY entrypoint.sh ./entrypoint.sh
RUN pip install --upgrade pip && pip install -r requirements.txt

RUN apt -y update && apt -y install netcat

EXPOSE 8000
COPY src ./
RUN chmod 777 /opt/appapp/src/entrypoint.sh
ENTRYPOINT ["/opt/app/src/entrypoint.sh"]

