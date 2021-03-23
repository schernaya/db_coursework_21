class Rating:

    def __init__(self, rating_id, user_id, app_id, rating, rating_date, comment=None):
        self.rating_id = rating_id
        self.user_id = user_id
        self.app_id = app_id
        self.rating = rating
        self.rating_date = rating_date
        self.comment = comment


