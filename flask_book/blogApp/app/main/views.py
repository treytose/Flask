from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User, Permission
from flask_login import login_required
from app.decorators import admin_required, permission_required

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
@admin_required
def secret():
    return 'Secret template!'


@main.route('/secret2')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def secret2():
    return 'Secret 2 template!'


@main.route('/secret3')
@login_required
@permission_required(Permission.FOLLOW)
def secret3():
    return 'Secret 3 template!'


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    #we pass in the 'user' object here because other people may be viewing other peoples profiles so user != current_user
    return render_template('user.html', user=user)
