FROM python:3.11.5-slim-bullseye AS develop

RUN apt-get update && \
    apt-get install -y ssh && \
    ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa

WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD src/. .

ENV DB_CONEXION=VALUE
ENV DB_NAME=VALUE
ENV DB_CLL_JOURNAL=VALUE
ENV DB_CLL_PARAMS=VALUE
ENV ENCRYPTION_KEY=VALUE

#Comando para ejecutar proceso principal
#CMD ["python", "main.py"]

#Comandos para ejecutar comando ciclico
#ENTRYPOINT ["top", "-b"]
#CMD ["-c"]

#Configurar para ofelia
CMD tail -f /dev/null