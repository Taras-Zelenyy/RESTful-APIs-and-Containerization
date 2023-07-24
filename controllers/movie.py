from flask import jsonify, make_response

from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import MOVIE_FIELDS
from .parse_request import get_request_data


def get_all_movies():
    """
    Get list of all records
    """
    all_movie = Movie.query.all()
    movies = []
    for movie in all_movie:
        mov = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(mov)
    return make_response(jsonify(movies), 200)


def get_movie_by_id():
    """
    Get record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be an integer'
            return make_response(jsonify(error=err), 400)

        obj = Movie.query.filter_by(id=row_id).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(movie), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_movie():
    """
    Add new movie
    """
    data = get_request_data()

    required_fields = {'name', 'year', 'genre'}
    missing_fields = required_fields - set(data.keys())
    if missing_fields:
        err = 'Inputted fields should exist'
        return make_response(jsonify(error=err), 400)

    # Check if inputted fields exist in ACTOR_FIELDS
    for field in data:
        if field not in set(MOVIE_FIELDS):
            err = 'Inputted fields should exist'
            return make_response(jsonify(error=err), 400)

    # Check if 'year' is an integer
    if 'year' in data:
        try:
            int(data['year'])
        except:
            err = 'Year should be an integer'
            return make_response(jsonify(error=err), 400)

    new_record = Movie.create(**data)
    new_movie = {k: v for k, v in new_record.__dict__.items() if k in MOVIE_FIELDS}
    return make_response(jsonify(new_movie), 200)


def update_movie():
    """
    Update movie record by id
    """
    data = get_request_data()

    # Check if 'id' is specified and is an integer
    if 'id' not in data.keys():
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

    try:
        movie_id = int(data['id'])
    except:
        err = 'Id must be integer'
        return make_response(jsonify(error=err), 400)

    # Check if the actor record with the given id exists
    obj = Movie.query.filter_by(id=movie_id).first()
    if not obj:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    # Check if inputted fields exist
    for field in data:
        if field != 'id' and field not in set(MOVIE_FIELDS):
            err = 'Inputted fields should exist'
            return make_response(jsonify(error=err), 400)

    # Check if 'year' is an integer
    if 'year' in data:
        try:
            int(data['year'])
        except:
            err = 'Year should be an integer'
            return make_response(jsonify(error=err), 400)

    upd_record = Movie.update(movie_id, **data)
    upd_movie = {k: v for k, v in upd_record.__dict__.items() if k in MOVIE_FIELDS}
    return make_response(jsonify(upd_movie), 200)


def delete_movie():
    """
    Delete movie by id
    """
    data = get_request_data()

    if 'id' not in data:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

    try:
        movie_id = int(data['id'])
    except ValueError:
        err = 'Id must be an integer'
        return make_response(jsonify(error=err), 400)

    # Check if the actor record with the given id exists
    movie = Movie.query.filter_by(id=movie_id).first()
    if not movie:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    # use this for 200 response code
    msg = 'Record successfully deleted'
    return make_response(jsonify(message=msg), 200)


def movie_add_relation():
    """
    Add actor to movie's cast
    """
    data = get_request_data()
    KEY_DICT = {'id', 'relation_id'}

    # Check if all keys in data are correct
    if not set(data.keys()).issubset(KEY_DICT):
        err = 'Wrong key'
        return make_response(jsonify(error=err), 400)

    # Check if 'id' and 'relation_id' are specified and are integers
    if 'id' in data and 'relation_id' in data:
        try:
            actor_id = int(data['id'])
            movie_id = int(data['relation_id'])
        except ValueError:
            err = 'Ids must be integers'
            return make_response(jsonify(error=err), 400)

        # Check if the actor record with the given actor_id exists
        actor = Actor.query.get(actor_id)
        if not actor:
            err = 'Actor with such id does not exist'
            return make_response(jsonify(error=err), 400)

        # Check if the movie record with the given movie_id exists
        movie = Movie.query.get(movie_id)
        if not movie:
            err = 'Movie with such id does not exist'
            return make_response(jsonify(error=err), 400)

        # use this for 200 response code
        movie = Movie.add_relation(movie_id, actor)  # add relation here
        rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        rel_movie['cast'] = str(movie.cast)
        return make_response(jsonify(rel_movie), 200)
    else:
        err = 'Both id and relation_id should be specified'
        return make_response(jsonify(error=err), 400)


def movie_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()

    # Check if 'id' is specified and is an integer
    if 'id' not in data.keys():
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

    try:
        movie_id = int(data['id'])
    except:
        err = 'Id must be integer'
        return make_response(jsonify(error=err), 400)

    # Check if the actor record with the given id exists
    obj = Movie.query.filter_by(id=movie_id).first()
    if not obj:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    # use this for 200 response code
    movie = Movie.clear_relations(movie_id)  # clear relations here
    rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
    rel_movie['cast'] = str(movie.cast)
    return make_response(jsonify(rel_movie), 200)
