from flask import abort, flash, redirect, render_template

from . import app
from .forms import URLmapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLmapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short = form.custom_id.data

    try:
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


@app.route('/<string:url>')
def mapping_view(url):
    urlmap = URLMap.get_by_short_link(url)
    if urlmap is None:
        abort(404)
    return redirect(urlmap.original), 302
