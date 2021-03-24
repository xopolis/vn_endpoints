FROM python:3.7-stretch

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_lg

COPY . /app/

ENTRYPOINT ["python", "server.py"]
