import atexit
import json
import psycopg2
import requests


class Country:
    def __init__(self, country: str, pd: int, i: int, m: int, ua: int, lto: int, ind: int):
        self.country: str = country
        self.pd: int = pd
        self.i: int = i
        self.m: int = m
        self.ua: int = ua
        self.lto: int = lto
        self.ind: int = ind

    def data(self):
        return [self.country, self.pd, self.i, self.m, self.ua, self.lto, self.ind]


def con() -> psycopg2:
    print('Connecting to PostgreSQL DB')
    conn: psycopg2 = \
        psycopg2.connect(user='postgres', password='admin', host='127.0.0.1', port='5432', database='postgres')

    def clean_up() -> None:
        conn.close()
        print('Closing connection', conn)

    atexit.register(clean_up)
    return conn


conn: psycopg2 = con()


def get_json() -> str:
    url: str = 'https://www.hofstede-insights.com/wp-json/v1/country'
    return requests.get(url).text


def main() -> None:
    print(get_json())


if __name__ == '__main__':
    main()
