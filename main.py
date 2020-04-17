import atexit
import json
import psycopg2
import requests
from typing import List


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

    def __str__(self):
        return f'{self.country}({self.pd},{self.i},{self.m},{self.ua},{self.lto},{self.ind})'


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


def num_or_0(text: str) -> int:
    if text == '':
        return 0
    else:
        return int(text)


def json_to_list_obs(js: json) -> List[Country]:
    obs: List[Country] = []
    for j in js:
        obj: Country = Country(j['slug'],
                               int(j['pdi']),
                               int(j['idv']),
                               int(j['mas']),
                               int(j['uai']),
                               num_or_0(j['lto']),
                               num_or_0(j['ind'])
                               )
        obs.append(obj)

    return obs


def insert_sql(data: List[Country]) -> None:
    sql: str = 'INSERT INTO postgres.public.hofstede (country, power, individual, masculinity, uncertainty, longterm, indulgence) VALUES (%s, %s, %s, %s, %s, %s, %s)'

    cursor = conn.cursor()
    for d in data:
        cursor.execute(sql, d.data())

    conn.commit()
    cursor.close()


def main() -> None:
    json_obj: json = json.loads(get_json())
    obs: List[Country] = json_to_list_obs(json_obj)
    insert_sql(obs)


if __name__ == '__main__':
    main()
