import random

from smapp.models import *
from smapp import app, db
import hashlib
import cloudinary.uploader
from flask_login import current_user
from sqlalchemy import func, or_


def load_class():
    return Class.query.all()


def load_official_students(kw=None, class_id=None, page=None):
    students = OfficialStudent.query

    if kw:
        students = students.filter(OfficialStudent.first_name.contains(kw)
                                   or OfficialStudent.last_name.contains(kw))

    if class_id:
        students = students.filter(OfficialStudent.class_id.__eq__(class_id))

    if page:
        page = int(page)
        page_size = app.config['PAGE_SIZE']
        start = (page - 1) * page_size
        return students.slice(start, start + page_size)

    return students.all()


def load_reception_students(kw=None, page=None):
    r_students = ReceptionStudent.query

    if kw:
        r_students = r_students.filter(or_(
            ReceptionStudent.first_name.contains(kw),
            ReceptionStudent.last_name.contains(kw)
        ))

    if page:
        page = int(page)
        page_size = app.config['PAGE_SIZE']
        start = (page - 1) * page_size
        return r_students.slice(start, start + page_size)

    return r_students.all()


def count_class_attendants(a_class):
    return Class.query.count()


def get_random_class_by_class_type(class_type):
    r_class = Class.query.filter(Class.class_type.name.__eq__(class_type.name))

    c_class = random.choice(r_class)
    while count_class_attendants(c_class) is MinMaxStuInClass.MAX.value:
        c_class = random.choice(r_class)

    return c_class


def get_reception_student_by_id(id):
    return ReceptionStudent.query.get(id)


def count_reception_students():
    return ReceptionStudent.query.count()


def get_user_by_id(id):
    return User.query.get(id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def get_user_role_by_id(id):
    return get_user_by_id(id).user_role


def change_ages_for_reception():
    pass


def change_numbers_of_attendants():
    pass
