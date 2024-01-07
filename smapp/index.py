import math
from flask import Flask, render_template, request, redirect, session, jsonify, url_for, flash
from functools import wraps
import utils, dao
from smapp import app, login
from flask_login import login_user, logout_user, current_user


@app.route('/')
def index():
    if current_user.is_authenticated:
        avatar = dao.get_avatar_user_by_id(current_user.id)
        return render_template('index.html', avatar=avatar)

    return render_template('index.html')


# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not session.get("user"):
#             return redirect(url_for('index', next=request.url))
#         return f(*args, **kwargs)
#     return decorated_function


@app.route('/login', methods=['get', 'post'])
def login_user_process():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            next = request.args.get('next')
            return redirect('/' if next is None else next)
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html')


@app.route('/admin/login', methods=['post'])
def login_admin_process():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

    return redirect('/admin')


@app.route('/logout')
def process_logout_user():
    logout_user()
    return redirect('/login')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    from smapp import admin

    app.run(debug=True)
