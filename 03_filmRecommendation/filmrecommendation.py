"""
Authors:
    Damian Brzoskowski (s18499)
    Rafał Sochacki (s20047)

Description:
    Example usage:
        euclidean_score:
            python filmrecommendation.py --user "Damian Brzoskowski" --json "user_data.json" --metric 'es'
        manhattan_score
            python filmrecommendation.py --user "Damian Brzoskowski" --json "user_data.json" --metric 'mh'

        --json it's not required

    1. Install:
        pip install numpy
        pip install imdbpy
    2. Docs:
        Numpy: https://numpy.org/doc/
        imbd: https://imdb-api.com/api
    3. Helps:
        Imbd: https://github.com/alberanid/imdbpy
"""

import argparse
import json
import imdb
import numpy as np

from utils import euclidean_score
from utils import manhattan_score


def build_arg_parser():
    parser = argparse.ArgumentParser(description='Find users who are similar to the input user')
    parser.add_argument('--user', dest="user", required=True,
                        help='Input user')
    parser.add_argument('--json', dest="json", required=False,
                        help='Add path to json file')
    parser.add_argument('--metric', dest="metric", required=True,
                        help="'es' = euclidean_score | 'mh' = manhattan_score")
    return parser


def find_similar_users_by_movie_taste(dataset, user, num_users, metic):
    """
        Find similar users.
            Parameters:
                dataset (dict): File with data, json format
                user (str): User to compare
                num_users (int): Number of users
                metic (str): 'mh or 'es'

            Return:
                scores (dict): Return similar users

    """
    if user not in dataset:
        raise TypeError(f'Cannot find {user} in the dataset')

    if metic == 'es':
        scores = np.array([[x, euclidean_score(dataset, user, x)] for x in dataset if x != user])
    elif metic == 'mh':
        scores = np.array([[x, manhattan_score(dataset, user, x)] for x in dataset if x != user])
    else:
        raise TypeError(f'Incorrect metric {metic}')

    scores_sorted = np.argsort(scores[:, 1])[::-1]

    top_users = scores_sorted[:num_users]

    return scores[top_users]


def movies_details(recommendations):
    print("MOVIES: \n")
    for i in recommendations:
        print(f"Movie title: {i}")
        movies = imbd_api.search_movie(i)
        movie = imbd_api.get_movie(movies[0].movieID)

        if movie.get('plot'):
            print(f"- Description: {' '.join(movie.get('plot'))}")
        else:
            print("- Description: ")
        print(f"- Year: {movie.get('year')}")
        print(f"- Rating: {movie.get('rating')}")
        print(f"- Votes: {movie.get('votes')}")
        if movie.get('box office'):
            print(f"- Box office: {movie.get('box office').get('Budget')}")
        else:
            print("- Box office: ")
        # list comprehension to print Directors
        if movie.get('directors'):
            [print(f"- Director: {director.get('name')}") for director in movie.get('directors')]
        else:
            print("- Director: ")
        print('-' * 30)  # separator

    not_recommended_movies = list(reversed(diff_between_users.keys()))[:5]
    print(f"{'*' * 30} NOT RECOMMENDED MOVIES {'*' * 30}")  # separator
    [print(f"- {j}") for j in not_recommended_movies]
    print(f"{'*' * 30}{'*' * len(' NOT RECOMMENDED MOVIES ')}{'*' * 30}")  # separator


if __name__ == '__main__':
    args = build_arg_parser().parse_args()
    user = args.user
    # Get data from default file
    json_file = args.json if args.json else "user_data.json"
    metric = args.metric

    metric = metric.lower()
    if metric not in ['es', 'mh']:
        raise TypeError(f'Cannot find metric {metric}')

    # IMDB API Connection
    imbd_api = imdb.IMDb()

    with open(json_file, 'r', encoding="UTF-8") as f:
        data = json.loads(f.read())
    similar_users = find_similar_users_by_movie_taste(data, user, 16, metric)

    top_maches = data[similar_users[0][0]]
    user_movies = data[user]
    diff_between_users = {}

    for key in top_maches.keys():
        if key not in user_movies.keys():
            diff_between_users[key] = top_maches[key]

    diff_between_users = {
        k: v for k, v in sorted(diff_between_users.items(), key=lambda x: x[1], reverse=True)
    }

    print(f"User `{user}` RESULTS: ")
    recommended_movies = list(diff_between_users.keys())[:5]
    movies_details(recommended_movies)
