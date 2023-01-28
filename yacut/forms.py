from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL


REQUIRED_FIELD_MESSAGE = 'Обязательное поле'
NOT_URL_MESSAGE = 'Представленное значение не является ссылкой'


class URLmapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(REQUIRED_FIELD_MESSAGE),
            URL(
                require_tld=False,
                message=NOT_URL_MESSAGE
            )
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Создать')
