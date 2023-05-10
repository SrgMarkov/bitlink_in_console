import requests
from urllib.parse import urlparse
from settings import SECRET_KEY


def get_short_link(access_token, url):
    url_bitly = 'https://api-ssl.bitly.com/v4/bitlinks'
    query = {"long_url": url}
    try:
        response = requests.post(url_bitly, headers=access_token, json=query)
        response.raise_for_status()
        bitlink = 'Битлинк: ' + response.json()['link'][8:]
        return bitlink
    except requests.exceptions.RequestException as e:
        return f"Ошибка при выполнении запроса: {e}"


def get_count_clicks(access_token, url):
    parsed = urlparse(url)
    url_bitly = f'https://api-ssl.bitly.com/v4/bitlinks/{parsed.netloc}{parsed.path}/clicks/summary'
    params = {'units': '-1'}
    try:
        response = requests.get(url_bitly, headers=access_token, params=params)
        response.raise_for_status()
        bitlink = 'По вашей ссылке прошли ' + str(response.json()['total_clicks']) + ' раз(а)'
        return bitlink
    except requests.exceptions.RequestException as e:
        return f"Ошибка при выполнении запроса: {e}"


def is_bitlink(access_token, url):
    parsed = urlparse(url)
    url_bitly = f'https://api-ssl.bitly.com/v4/bitlinks/{parsed.netloc}{parsed.path}'
    try:
        response = requests.get(url_bitly, headers=access_token)
        response.raise_for_status()
        return response.ok
    except requests.exceptions.RequestException as e:
        return f"Ошибка при выполнении запроса: {e}"


def main():
    token = {'Authorization': f'Bearer {SECRET_KEY}'}
    link = input('Введите ссылку: ')
    print(get_count_clicks(token, link)) if is_bitlink(token, link) else print(get_short_link(token, link))


if __name__ == '__main__':
    main()

