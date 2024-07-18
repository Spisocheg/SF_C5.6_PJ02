import requests
import json

from config import EXCHANGERATE_API


VALUES = {'EUR': ['Евро', 'Euro', 'EUR'],
          'USD': ['Доллар', 'Dollar', 'USD', 'Доллар США', 'US Dollar'],
          'RUB': ['Рубль', 'Ruble', 'RUB', 'Российский рубль', 'Russian ruble']}


class ValuesManager:
    @staticmethod
    def get_price(base, quote, amount) -> float:
        response_json = json.loads(
            requests.get(f'https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API}/pair/{base}/{quote}').content)

        return round(response_json['conversion_rate'] * amount, 2)


class APIException(Exception):
    pass
