from django.core.management.base import BaseCommand
import requests
from xml.etree.ElementTree import fromstring
from book.models import Value


class Command(BaseCommand):
    help = 'Get exchange rate'

    def handle(self, *args, **kwargs):
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
