FROM python:3.7.9

COPY . /webfinalwork
WORKDIR /webfinalwork

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]