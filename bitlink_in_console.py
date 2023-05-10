import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv



def get_short_link(access_token, url):
    url_bitly = 'https://api-ssl.bitly.com/v4/bitlinks'
    query = {"long_url": url}
    response = requests.post(url_bitly, headers=access_token, json=query)
    response.raise_for_status()
    bitlink = 'Битлинк: ' + response.json()['link'][8:]
    return bitlink


def get_count_clicks(access_token, url):
    parsed = urlparse(url)
    url_bitly = f'https://api-ssl.bitly.com/v4/bitlinks/{parsed.netloc}{parsed.path}/clicks/summary'
    params = {'units': '-1'}
    response = requests.get(url_bitly, headers=access_token, params=params)
    response.raise_for_status()
    bitlink = 'По вашей ссылке прошли ' + str(response.json()['total_clicks']) + ' раз(а)'
    return bitlink


def is_bitlink(access_token, url):
    parsed = urlparse(url)
    url_bitly = f'https://api-ssl.bitly.com/v4/bitlinks/{parsed.netloc}{parsed.path}'
    response = requests.get(url_bitly, headers=access_token)
    return response.ok


def main():
    load_dotenv()
    token = {'Authorization': f'Bearer {os.getenv("BITLY_TOKEN")}'}
    link = input('Введите ссылку: ')
    try:
        print(get_count_clicks(token, link)) if is_bitlink(token, link) else print(get_short_link(token, link))
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")


if __name__ == '__main__':
    main()

