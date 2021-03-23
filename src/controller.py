from view import View
from model import Model

from models.app import App
from models.developer import Developer
from models.user import User
from models.rating import Rating

from generation.main import generate_apps, \
    generate_developers, generate_reviews, \
    generate_users

from visualisation.graphs import visualize_top_entities, \
    visualize_piechart, visualize_dates, index_results


class Controller:

    def __init__(self, conn):
        self.model = Model(conn)
        self.view = View()

    def menu(self, methods, methods_list):
        while True:
            try:
                self.view.numerated_array(methods_list)
                method_id = self.view.get_int('number:')
                if method_id is None:
                    raise ValueError('You need to enter action')
                elif method_id == 0:
                    break
                methods[method_id]()
            except Exception as err:
                self.view.show_error(err)

    def start(self):
        methods_list = ['exit', 'entity menu', 'graph analysis menu',
                        'generation menu', 'search menu']

        methods = {
            1: lambda: self.entity_menu(),
            2: lambda: self.graph_menu(),
            3: lambda: self.generation_menu(),
            4: lambda: self.search_menu(),
        }
        self.menu(methods, methods_list)

    def entity_menu(self):
        actions_list = ['go back',
                        'get apps', 'get developers', 'get users',
                        'get app', 'get developer', 'get user', 'get rating',
                        'update app', 'update developer', 'update user', 'update rating',
                        'add app', 'add developer', 'add user', 'add rating',
                        'delete app', 'delete developer', 'delete user', 'delete rating', 'delete developer app'
                        ]
        actions = {
            1: lambda: self.get_apps(),
            2: lambda: self.get_developers(),
            3: lambda: self.get_users(),
            4: lambda: self.get_app(self.view.get_int('app id')),
            5: lambda: self.get_developer(self.view.get_int('developer id')),
            6: lambda: self.get_user(self.view.get_int('user id')),
            7: lambda: self.get_rating(self.view.get_int('app id'), self.view.get_int('user id')),
            8: lambda: self.update_app(self.edit_app(self.view.get_int('app id'))),
            9: lambda: self.update_developer(self.edit_developer(self.view.get_int('dev id'))),
            10: lambda: self.update_user(self.edit_user(self.view.get_int('user id'))),
            11: lambda: self.update_rating(self.edit_rating(self.view.get_int('app id'), self.view.get_int('user id'))),
            12: lambda: self.add_app(self.create_app()),
            13: lambda: self.add_developer(self.create_developer()),
            14: lambda: self.add_user(self.create_user()),
            15: lambda: self.add_rating(self.create_rating()),
            16: lambda: self.delete_app(self.view.get_int('app id')),
            17: lambda: self.delete_developer(self.view.get_int('developer id')),
            18: lambda: self.delete_user(self.view.get_int('user id')),
            19: lambda: self.delete_rating(self.view.get_int('app id'), self.view.get_int('user id')),
            20: lambda: self.delete_developer_app(self.view.get_int('developer id'), self.view.get_int('app id')),
        }
        self.menu(actions, actions_list)

    def search_menu(self):
        actions_list = ['go back',
                        'search apps by similar title and category',
                        'search developers by app rating and released date',
                        'search users by similar comments']

        actions = {
            1: lambda: self.search_apps(self.view.get_str('title'), self.view.get_str('category')),
            2: lambda: self.search_developers(self.view.get_str('rating'),
                                              self.view.get_date('released_date_from'),
                                              self.view.get_date('released_date_to')),
            3: lambda: self.search_users(self.view.get_str('comment'))
        }
        self.menu(actions, actions_list)

    def graph_menu(self):
        actions_list = ['go back',
                        'top apps by installs', 'top categories', 'top developers',
                        'types statistics', 'released_dates_statistics']

        actions = {
            1: lambda: visualize_top_entities(
                self.model.get_top_apps(), 'top_apps'),
            2: lambda: visualize_top_entities(
                self.model.get_top_categories(),
                'top_categories'),
            3: lambda: visualize_top_entities(
                self.model.get_top_developers(),
                'top_developers'),
            4: lambda: visualize_piechart(
                self.model.types_statistics(),
                'types_statistics'),
            5: lambda: visualize_dates(
                self.model.released_date_statistics(),
                'released_date_statistics'),
            6: lambda: index_results('index_results')
        }
        self.menu(actions, actions_list)

    def generation_menu(self):
        actions_list = ['go back',
                        'generate apps', 'generate developers',
                        'generate users', 'generate rating']

        actions = {
            1: lambda: self.generate_apps(self.view.get_int('quantity')),
            2: lambda: self.generate_developers(self.view.get_int('quantity')),
            3: lambda: self.generate_users(self.view.get_int('quantity')),
            4: lambda: self.generate_ratings(self.view.get_int('quantity'))
        }
        self.menu(actions, actions_list)

    # get operations

    def get_apps(self):
        return self.view.list_str(self.model.get_apps(), 'App')

    def get_developers(self):
        return self.view.list_str(self.model.get_developers(), 'Developer')

    def get_users(self):
        return self.view.list_str(self.model.get_users(), 'User')

    def get_app(self, app_id):
        return self.view.list_str(self.model.get_app(app_id), 'App')

    def get_developer(self, developer_id):
        return self.view.list_str(self.model.get_developer(developer_id), 'Developer')

    def get_user(self, user_id):
        return self.view.list_str(self.model.get_user(user_id), 'User')

    def get_rating(self, app_id, user_id):
        return self.view.list_str(self.model.get_rating(app_id, user_id), 'Rating')

    # update operations

    def update_app(self, app):
        if app:
            return self.view.list_str(self.model.update_app(app), 'App', 'Updated')

    def update_developer(self, developer):
        if developer:
            return self.view.list_str(self.model.update_developer(developer), 'Developer', 'Updated')

    def update_user(self, user):
        if user:
            return self.view.list_str(self.model.update_user(user), 'User', 'Updated')

    def update_rating(self, rating):
        if rating:
            return self.view.list_str(self.model.update_rating(rating), 'Rating', 'Updated')

    # add operations

    def add_app(self, app):
        return self.view.list_str(self.model.add_app(app), 'App', 'Added')

    def add_developer(self, developer):
        return self.view.list_str(self.model.add_developer(developer), 'Developer', 'Added')

    def add_user(self, user):
        return self.view.list_str(self.model.add_user(user), 'User', 'Added')

    def add_rating(self, rating):
        return self.view.list_str(self.model.app_rating(rating), 'Rating', 'Added')

    # delete operations

    def delete_app(self, app_id):
        return self.view.list_str(self.model.delete_app(app_id), 'App', 'Deleted')

    def delete_developer(self, dev_id):
        return self.view.list_str(self.model.delete_developer(dev_id), 'Developer', 'Deleted')

    def delete_user(self, user_id):
        return self.view.list_str(self.model.delete_user(user_id), 'User', 'Deleted')

    def delete_rating(self, app_id, user_id):
        return self.view.list_str(self.model.delete_rating(app_id, user_id), 'Rating', 'Deleted')

    def delete_developer_app(self, developer_id, app_id):
        return self.view.list_str(self.model.delete_developer_app(developer_id, app_id), 'Link', 'Deleted')

    # generate operations

    def generate_apps(self, quantity):
        return self.view.list_str(generate_apps(quantity), 'App', 'Generated')

    def generate_developers(self, quantity):
        return self.view.list_str(generate_developers(quantity), 'Developer', 'Generated')

    def generate_users(self, quantity):
        return self.view.list_str(generate_users(quantity), 'User', 'Generated')

    def generate_ratings(self, quantity):
        return self.view.list_str(generate_reviews(quantity), 'Rating', 'Generated')

    # search operations

    def search_apps(self, title, category):
        return self.view.list_str(self.model.search_apps(title, category), 'App')

    def search_developers(self, rating, released_date_from, released_date_to):
        return self.view.list_str(self.model.search_developers(rating, released_date_from, released_date_to),
                                  'Developer')

    def search_users(self, comment):
        return self.view.list_str(self.model.search_users(comment), 'User')

    # edit operations

    def edit_app(self, app_id):
        app = self.model.get_app(app_id)
        self.view.list_str(app, 'App')
        options = ['app_name', 'size', 'installs',
                   'type_id', 'category_id']
        while True:
            try:
                self.view.numerated_array(options)
                option = self.view.get_int('number')
                if option == 0:
                    app_name = self.view.get_str('app name')
                    if app_name is None:
                        raise ValueError(self.view.show_error('app name'))
                    app['app_name'] = app_name
                elif option == 1:
                    size = self.view.get_int('size')
                    if size is None:
                        raise ValueError(self.view.show_error('size'))
                    app['size'] = size
                elif option == 2:
                    installs = self.view.get_int('installs')
                    if installs is None:
                        raise ValueError(self.view.show_error('installs'))
                    app['installs'] = installs
                elif option == 3:
                    type_id = self.view.get_int('type_id')
                    if type_id is not None and not 1 <= type_id <= 3:
                        self.view.show_error('type id', 'input')
                    app['type_id'] = type_id
                elif option == 4:
                    category_id = self.view.get_int('category id')
                    if category_id is not None and not 1 <= category_id <= 47:
                        raise ValueError(self.view.show_error('category id'))
                    app['category_id'] = category_id
                else:
                    raise ValueError('You need to enter action')
                return App(app['app_id'], app['app_name'], app['size'],
                           app['installs'], app['type_id'], app['category_id'])
            except Exception as err:
                self.view.show_error(err)

    def edit_developer(self, dev_id):
        developer = self.model.get_developer(dev_id)
        self.view.list_str(developer, 'Developer')
        options = ['dev_name', 'email', 'website']
        while True:
            try:
                self.view.numerated_array(options)
                option = self.view.get_int('number')
                if option == 0:
                    dev_name = self.view.get_str('developer name')
                    if dev_name is None:
                        raise ValueError(self.view.show_error('developer name'))
                    developer['dev_name'] = dev_name
                elif option == 1:
                    email = self.view.get_str('email')
                    if email is None:
                        raise ValueError(self.view.show_error('email'))
                    developer['email'] = email
                elif option == 2:
                    website = self.view.get_str('website')
                    developer['website'] = website
                else:
                    raise ValueError('You need to enter action')
                return Developer(developer['dev_id'], developer['dev_name'],
                                 developer['email'], developer['website'])
            except Exception as err:
                self.view.show_error(err)

    def edit_user(self, user_id):
        user = self.model.get_user(user_id)
        self.view.list_str(user, 'User')
        options = ['username', 'fullname', 'registration_date']
        while True:
            try:
                self.view.numerated_array(options)
                option = self.view.get_int('number')
                if option == 0:
                    username = self.view.get_str('username')
                    if username is None:
                        raise ValueError(self.view.show_error('username'))
                    user['username'] = username
                elif option == 1:
                    fullname = self.view.get_str('fullname')
                    if fullname is None:
                        raise ValueError(self.view.show_error('fullname'))
                    user['fullname'] = fullname
                elif option == 2:
                    registration_date = self.view.get_date('registration date')
                    if registration_date is None:
                        raise ValueError(self.view.show_error('registration date'))
                    user['registration_date'] = registration_date
                else:
                    raise ValueError('You need to enter action')
                return User(user['user_id'], user['username'],
                            user['fullname'], user['registration_date'])
            except Exception as err:
                self.view.show_error(err)

    def edit_rating(self, app_id, user_id):
        rating = self.model.get_rating(app_id, user_id)
        self.view.list_str(rating, 'Rating')
        options = ['user_id', 'app_id', 'rating', 'rating_date', 'comment']
        while True:
            try:
                self.view.numerated_array(options)
                option = self.view.get_int('number')
                if option == 0:
                    user_id = self.view.get_int('user_id')
                    if user_id is None:
                        raise ValueError(self.view.show_error('user_id'))
                    rating['user_id'] = user_id
                elif option == 1:
                    app_id = self.view.get_int('app_id')
                    if app_id is None:
                        raise ValueError(self.view.show_error('app_id'))
                    rating['app_id'] = app_id
                elif option == 2:
                    value = self.view.get_float('rating')
                    if value is None or not 1.0 <= value <= 5.0:
                        raise ValueError(self.view.show_error('rating'))
                    rating['rating'] = value
                elif option == 3:
                    rating_date = self.view.get_date('rating date')
                    if rating_date is None:
                        raise ValueError(self.view.show_error('rating date'))
                    rating['rating_date'] = rating_date
                elif option == 4:
                    comment = self.view.get_str('comment')
                    rating['comment'] = comment
                else:
                    raise ValueError('You need to enter action')
                return Rating(rating['link_id'], rating['user_id'],
                              rating['app_id'], rating['rating'],
                              rating['rating_date'], rating['comment'])
            except Exception as err:
                self.view.show_error(err)

    # create operations

    def create_app(self):
        try:
            app_name = self.view.get_str('app name')
            if app_name is None:
                raise ValueError(self.view.show_error('app name'))
            size = self.view.get_int('size')
            if size is None:
                raise ValueError(self.view.show_error('size'))
            installs = self.view.get_int('installs')
            if installs is None:
                raise ValueError(self.view.show_error('installs'))
            type_id = self.view.get_int('type id')
            if type_id is not None and not 1 <= type_id <= 3:
                raise ValueError(self.view.show_error('type id', 'input'))
            category_id = self.view.get_int('category id')
            if category_id is not None and not 1 <= category_id <= 47:
                raise ValueError(self.view.show_error('category id'))
            return App(0, app_name, size, installs, type_id, category_id)
        except Exception as err:
            self.view.show_error(err)

    def create_developer(self):
        try:
            dev_name = self.view.get_str('developer name')
            if dev_name is None:
                raise ValueError(self.view.show_error('developer name'))
            email = self.view.get_str('email')
            if email is None:
                raise ValueError(self.view.show_error('email'))
            website = self.view.get_str('website')
            return Developer(0, dev_name, email, website)
        except Exception as err:
            self.view.show_error(err)

    def create_user(self):
        try:
            username = self.view.get_str('username')
            if username is None:
                raise ValueError(self.view.show_error('username'))
            fullname = self.view.get_str('fullname')
            if fullname is None:
                raise ValueError(self.view.show_error('fullname'))
            registration_date = self.view.get_date('registration date')
            if registration_date is None:
                raise ValueError(self.view.show_error('registration date'))
            return User(0, username, fullname, registration_date)
        except Exception as err:
            self.view.show_error(err)

    def create_rating(self):
        try:
            user_id = self.view.get_int('user id')
            if user_id is None:
                raise ValueError(self.view.show_error('user id'))
            app_id = self.view.get_int('app id')
            if app_id is None:
                raise ValueError(self.view.show_error('app id'))
            rating = self.view.get_float('rating')
            if rating is None or not 1.0 <= rating <= 5.0:
                raise ValueError(self.view.show_error('rating'))
            rating_date = self.view.get_date('rating date')
            if rating_date is None:
                raise ValueError(self.view.show_error('rating date'))
            comment = self.view.get_str('comment')
            return Rating(0, user_id, app_id, rating, rating_date, comment)
        except Exception as err:
            self.view.show_error(err)
