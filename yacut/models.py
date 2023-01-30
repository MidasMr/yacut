from datetime import datetime
from random import sample
import re

from flask import url_for

from . import db
from settings import (
    URL_SYMBOLS, SHORT_LINK_ATTEMPS, SHORT_LINK_LENGTH,
    SHORT_LINK_PATTERN, USER_SHORT_LINK_LENGTH
)

API_CUSTOM_ID_ALREADY_EXISTS_MESSAGE = 'Имя "{name}" уже занято.'
CUSTOM_ID_ALREADY_EXISTS_MESSAGE = 'Имя {name} уже занято!'
INCORRECT_NAME_FOR_SHORT_LINK_MESSAGE = (
    'Указано недопустимое имя для короткой ссылки'
)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String, nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('mapping_view', url=self.short, _external=True)
        )

    @staticmethod
    def create_from_api(data):
        short = data.get('custom_id')
        short = URLMap.get_unique_short_id() if not short else short
        if URLMap.get_urlmap_by_short_link(short):
            raise ValueError(
                API_CUSTOM_ID_ALREADY_EXISTS_MESSAGE.format(name=short)
            )
        if not re.fullmatch(SHORT_LINK_PATTERN, short):
            raise ValueError(INCORRECT_NAME_FOR_SHORT_LINK_MESSAGE)
        if len(short) > USER_SHORT_LINK_LENGTH:
            raise ValueError(INCORRECT_NAME_FOR_SHORT_LINK_MESSAGE)
        return URLMap.create_urlmap(original=data['url'], short=short)

    @staticmethod
    def get_urlmap_by_short_link(short_link):
        return URLMap.query.filter_by(short=short_link).first()

    @staticmethod
    def get_unique_short_id():
        for _ in range(SHORT_LINK_ATTEMPS):
            url = ''.join(sample(URL_SYMBOLS, SHORT_LINK_LENGTH))
            if URLMap.get_urlmap_by_short_link(url):
                continue
            return url

    @staticmethod
    def create_urlmap(original, short=None):
        short = URLMap.get_unique_short_id() if not short else short
        if URLMap.get_urlmap_by_short_link(short):
            raise ValueError(
                CUSTOM_ID_ALREADY_EXISTS_MESSAGE.format(name=short)
            )
        urlmap = URLMap(
            original=original,
            short=short
        )
        db.session.add(urlmap)
        db.session.commit()
        return urlmap
