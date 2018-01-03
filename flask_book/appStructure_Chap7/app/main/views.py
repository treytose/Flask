from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from flask_login import login_required

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('.index')) #.index is for referring to within the same blueprint, to refer outside of the BP use <package>.index
    return render_template('index.html', form =form, name=session.get('name'), #e.g. here .index is the same as: main.index
                            known=session.get('known', False),
                            current_time=datetime.utcnow())


@main.route('/secret')
@login_required
def secret():
    return 'Secret template!'
