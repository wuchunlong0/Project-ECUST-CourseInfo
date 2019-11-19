FROM python
LABEL author='wu-wenxiang@outlook.com'

RUN apt-get update \
    && apt-get install -y nginx supervisor systemd vim cron \
    && pip install gunicorn \
    && pip install setuptools \
    && pip install gevent \
    && pip install ansible==2.9 \
    && pip install django==2.2.6 \
    && pip install django-filter \
    && pip install monthdelta \
    && pip install Pillow \
    && pip install xlrd \
    && pip install xlsxwriter \
    && pip install pypinyin \
    && pip install sqlalchemy

ENV PYTHONIOENCODING=utf-8