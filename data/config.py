from configparser import ConfigParser


parser = ConfigParser()
parser.read(r'config.ini')


def set_value(section, key, value):
    parser.set(section, key, value)
    with open('config.ini', 'w') as configfile:
        parser.write(configfile)


class Telegram:
    section = 'telegram'
    token = parser.get(section, 'token')


class MySQL:
    section = 'mysql'
    host = parser.get(section, 'host')
    port = int(parser.get(section, 'port'))
    user = parser.get(section, 'user')
    password = parser.get(section, 'password')
    database = parser.get(section, 'database')


class Webhooks:
    section = 'webhooks'
    listen_address = parser.get(section, 'listen_address')
    listen_port = parser.getint(section, 'listen_port')
    base_url = parser.get(section, 'base_url')
    bot_path = parser.get(section, 'bot_path')


class Settings:
    section = 'settings'
    currency = parser.get(section, 'currency')
    payment_token = parser.get(section, 'payment_token')
    password = parser.get(section, 'password')
