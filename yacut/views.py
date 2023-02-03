from flask import abort, flash, redirect, render_template

from . import app
from .forms import URLmapForm
from .models import URLMap

CUSTOM_ID_ALREADY_EXISTS_MESSAGE = 'Имя {name} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLmapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short = form.custom_id.data

    try:
        if short:
            if not URLMap.short_link_is_free(short):
                flash(CUSTOM_ID_ALREADY_EXISTS_MESSAGE.format(name=short))
                return render_template('index.html', form=form)
        urlmap = URLMap.create(
            original=form.original_link.data,
            short=short
        )
        return render_template(
            'index.html',
            form=form,
            short_link=urlmap.short
        )
    except ValueError as error:
        flash(error)
        return render_template('index.html', form=form)


@app.route('/<string:short_link>')
def mapping_view(short_link):
    urlmap = URLMap.get_by_short_link(short_link)
    if urlmap is None:
        abort(404)
    return redirect(urlmap.original), 302
