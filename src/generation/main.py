import psycopg2

from psycopg2.extras import DictCursor
from csv_parse.main import csv_parse

from google_play_scraper import scrape_reviews, scrape_apps

connection = psycopg2.connect(dbname='play_store', user='postgres',
                              password='postgres', host='localhost')
connection.autocommit = True
cursor = connection.cursor(cursor_factory=DictCursor)


def generate_apps(quantity):
    fields = ['App Name', 'Size', 'Installs', 'Type', 'Category']
    dict_data = csv_parse('../data/csv/Google-Playstore.csv', fields, quantity)
    new_apps = []

    for row in dict_data:
        cursor.execute('SELECT * FROM apps_types WHERE type = %s  ', (row['Type'],))
        type_exists = cursor.fetchone()
        if not type_exists:
            cursor.execute('INSERT INTO apps_types (type) '
                           'VALUES (%s) RETURNING * ', (row['Type'],))
            type_exists = cursor.fetchone()

        cursor.execute('SELECT * FROM apps_categories WHERE category = %s  ', (row['Category'],))
        category_exits = cursor.fetchone()
        if not category_exits:
            cursor.execute('INSERT INTO apps_categories (category) '
                           'VALUES (%s) RETURNING *', (row['Category'],))
            category_exits = cursor.fetchone()

        cursor.execute('INSERT INTO apps '
                       '(app_name, size, installs, '
                       'type_id, category_id) '
                       'VALUES (%s, %s, %s, %s, %s) '
                       'RETURNING *',
                       (row['App Name'], row['Size'], row['Installs'],
                        type_exists['type_id'], category_exits['category_id']))

        new_app = cursor.fetchone()
        new_apps.append(dict(new_app))

    return new_apps


def generate_developers(quantity):
    fields = ['Developer Id', 'Developer Website', 'Developer Email', 'Released', 'App Name']
    dict_data = csv_parse('../data/csv/Google-Playstore.csv', fields, quantity)
    new_developers = []

    for row in dict_data:
        cursor.execute('INSERT INTO developers '
                       '(dev_name, email, website) '
                       'VALUES (%s, %s, %s) '
                       'RETURNING *',
                       (row['Developer Id'], row['Developer Website'],
                        row['Developer Email']))
        new_developer = cursor.fetchone()
        new_developers.append(dict(new_developer))

        cursor.execute('SELECT * FROM apps WHERE app_name = %s  ', (row['App Name'],))
        app = cursor.fetchone()
        if app:
            cursor.execute('INSERT INTO dev_app_links '
                           '(app_id, dev_id, released_date) '
                           'VALUES (%s, %s, %s) '
                           'RETURNING *',
                           (app['app_id'], new_developer['dev_id'],
                            row['Released']))
    return new_developers


app_packages = [
    'com.anydo',
    'com.todoist',
    'com.ticktick.task',
    'com.habitrpg.android.habitica',
    'cc.forestapp',
    'com.oristats.habitbull',
    'com.levor.liferpgtasks',
    'com.habitnow',
    'com.microsoft.todos',
    'prox.lab.calclock',
    'com.gmail.jmartindev.timetune',
    'com.artfulagenda.app',
    'com.tasks.android',
    'com.appgenix.bizcal',
    'com.appxy.planner'
]


def generate_users(quantity):
    users = scrape_reviews(app_packages, quantity)
    generated_users = []
    for user in users:
        fullname = user['userName']
        username = user['userName'].lower().replace(' ', '_')
        cursor.execute('INSERT INTO users '
                       '(username, fullname, registration_date) '
                       'VALUES (%s, %s, ((current_date - floor(random()* (365-0+ 1) + 0)*(\'1 '
                       'day\')::interval)::date)) '
                       'RETURNING *',
                       (username, fullname))
        row = cursor.fetchone()
        generated_users.append(dict(row))

    return generated_users


def generate_reviews(quantity):
    reviews = scrape_reviews(app_packages, quantity)
    generated_reviews = []
    for review in reviews:
        rating = review['score']
        comment = review['content']

        cursor.execute('INSERT INTO ratings '
                       '(user_id, app_id, rating, comment, rating_date) '
                       'VALUES (random_user_id(), random_app_id(), %s, %s, '
                       '((current_date - floor(random()* (365-0+ 1) + 0)*'
                       '(\'1 day\')::interval)::date)) '
                       'RETURNING *',
                       (rating, comment))
        row = cursor.fetchone()
        generated_reviews.append(dict(row))

    return generated_reviews
