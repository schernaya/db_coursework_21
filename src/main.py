import psycopg2

from controller import Controller

conn = psycopg2.connect(dbname='play_store', user='postgres',
                        password='postgres', host='localhost')


def main():
    c = Controller(conn)
    c.start()
    exit(0)


if __name__ == '__main__':
    main()
