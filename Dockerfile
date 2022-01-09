FROM python:latest

COPY src /
ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt

CMD [ "python", "/app.py" ]