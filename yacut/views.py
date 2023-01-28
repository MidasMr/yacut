from random import sample

from flask import abort, flash, redirect, render_template

from . import app, db
from .models import URLMap
from .forms import URLmapForm

URL_SYMBOLS = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789'

CUSTOM_ID_ALREADY_EXISTS_MESSAGE = 'Имя {name} уже занято!'


def get_unique_short_id():
    url = ''.join(sample(URL_SYMBOLS, 6))
    if URLMap.query.filter_by(short=url).first():
        url = get_unique_short_id()
    return url


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLmapForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if not short:
            short = get_unique_short_id()
        if URLMap.query.filter_by(short=short).first():
            flash(CUSTOM_ID_ALREADY_EXISTS_MESSAGE.format(name=short))
            return render_template('index.html', form=form)
        urlmap = URLMap(
            original=form.original_link.data,
            short=short
        )
        db.session.add(urlmap)
        db.session.commit()
        flash(urlmap.short, 'short-link')
    return render_template('index.html', form=form)


@app.route('/<string:url>')
def mapping_view(url):
    urlmap = URLMap.query.filter_by(short=url).first()
    if urlmap is None:
        abort(404)
    return redirect(URLMap.query.filter_by(short=url).first().original), 302
