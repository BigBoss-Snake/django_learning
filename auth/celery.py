import os
from celery import Celery
from celery.schedules import crontab
import requests
from xml.etree.ElementTree import fromstring


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth.settings')

app = Celery('auth')
app.config_from_object('django.conf:settings')
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Moscow',
    enable_utc=True,
)

app.autodiscover_tasks()


@app.task
def lol():
    print('HelloWorld!')
    return('Hello World!')


@app.task
def get_rate():
    from book.models import Value
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?'
    data = requests.get(url)
    xml = fromstring(data.text)

    usd = xml.find("Valute[@ID='R01235']/Value").text
    eur = xml.find("Valute[@ID='R01239']/Value").text

    usd_obj = Value.objects.get(title='Usd')
    eur_obj = Value.objects.get(title='Eur')

    usd_obj.count = float(usd.replace(',', '.'))
    eur_obj.count = float(eur.replace(',', '.'))

    usd_obj.save()
    eur_obj.save()
    print('Ok')


app.conf.beat_schedule = {
    'get rate': {
        'task': 'auth.celery.get_rate',
        'schedule': crontab(hour=6),
    },
    'test': {
        'task': 'auth.celery.lol',
        'schedule': crontab(),
    },
}
