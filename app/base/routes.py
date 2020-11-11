# -*- encoding: utf-8 -*-
from flask import jsonify, render_template, redirect, request, url_for
from flask_login import (current_user, login_required, login_user, logout_user)
from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm
from app.models import User
from app.base.util import verify_pass


@blueprint.route('/')
def route_default():
  return redirect(url_for('base_blueprint.login'))


## Login
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
  login_form = LoginForm(request.form)
  if 'login' in request.form:
    # read form data
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    
    # Check the password
    if user and verify_pass(password, user.password):
        login_user(user)
        return redirect(url_for('base_blueprint.route_default'))

    # Something (user or pass) is not ok
    return render_template( 'accounts/login.html', msg='Wrong user or password', form=login_form)

  if not current_user.is_authenticated:
    return render_template('accounts/login.html', form=login_form)

  return redirect(url_for('home_blueprint.index'))
    

## Register user
@blueprint.route('/register', methods=['GET', 'POST'])
def register():
  login_form = LoginForm(request.form)
  create_account_form = CreateAccountForm(request.form)
  if 'register' in request.form:
    username = request.form['username']
    email = request.form['email']

    # Check usename exists
    user = User.query.filter_by(username=username).first()
    if user:
      return render_template('accounts/register.html', 
                              msg='Username already registered',
                              success=False,
                              form=create_account_form)

    # Check email exists
    user = User.query.filter_by(email=email).first()
    if user:
      return render_template('accounts/register.html', 
                              msg='Email already registered', 
                              success=False,
                              form=create_account_form)

    # else we can create the user
    user = User(**request.form)

    return render_template('accounts/register.html', 
                            msg='User created please <a href="/login">login</a>', 
                            success=True,
                            form=create_account_form)

  # GET route
  else:
    return render_template('accounts/register.html', form=create_account_form)


## TODO forgot password
@blueprint.route('/reset', methods=['GET', 'POST'])
def reset():
  pass


# Logout user
@blueprint.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('base_blueprint.login'))


@blueprint.route('/shutdown')
def shutdown():
  func = request.environ.get('werkzeug.server.shutdown')
  if func is None:
      raise RuntimeError('Not running with the Werkzeug Server')
  func()
  return 'Server shutting down...'


## Errors
@login_manager.unauthorized_handler
def unauthorized_handler():
  return render_template('page-403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
  return render_template('page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
  return render_template('page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
  return render_template('page-500.html'), 500
