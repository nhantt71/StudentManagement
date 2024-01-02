import math
from flask import Flask, render_template, request, redirect, session, jsonify
import dao
import utils
from smapp import app, login
from flask_login import login_user, logout_user, login_required


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['get', 'post'])
@login_required
def login_user_process():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

        next = request.args.get('next')
        return redirect('/' if next is None else next)

    return render_template('login.html')


@app.route('/admin/login', methods=['post'])
@login_required
def login_admin_process():
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

