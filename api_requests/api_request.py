# GET https://geocode-maps.yandex.ru/1.x
#  ? geocode=<string>
#  & apikey=<string>
#  & [sco=<string>]
#  & [kind=<string>]
#  & [rspn=<boolean>]
#  & [ll=<number>, <number>]
#  & [spn=<number>, <number>]
#  & [bbox=<number>,<number>~<number>,<number>]
#  & [format=<string>]
#  & [results=<integer>]
#  & [skip=<integer>]
#  & [lang=<string>]
#  & [callback=<string>]

# GET https://api.weather.yandex.ru/v2/forecast?
#  lat=<широта>
#  & lon=<долгота>
#  & [lang=<язык ответа>]
#  & [limit=<срок прогноза>]
#  & [hours=<наличие почасового прогноза>]
#  & [extra=<подробный прогноз осадков>]

# X-Yandex-API-Key: <значение ключа>

import json

import requests

from api_requests import api_config

@api_config.api(apikey=api_config.keys['apikey_geo'])
def get_city_location(city: str, apikey: str):
    payload = dict(
        geocode=city,
        apikey=apikey,
        format='json'
    )
    request = requests.get('https://geocode-maps.yandex.ru/1.x', params=payload)
    js_req = json.loads(request.text)
    position = js_req['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    return position
    

@api_config.api(apikey=api_config.keys['apikey_weather'])
def get_weather(city: str, apikey_dict: dict[str]):
    payload = {key: value for key, value in
        zip(('lat', 'lon', 'lang'), get_city_location(city).split() + ['ru_RU'])
    }
    request = requests.get('https://api.weather.yandex.ru/v2/forecast?', params=payload, headers=apikey_dict)
    js_req = json.loads(request.text)
    return js_req
