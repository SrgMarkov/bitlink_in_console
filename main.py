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
    return response.json()['id']


def get_count_clicks(access_token, url):
    url_components = urlparse(url)
    bitly_url = f'https://api-ssl.bitly.com/v4/bitlinks/{url_components.netloc}{url_components.path}/clicks/summary'
    params = {'units': '-1'}
    api_auth = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(bitly_url, headers=api_auth, params=params)
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(access_token, url):
    url_components = urlparse(url)
    bitly_url = f'https://api-ssl.bitly.com/v4/bitlinks/{url_components.netloc}{url_components.path}'
    api_auth = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(bitly_url, headers=api_auth)
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    bitly_token = os.getenv("BITLY_TOKEN")
    command_arguments = argparse.ArgumentParser(description='При вводе ссылки вида https://example.com создает '
                                                            'короткую ссылку вида bit.ly/random. При вводе короткой '
                                                            'ссылки - возвращает количество переходов по ней')
    command_arguments.add_argument('link', help='введите ссылку')
    args = command_arguments.parse_args()
    try:
        print(f'По вашей ссылке прошли {get_count_clicks(bitly_token, args.link)} раз(а)') if \
            is_bitlink(bitly_token, args.link) else print(f'Битлинк: {get_short_link(bitly_token, args.link)}')
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")

