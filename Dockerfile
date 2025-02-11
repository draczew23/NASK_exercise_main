FROM python:3.12

COPY requirements.txt /
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt

COPY . /app
WORKDIR /app
EXPOSE 8080

CMD ["gunicorn","--config", "gunicorn_config.py", "app:app"]