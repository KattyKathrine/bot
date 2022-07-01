import requests
import json
from config import currancies

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def check_input(mes, bot, cur1, cur2, n):

        try:
            if cur1 not in currancies.keys() or cur2 not in currancies.keys():
                raise APIException("Такой валюты нет в списке доступных валют.\n\
Увидеть список доступных валют:\n\
/values")

            if cur1 == cur2:
                raise APIException("Нужно указать разные валюты из списка")

            float(n)

        except APIException as err:
            bot.reply_to(mes, str(err))
        except ValueError:
            bot.reply_to(mes, "Количество переводимой валюты необходимо указать числом")

        else:
            return True

    @staticmethod
    def get_price(cur1, cur2, n):

        r = requests.get(f'https://currate.ru/api/?get=rates&pairs={currancies[cur1] + currancies[cur2]}&key=здесь_был_ключ')
        rate = json.loads(r.content)['data'][currancies[cur1] + currancies[cur2]]
        return float(n) * float(rate)
