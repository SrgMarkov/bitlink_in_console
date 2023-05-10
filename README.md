## Работа с сервисом [bit.ly](https://app.bitly.com/) в консоли

- Длинные ссылки `http://example.com` при вводе сокращаются до коротких `bit.ly/example`
- При вводе битлинка `bit.ly/example` - подсчет общего количества переходов по ней

### Как установить

- Python3 должен быть уже установлен
- в директории с файлами программы необходимо создать `.env` файл, в котором прописать **API** [bit.ly](https://app.bitly.com/)
```
BITLY_TOKEN=thisistoKeN4example
```
- Установить python-dotenv
```
pip install python-dotenv
```

### Основные функции

- `get_short_link` - получение короткой ссылки
- `get_count_clicks` - получение количества кликов по каороткой ссылке
- `is_bitlink` - проверка, является ли ссылка битлинком
