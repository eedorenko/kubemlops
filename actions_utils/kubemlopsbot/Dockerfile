FROM python:3.7.4-slim-buster
COPY . /bot/
WORKDIR bot
RUN pip install -r requirements.txt --upgrade
CMD ["python", "kubemlopsbotserver.py"]