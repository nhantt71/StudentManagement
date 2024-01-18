import math

from flask import render_template, request, redirect
from flask_login import login_user, logout_user, current_user

import dao
from smapp import *


@app.route('/')
def index():
    if current_user.is_authenticated:
        user = dao.get_user_by_id(current_user.id)
        return render_template('index.html', user=user)

    return render_template('index.html')


@app.route('/reception')
def reception():
    if current_user.is_authenticated:
        user = dao.get_user_by_id(current_user.id)
        kw = request.args.get('kw')
        page = request.args.get('page')
        re_students = dao.load_reception_students(kw=kw, page=page)
        total_re_students = dao.count_reception_students()
        return render_template('reception.html', user=user,
                               re_students=re_students,
                               pages=math.ceil(total_re_students/app.config['PAGE_SIZE']))
    return render_template('login.html')


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
            return render_template('login.html', err_msg='Wrong username or password!')
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
    app.run(debug=True)
