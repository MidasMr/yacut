from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


NO_JSON_DATA = 'Отсутствует тело запроса'
NO_URL_FIELD_MESSAGE = '"url" является обязательным полем!'
SHORT_ID_NOT_FOUND_MESSAGE = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def add_new_link():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(NO_JSON_DATA)
    if 'url' not in data:
        raise InvalidAPIUsage(NO_URL_FIELD_MESSAGE)
    try:
        urlmap = URLMap.create_from_api(data)
        return jsonify(urlmap.to_dict()), 201
    except ValueError as error:
        raise InvalidAPIUsage(str(error))


@app.route('/api/id/<string:short_id>/')
def get_original_link(short_id):
    urlmap = URLMap.get_urlmap_by_short_link(short_id)
    if not urlmap:
        raise InvalidAPIUsage(SHORT_ID_NOT_FOUND_MESSAGE, 404)
    return jsonify(url=urlmap.original), 200
