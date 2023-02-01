from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

CUSTOM_ID_ALREADY_EXISTS_MESSAGE = 'Имя "{name}" уже занято.'
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
    short = data.get('custom_id')
    if short:
        try:
            URLMap.short_link_is_free(short)
        except ValueError:
            raise InvalidAPIUsage(
                CUSTOM_ID_ALREADY_EXISTS_MESSAGE.format(name=short)
            )
    try:
        urlmap = URLMap.create(
            original=data['url'],
            short=short,
            validate=True
        )
        return jsonify(urlmap.to_dict()), 201
    except ValueError as error:
        raise InvalidAPIUsage(str(error))


@app.route('/api/id/<string:short_id>/')
def get_original_link(short_id):
    urlmap = URLMap.get_by_short_link(short_id)
    if not urlmap:
        raise InvalidAPIUsage(SHORT_ID_NOT_FOUND_MESSAGE, 404)
    return jsonify(url=urlmap.original), 200
