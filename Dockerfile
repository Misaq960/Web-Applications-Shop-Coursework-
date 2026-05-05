FROM python:3.10.4-bullseye

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r ./requirements.txt

COPY . /usr/src/app
WORKDIR /usr/src/app/shop_app

RUN chmod -R g+w /usr/src/app/shop_app/instance

CMD gunicorn --bind 0.0.0.0:5000 shopApp:app
