from smapp.models import *
from smapp import app
import hashlib


def load_class():
    return Class.query.all()


def load_official_students(kw=None, class_id=None, page=None):
    students = OfficialStudent.query

    if kw:
        students = students.filter(OfficialStudent.first_name.contains(kw) or OfficialStudent.last_name.contains(kw))

    if class_id:
        students = students.filter(OfficialStudent.class_id.__eq__(class_id))

    if page:
        page = int(page)
        page_size = app.config['PAGE_SIZE']
        start = (page - 1) * page_size
        return students.slice(start, start + page_size)

    return students.all()


def get_user_by_id(id):
    return User.query.get(id)


def get_avatar_user_by_id(id):
    return get_user_by_id(id).avatar


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def change_ages_for_reception():
    pass


def change_numbers_of_attendants():
    pass



