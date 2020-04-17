import atexit
import psycopg2


def con() -> psycopg2:
    print('Connecting to PostgreSQL DB')
    conn: psycopg2 = \
        psycopg2.connect(user='postgres', password='admin', host='127.0.0.1', port='5432', database='postgres')

    def clean_up() -> None:
        conn.close()
        print('Closing connection', conn)

    atexit.register(clean_up)
    return conn


def main() -> None:
    con()
    print('hello')


if __name__ == '__main__':
    main()
