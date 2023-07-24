from flask import jsonify, make_response

from datetime import datetime as dt
from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import ACTOR_FIELDS  # to make response pretty
from .parse_request import get_request_data


def get_all_actors():
    """
    Get list of all records
    """
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200)


def get_actor_by_id():
    """
    Get record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_actor():
    """
    Add new actor
    """
    data = get_request_data()
    ### YOUR CODE HERE ###

    # Check if all required fields are present
    required_fields = {'name', 'gender', 'date_of_birth'}
    missing_fields = required_fields - set(data.keys())
    if missing_fields:
        err = 'Inputted fields should exist'
        return make_response(jsonify(error=err), 400)

    # Check if inputted fields exist in ACTOR_FIELDS
    for field in data:
        if field not in set(ACTOR_FIELDS):
            err = 'Inputted fields should exist'
            return make_response(jsonify(error=err), 400)

    DATE_FORMAT = '%d.%m.%Y'  # You can extract this from constants if needed

    try:
        dt.strptime(data['date_of_birth'], DATE_FORMAT)
    except:
        err = 'Date of birth should be in format DATE_FORMAT'
        return make_response(jsonify(error=err), 400)
    # use this for 200 response code
    new_record = Actor.create(**data)
    new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(new_actor), 200)
    ### END CODE HERE ###


def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()

    # Check if 'id' is specified and is an integer
    if 'id' not in data:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

    try:
        actor_id = int(data['id'])
    except ValueError:
        err = 'Id must be an integer'
        return make_response(jsonify(error=err), 400)

    # Check if the actor record with the given id exists
    actor = Actor.query.filter_by(id=actor_id).first()
    if not actor:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    # Check if inputted fields exist in ACTOR_FIELDS
    for field in data:
        if field not in ACTOR_FIELDS:
            err = 'Inputted fields should exist'
            return make_response(jsonify(error=err), 400)

    DATE_FORMAT = '%d.%m.%Y'

    if 'date_of_birth' in data.keys():
        try:
            dt.strptime(data.get('date_of_birth'), DATE_FORMAT)
        except:
            err = 'Date of birthday must be in correct format'
            return make_response(jsonify(error=err), 400)

    # update the actor record
    upd_record = Actor.update(actor_id, **data)
    upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(upd_actor), 200)

    ### END CODE HERE ###


def delete_actor():
    """
    Delete actor by id
    """
    data = get_request_data()

    if 'id' not in data:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

    try:
        actor_id = int(data['id'])
    except ValueError:
        err = 'Id must be an integer'
        return make_response(jsonify(error=err), 400)

    # Check if the actor record with the given id exists
    actor = Actor.query.filter_by(id=actor_id).first()
    if not actor:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    # use this for 200 response code
    msg = 'Record successfully deleted'
    return make_response(jsonify(message=msg), 200)
    ### END CODE HERE ###


def actor_add_relation():
    """
    Add a movie to actor's filmography
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
        actor = Actor.add_relation(actor_id, movie)  # add relation here
        rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        rel_actor['filmography'] = str(actor.filmography)
        return make_response(jsonify(rel_actor), 200)
    else:
        err = 'Both id and relation_id should be specified'
        return make_response(jsonify(error=err), 400)


def actor_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###

    # Check if 'id' is specified and is an integer
    if 'id' not in data.keys():
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

    try:
        actor_id = int(data['id'])
    except:
        err = 'Id must be an integer'
        return make_response(jsonify(error=err), 400)

    # obj = Actor.query.get(actor_id)
    # if not obj:
    #     err = 'Record with such id does not exist'
    #     return make_response(jsonify(error=err), 400)

    # Check if the actor record with the given id exists
    obj = Actor.query.filter_by(id=actor_id).first()
    if not obj:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    # use this for 200 response code
    actor = Actor.clear_relations(actor_id)  # clear relations here
    rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
    rel_actor['filmography'] = str(actor.filmography)
    return make_response(jsonify(rel_actor), 200)
    ### END CODE HERE ###
