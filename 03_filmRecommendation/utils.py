"""
Authors:
    Damian Brzoskowski (s18499)
    Rafał Sochacki (s20047)

Useful links:
    https://en.wikipedia.org/wiki/Euclidean_distance
    https://en.wikipedia.org/wiki/Taxicab_geometry
    https://www.analyticsvidhya.com/blog/2020/02/4-types-of-distance-metrics-in-machine-learning/
    https://numpy.org/doc/stable/index.html
"""

import numpy as np


def check_user_exist(users, dataset):
    """Checking if user exist on our dataset"""
    for user in users:
        if user not in dataset:
            raise TypeError(f'Cannot find {user} in the dataset')


def scores(dataset, user1, user2):
    """
        euclidean_sore and manhattan_score contains common logic.
        Following the DRY principle, we combined it into 1 function sores
    """
    result = []
    check_user_exist([user1, user2], dataset)
    common_movies = {}

    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1

    # If users have common movies then score is 0
    if len(common_movies) == 0:
        return 0

    for item in dataset[user1]:
        if item in dataset[user2]:
            result.append(np.square(dataset[user1][item] - dataset[user2][item]))

    return result


def euclidean_score(dataset, user1, user2):
    result = scores(dataset, user1, user2)
    return 1 / (1 + np.sqrt(np.sum(result)))


def manhattan_score(dataset, user1, user2):
    result = scores(dataset, user1, user2)
    return np.sum(result)
