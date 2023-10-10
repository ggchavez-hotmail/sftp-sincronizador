FROM python:3.11.5-slim-bullseye AS develop

RUN apt-get update && \
    apt-get install -y ssh && \
    ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa

WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .

ENV DB_CONEXION=VALUE
ENV DB_NAME=VALUE
ENV DB_CLL_JOURNAL=VALUE
ENV DB_CLL_PARAMS=VALUE

CMD ["python", "main.py"]