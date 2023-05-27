import os
import argparse
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


def get_short_link(access_token, url):
    bitly_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    query = {"long_url": url}
    api_auth = {'Authorization': f'Bearer {access_token}'}
    response = requests.post(bitly_url, headers=api_auth, json=query)
    response.raise_for_status()
    bitlink = response.json()["link"][8:]
    return f'Битлинк: {bitlink}'


def get_count_clicks(access_token, url):
    parsed = urlparse(url)
    bitly_url = f'https://api-ssl.bitly.com/v4/bitlinks/{parsed.netloc}{parsed.path}/clicks/summary'
    params = {'units': '-1'}
    api_auth = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(bitly_url, headers=api_auth, params=params)
    response.raise_for_status()
    bitlink = str(response.json()["total_clicks"])
    return f'По вашей ссылке прошли {bitlink} раз(а)'


def is_bitlink(access_token, url):
    parsed = urlparse(url)
    bitly_url = f'https://api-ssl.bitly.com/v4/bitlinks/{parsed.netloc}{parsed.path}'
    api_auth = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(bitly_url, headers=api_auth)
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    bitly_token = os.getenv("BITLY_TOKEN")
    parser = argparse.ArgumentParser(description='При вводе ссылки вида https://example.com создает короткую ссылку '
                                                 'вида bit.ly/random. При вводе короткой ссылки - возвращает '
                                                 'количество переходов по ней')
    parser.add_argument('link', help='введите ссылку')
    args = parser.parse_args()
    try:
        print(get_count_clicks(bitly_token, args.link)) if is_bitlink(bitly_token, args.link) \
            else print(get_short_link(bitly_token, args.link))
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")

