"""
Скачивание PDF с ЕГРЮЛ-выпиской с сайта ФНС.
Ошибки не обрабатываем, весь код оборачиваем в try-except, поскольку если сломалось, мы ничего поделать не может.
"""

import requests
import time


BASE_URL = 'https://egrul.nalog.ru/'
REQUEST_URL = BASE_URL + 'vyp-request/'
SEARCH_URL = BASE_URL + 'search-result/'
STATUS_URL = BASE_URL + 'vyp-status/'
DOWNLOAD_URL = BASE_URL + 'vyp-download/'


def _init_request(inn):
    """ Инициолизация запроса """
    resp = requests.post(
        BASE_URL,
        data={'query': inn},
        headers={
            'Host': 'egrul.nalog.ru',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://egrul.nalog.ru/index.html',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        }
    )
    j = resp.json()
    t1 = j.get('t')

    resp = requests.get(SEARCH_URL + t1)
    j = resp.json()
    return j.get('rows')[0].get('t')


def _wait(t_code):
    """ Ожидание выполнения запроса. """
    requests.get(REQUEST_URL + t_code)
    counter = 0

    while True:
        time.sleep(0.2)
        counter += 1
        resp = requests.get(STATUS_URL + t_code)
        if resp.json().get('status') == 'ready' or counter > 5:
            return


def _download(t_code):
    """ Скачивание документа. """
    resp = requests.get(DOWNLOAD_URL + t_code)
    return resp.content


def download_pdf(inn):
    try:
        req_code = _init_request(inn)
        _wait(req_code)
        return _download(req_code)
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    download_pdf('5024085154')
