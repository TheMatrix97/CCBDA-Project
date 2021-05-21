FROM python:3.8-buster
COPY docker_entrypoint.py requirements.txt JobIssuer.py ./
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "docker_entrypoint.py"]