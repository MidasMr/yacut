from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id, URL_SYMBOLS

NO_JSON_DATA = 'Отсутствует тело запроса'
NO_URL_FIELD_MESSAGE = '"url" является обязательным полем!'
INCORRECT_NAME_FOR_SHORT_LINK_MESSAGE = (
    'Указано недопустимое имя для короткой ссылки'
)
CUSTOM_ID_ALREADY_EXISTS_MESSAGE = 'Имя "{name}" уже занято.'
SHORT_ID_NOT_FOUND_MESSAGE = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def add_new_link():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(NO_JSON_DATA)
    if 'url' not in data:
        raise InvalidAPIUsage(NO_URL_FIELD_MESSAGE)
    cutom_id = data.get('custom_id')
    if cutom_id is None or data['custom_id'] == '':
        data['custom_id'] = get_unique_short_id()
    elif URLMap.query.filter_by(short=cutom_id).first():
        raise InvalidAPIUsage(
            CUSTOM_ID_ALREADY_EXISTS_MESSAGE.format(name=cutom_id)
        )
    elif len(cutom_id) > 16:
        raise InvalidAPIUsage(INCORRECT_NAME_FOR_SHORT_LINK_MESSAGE)
    else:
        for letter in data['custom_id']:
            if letter not in URL_SYMBOLS:
                raise InvalidAPIUsage(INCORRECT_NAME_FOR_SHORT_LINK_MESSAGE)
    urlmap = URLMap()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_dict()), 201


@app.route('/api/id/<string:short_id>/')
def get_original_link(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if not urlmap:
        raise InvalidAPIUsage(SHORT_ID_NOT_FOUND_MESSAGE, 404)
    return jsonify(url=urlmap.original), 200
