FROM python:3.8.10
WORKDIR /auth
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE auth.settings
ENV PYTHONDONTWRITEBYTECODE=1
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
ADD manage.py /
CMD ["python"]