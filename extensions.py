import requests
import json
from config import keys

# обработчик ошибок
class ConvertException(Exception):
    pass

# основной класс конвертера
class CryptoConvert():
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту: {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту: {base}')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise ConvertException(f'Не удалось обработать количество валюты: {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')

        total_amount = round(float(json.loads(r.content)[keys[base]]) * float(amount), 2)

        return str(total_amount)

