FROM python:3

ADD requirements.txt /

RUN pip install -r requirements.txt

ADD script /script

WORKDIR script

CMD ["python3", "main.py"]
