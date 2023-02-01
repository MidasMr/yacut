from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from settings import USER_SHORT_LINK_LENGTH, SHORT_LINK_PATTERN, MAX_URL_LENGTH

CUSTOM_ID_PLACEHOLDER = 'Ваш вариант короткой ссылки'
ORIGINAL_LINK_PLACEHOLDER = 'Длинная ссылка'
SUBMIT_BUTTON_PHRASE = 'Создать'

REQUIRED_FIELD_MESSAGE = 'Обязательное поле'
NOT_URL_MESSAGE = 'Представленное значение не является ссылкой'


class URLmapForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_PLACEHOLDER,
        validators=[
            Length(max=MAX_URL_LENGTH),
            DataRequired(REQUIRED_FIELD_MESSAGE),
            URL(
                require_tld=False,
                message=NOT_URL_MESSAGE
            )
        ]
    )
    custom_id = StringField(
        CUSTOM_ID_PLACEHOLDER,
        validators=[
            Length(max=USER_SHORT_LINK_LENGTH),
            Optional(),
            Regexp(SHORT_LINK_PATTERN)
        ]
    )
    submit = SubmitField(SUBMIT_BUTTON_PHRASE)
