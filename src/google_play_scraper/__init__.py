import pandas as pd

from .constants.google_play import Sort
from .features.app import app
from .features.reviews import reviews, reviews_all

VERSION = __version__ = "0.1.2"


def scrape_reviews(app_packages, quantity):
    app_reviews = []

    for ap in app_packages:
        temp, _ = reviews(
            ap,
            sort=Sort.NEWEST,  # defaults to Sort.MOST_RELEVANT
            count=quantity,
        )
        app_reviews.extend(temp)
        if len(app_reviews) >= quantity:
            break

    app_reviews_df = pd.DataFrame(app_reviews)
    app_reviews_df.to_csv('../data/csv/reviews.csv', header=True)

    return app_reviews


def scrape_apps(app_packages, quantity):
    app_infos = []

    for ap in app_packages:
        rvs = app(ap)
        app_infos.append(dict(rvs))
        if len(app_infos) >= quantity:
            break

    app_reviews_df = pd.DataFrame(app_infos)
    app_reviews_df.to_csv('../data/csv/apps.csv', header=True)

    return app_infos
