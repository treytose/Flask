from . import authBP
from flask import render_template, redirect, url_for, flash, request
from app.auth.forms import LoginForm

@authBP.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): #checks if POST req. and has valid form values
        return 'POST'

    return render_template('auth/login.html', form=form)
