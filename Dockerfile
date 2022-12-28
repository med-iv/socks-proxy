FROM python:3.7.15-alpine3.17
COPY server.py server.py
ENTRYPOINT ["python3", "server.py"]
