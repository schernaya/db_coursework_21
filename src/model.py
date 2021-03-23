from psycopg2.extras import DictCursor


class Model(object):

    def __init__(self, connection):
        self.conn = connection
        self.conn.autocommit = True
        self.cursor = connection.cursor(cursor_factory=DictCursor)

    # get operations

    def get_apps(self):
        self.cursor.execute('SELECT * FROM apps')
        rows = self.cursor.fetchall()
        apps = []
        for row in rows:
            apps.append(dict(row))
        return apps

    def get_developers(self):
        self.cursor.execute('SELECT * FROM developers')
        rows = self.cursor.fetchall()
        developers = []
        for row in rows:
            developers.append(dict(row))
        return developers

    def get_users(self):
        self.cursor.execute('SELECT * FROM users')
        rows = self.cursor.fetchall()
        users = []
        for row in rows:
            users.append(dict(row))
        return users

    def get_app(self, app_id):
        self.cursor.execute('SELECT * FROM apps WHERE app_id = %s ', (app_id,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def get_developer(self, dev_id):
        self.cursor.execute('SELECT * FROM developers WHERE dev_id = %s ', (dev_id,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def get_user(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE user_id = %s ', (user_id,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def get_rating(self, app_id, user_id):
        self.cursor.execute('SELECT * FROM ratings WHERE app_id = %s AND user_id = %s',
                            (app_id, user_id,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    # update operations

    def update_app(self, app):
        self.cursor.execute('UPDATE apps '
                            'SET app_name = %s, size = %s, installs = %s, '
                            'type_id = %s, category_id = %s '
                            'WHERE app_id = %s '
                            'RETURNING *',
                            (app.app_name, app.size, app.installs,
                             app.type_id, app.category_id, app.app_id))
        row = self.cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def update_developer(self, developer):
        self.cursor.execute('UPDATE developers '
                            'SET dev_name = %s, email = %s, website = %s '
                            'WHERE dev_id = %s '
                            'RETURNING *',
                            (developer.dev_name, developer.email,
                             developer.website, developer.dev_id))
        row = self.cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def update_user(self, user):
        self.cursor.execute('UPDATE users '
                            'SET username = %s, fullname = %s, registration_date = %s '
                            'WHERE user_id = %s '
                            'RETURNING *',
                            (user.username, user.fullname, user.registration_date,
                             user.user_id))
        row = self.cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def update_rating(self, rating):
        self.cursor.execute('UPDATE ratings '
                            'SET rating = %s, rating_date = %s, comment = %s '
                            'WHERE user_id = %s AND app_id = %s '
                            'RETURNING *',
                            (rating.rating, rating.rating_date, rating.comment,
                             rating.user_id, rating.app_id))
        row = self.cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    # add operations

    def add_app(self, app):
        self.cursor.execute('INSERT INTO apps '
                            '(app_name, size, installs, '
                            'type_id, category_id) '
                            'VALUES (%s, %s, %s, %s, %s) '
                            'RETURNING *',
                            (app.app_name, app.size, app.installs,
                             app.type_id, app.category_id))
        row = self.cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def add_developer(self, developer):
        self.cursor.execute('INSERT INTO developers '
                            '(dev_name, email, website) '
                            'VALUES (%s, %s, %s) '
                            'RETURNING *',
                            (developer.dev_name, developer.email,
                             developer.website))
        row = self.cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def add_user(self, user):
        self.cursor.execute('INSERT INTO users '
                            '(username, fullname, registration_date) '
                            'VALUES (%s, %s, %s) '
                            'RETURNING *',
                            (user.username, user.fullname,
                             user.registration_date))
        row = self.cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def app_rating(self, rating):
        self.cursor.execute('INSERT INTO ratings '
                            '(user_id, app_id, rating, rating_date, comment) '
                            'VALUES (%s, %s, %s, %s, %s) '
                            'RETURNING *',
                            (rating.user_id, rating.app_id,
                             rating.rating, rating.rating_date, rating.comment))
        row = self.cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    # delete operations

    def delete_app(self, app_id):
        self.cursor.execute('DELETE FROM apps '
                            'WHERE app_id = %s '
                            'RETURNING *',
                            (app_id,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def delete_developer(self, dev_id):
        self.cursor.execute('DELETE FROM developers '
                            'WHERE dev_id = %s '
                            'RETURNING *',
                            (dev_id,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def delete_user(self, user_id):
        self.cursor.execute('DELETE FROM users '
                            'WHERE user_id = %s '
                            'RETURNING *',
                            (user_id,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def delete_rating(self, app_id, user_id):
        self.cursor.execute('DELETE FROM ratings '
                            'WHERE app_id = %s AND user_id = %s '
                            'RETURNING *',
                            (app_id, user_id,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def delete_developer_app(self, app_id, dev_id):
        self.cursor.execute('DELETE FROM dev_app_links '
                            'WHERE app_id = %s AND dev_id = %s '
                            'RETURNING *',
                            (app_id, dev_id,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    # search operations

    def search_apps(self, title, category):
        self.cursor.execute("SELECT app_id, app_name, size, installs, type_id, apps.category_id  FROM apps "
                            "INNER JOIN apps_categories "
                            "ON apps.category_id = apps_categories.category_id "
                            "WHERE \"app_name_tsv\" @@ plainto_tsquery(%s) "
                            "AND category = %s"
                            "ORDER BY ts_rank(\"app_name_tsv\", "
                            "plainto_tsquery(%s)) DESC ", (title, category, title))
        rows = self.cursor.fetchall()
        apps = []
        for row in rows:
            apps.append(dict(row))
        return apps

    def search_developers(self, rating, released_date_from, released_date_to):
        self.cursor.execute('WITH t AS (SELECT app_id, avg(rating) AS avg_stars '
                            'FROM ratings GROUP BY app_id) '
                            'SELECT developers.dev_id, dev_name, email from developers '
                            'INNER JOIN dev_app_links ON developers.dev_id = dev_app_links.dev_id '
                            'INNER JOIN t ON t.app_id = dev_app_links.app_id '
                            'WHERE t.avg_stars > %s AND released_date '
                            'BETWEEN %s AND %s ',
                            (rating, released_date_from, released_date_to))
        rows = self.cursor.fetchall()
        developers = []
        for row in rows:
            developers.append(dict(row))
        return developers

    def search_users(self, comment):
        self.cursor.execute("SELECT users.user_id, username, fullname, registration_date FROM users "
                            "INNER JOIN ratings ON ratings.user_id = users.user_id "
                            "WHERE \"comment_tsv\" @@ plainto_tsquery(%s) "
                            "ORDER BY ts_rank(\"comment_tsv\", "
                            "plainto_tsquery(%s)) DESC ", (comment, comment))
        rows = self.cursor.fetchall()
        users = []
        for row in rows:
            users.append(dict(row))
        return users

    # to analyze operations

    def get_top_apps(self):
        self.cursor.execute('SELECT * FROM apps ORDER BY installs DESC LIMIT 10 ')
        rows = self.cursor.fetchall()
        apps = []
        for row in rows:
            app = dict()
            app['name'] = row[1]
            app['installs'] = row[3]
            apps.append(app)
        return apps

    def get_top_categories(self):
        self.cursor.execute('SELECT distinct c.category, s.installs '
                            'FROM apps AS f '
                            'JOIN (SELECT category_id, SUM(installs) AS installs '
                            'FROM apps GROUP BY category_id) AS s '
                            'ON f.category_id = s.category_id '
                            'INNER JOIN apps_categories as c ON '
                            'c.category_id = f.category_id '
                            'ORDER BY installs DESC LIMIT 10 ')
        rows = self.cursor.fetchall()
        categories = []
        for row in rows:
            category = dict()
            category['name'] = row[0]
            category['installs'] = float(row[1])
            categories.append(category)
        return categories

    def get_top_developers(self):
        self.cursor.execute('SELECT distinct d.dev_name, s.installs '
                            'FROM developers AS d '
                            'INNER JOIN dev_app_links as l ON '
                            'l.dev_id = d.dev_id '
                            'INNER JOIN apps as a ON '
                            'a.app_id = l.app_id '
                            'JOIN (SELECT app_id, SUM(installs) AS installs '
                            'FROM apps GROUP BY app_id) AS s '
                            'ON a.app_id = s.app_id '
                            'ORDER BY installs DESC LIMIT 10')
        rows = self.cursor.fetchall()
        categories = []
        for row in rows:
            category = dict()
            category['name'] = row[0]
            category['installs'] = float(row[1])
            categories.append(category)
        return categories

    def types_statistics(self):
        self.cursor.execute('SELECT distinct c.type, s.installs '
                            'FROM apps AS f JOIN (SELECT type_id, '
                            'SUM(installs) AS installs '
                            'FROM apps GROUP BY type_id) '
                            'AS s ON  f.type_id = s.type_id '
                            'INNER JOIN apps_types as c '
                            'ON c.type_id = f.type_id '
                            'ORDER BY installs DESC LIMIT 10')
        rows = self.cursor.fetchall()
        types = []
        for row in rows:
            type = dict()
            type['name'] = row[0]
            type['installs'] = float(row[1])
            types.append(type)
        return types

    def released_date_statistics(self):
        self.cursor.execute('select released_date, count(released_date) as num '
                            'from dev_app_links group by released_date '
                            'order by released_date asc')
        rows = self.cursor.fetchall()
        data = []
        for row in rows:
            d = dict()
            d['date'] = row[0]
            d['number'] = row[1]
            data.append(d)
        return data
