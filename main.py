import os
import argparse
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


def get_short_link(access_token, url):
    url_bitly = 'https://api-ssl.bitly.com/v4/bitlinks'
    query = {"long_url": url}
    api_auth = {'Authorization': f'Bearer {access_token}'}
    response = requests.post(url_bitly, headers=api_auth, json=query)
    response.raise_for_status()
    bitlink = 'Битлинк: ' + response.json()['link'][8:]
    return bitlink


def get_count_clicks(access_token, url):
    parsed = urlparse(url)
    url_bitly = f'https://api-ssl.bitly.com/v4/bitlinks/{parsed.netloc}{parsed.path}/clicks/summary'
    params = {'units': '-1'}
    api_auth = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url_bitly, headers=api_auth, params=params)
    response.raise_for_status()
    bitlink = 'По вашей ссылке прошли ' + str(response.json()['total_clicks']) + ' раз(а)'
    return bitlink


def is_bitlink(access_token, url):
    parsed = urlparse(url)
    url_bitly = f'https://api-ssl.bitly.com/v4/bitlinks/{parsed.netloc}{parsed.path}'
    api_auth = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url_bitly, headers=api_auth)
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
