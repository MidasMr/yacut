from datetime import datetime
from random import sample

from flask import url_for

from . import db
from settings import (
    SHORT_LINK_SYMBOLS, SHORT_LINK_ATTEMPS, SHORT_LINK_LENGTH
)

CUSTOM_ID_ALREADY_EXISTS_MESSAGE = 'Имя {name} уже занято!'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(
        db.String(length=SHORT_LINK_LENGTH),
        nullable=False,
        unique=True
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('mapping_view', url=self.short, _external=True)
        )

    @staticmethod
    def validate_short(short):
        if URLMap.get_by_short_link(short):
            raise ValueError(
                CUSTOM_ID_ALREADY_EXISTS_MESSAGE.format(name=short)
            )
        return short

    @staticmethod
    def get_by_short_link(short_link):
        return URLMap.query.filter_by(short=short_link).first()

    @staticmethod
    def get_unique_short_id():
        for _ in range(SHORT_LINK_ATTEMPS):
            url = ''.join(sample(SHORT_LINK_SYMBOLS, SHORT_LINK_LENGTH))
            if URLMap.get_by_short_link(url):
                continue
            return url
        return URLMap.get_unique_short_id()

    @staticmethod
    def create(original, short=None):
        short = URLMap.get_unique_short_id() if (
            not short
        ) else URLMap.validate_short(short)
        urlmap = URLMap(
            original=original,
            short=short
        )
        db.session.add(urlmap)
        db.session.commit()
        return urlmap
