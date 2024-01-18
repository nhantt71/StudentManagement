from sqlalchemy.orm import relationship
from smapp import db
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Enum, Date, DateTime, Boolean
from datetime import date
from flask_login import UserMixin
import enum


class UserRoleEnum(enum.Enum):
    TEACHER = 1
    ADMIN = 2
    STAFF = 3


class Gender(enum.Enum):
    MALE = 1
    FEMALE = 2

    def __str__(self):
        return "Nam" if self.name.__eq__("MALE") else "Nữ"


class Reception(enum.Enum):
    IDLE = 1
    ACCEPTED = 2

    def __str__(self):
        return self.name


class LevelOfRegulations(enum.Enum):
    RECEPTION = 1
    STUDENT = 2
    SCHOOL = 3

    def __str__(self):
        return self.name


class MinMaxStuInClass(enum.Enum):
    MIN = 20
    MAX = 40

    def __str__(self):
        return self.name


class ReceptionAge(enum.Enum):
    MIN = 15
    MAX = 20


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dsp3ymism/image/upload/v1704064887/tatutgw6pg2ackzlhht4.png')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.TEACHER)
    teachers = relationship('Teacher', backref='user', lazy=True, uselist=False)

    def __str__(self):
        return self.name


class Regulations(BaseModel):
    level = Column(Enum(LevelOfRegulations))
    content = Column(String(200))

    def __str__(self):
        return self.content


class ClassType(BaseModel):
    class_type_name = Column(String(50), unique=True, nullable=False)
    classes = relationship('Class', backref='classtype', lazy=True)
    reception_students = relationship('ReceptionStudent', backref='classtype', lazy=True)

    def __str__(self):
        return self.class_type_name


class Class(BaseModel):
    class_name = Column(String(50), unique=True, nullable=False)
    number_of_attendants = Column(Integer)
    class_type_id = Column(Integer, ForeignKey(ClassType.id), nullable=False)
    official_students = relationship('OfficialStudent', backref='class', lazy=True)

    def __str__(self):
        return self.class_name


class Person(BaseModel):
    __abstract__ = True

    first_name = Column(String(20), nullable=False)
    last_name = Column(String(50), nullable=False)
    gender = Column(Enum(Gender))
    birth = Column(Date)
    address = Column(String(100))
    phone_number = Column(String(10))
    email = Column(String(50))

    def __str__(self):
        return self.last_name + self.first_name


class ReceptionStudent(Person):
    class_type = Column(Integer, ForeignKey(ClassType.id), nullable=False)
    acceptation = Column(Enum(Reception), nullable=False, default=Reception.IDLE)


class OfficialStudent(Person):
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)
    subjects = relationship('OfficialStudentSubject', backref='officialstudent', lazy=True)


class Year(BaseModel):
    year = Column(String(10), nullable=False)
    semesters = relationship('Semester', backref='year', lazy=True)

    def __str__(self):
        return self.year


class Semester(BaseModel):
    semester_name = Column(String(50), nullable=False)
    year_id = Column(Integer, ForeignKey(Year.id), nullable=False)
    subjects = relationship('Subject', backref='semester', lazy=True)

    def __str__(self):
        return self.semester_name + self.year_id.__str__()


class Score(BaseModel):
    __abstract__ = True

    score = Column(Float, nullable=False)

    def __str__(self):
        return self.score


class Subject(BaseModel):
    subject_name = Column(String(50), nullable=False)
    semester_id = Column(Integer, ForeignKey(Semester.id), nullable=False)
    official_students = relationship('OfficialStudentSubject', backref='subject', lazy=True)

    def __str__(self):
        return self.subject_name


class Teacher(Person):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=False)


class OfficialStudentSubject(BaseModel):
    official_student_id = Column(Integer, ForeignKey(OfficialStudent.id), primary_key=True, nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.id), primary_key=True, nullable=False)
    one_period_tests = relationship('OnePeriodTest', backref='official_student_subject', lazy=True)
    quarter_hour_tests = relationship('QuarterHourTest', backref='official_student_subject', lazy=True)
    semester_tests = relationship('SemesterTest', backref='official_student_subject', lazy=True, uselist=False)


class OnePeriodTest(Score):
    student_subject_id = Column(Integer, ForeignKey(OfficialStudentSubject.id), nullable=False)


class QuarterHourTest(Score):
    student_subject_id = Column(Integer, ForeignKey(OfficialStudentSubject.id), nullable=False)


class SemesterTest(Score):
    student_subject_id = Column(Integer, ForeignKey(OfficialStudentSubject.id), nullable=False)


if __name__ == '__main__':
    from smapp import app

    with app.app_context():


        # rs = ReceptionStudent(birth=date(2003, 12, 5))
        # with open('data/reception_students.json', 'r') as f:
        #     data = json.load(f)
        #
        # for i in data:
        #     acceptation = None
        #     if i['acceptation'] == "IDLE":
        #         acceptation = Reception.IDLE
        #     else:
        #         acceptation = Reception.ACCEPTED
        #     class_type = None
        #     if i['class_type'] == 'K10':
        #         class_type = ClassType.K10
        #     elif i['class_type'] == 'K11':
        #         class_type = ClassType.K11
        #     else:
        #         class_type = ClassType.K12
        #     rs = ReceptionStudent(first_name=i['first_name'], last_name=i['last_name'], gender=i['gender'],
        #                             birth=i['birth'], address=i['address'], phone_number=i['phone_number'],
        #                             email=i['email'], class_type=class_type, acceptation=acceptation)
        #     db.session.add(rs)
        #
        # db.session.commit()

        # db.create_all()
        import hashlib
        # #
        u = User(name='Admin',
                 username='admin',
                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRoleEnum.ADMIN)
        db.session.add(u)
        db.session.commit()

        # c1 = Class(class_name='10A1', class_type=ClassType.K10)
        # c2 = Class(class_name='10A2', class_type=ClassType.K10)
        # c3 = Class(class_name='10A3', class_type=ClassType.K10)
        # c4 = Class(class_name='10A4', class_type=ClassType.K10)
        # c5 = Class(class_name='10A5', class_type=ClassType.K10)
        # c6 = Class(class_name='10A6', class_type=ClassType.K10)
        # c11 = Class(class_name='11B1', class_type=ClassType.K11)
        # c12 = Class(class_name='11B2', class_type=ClassType.K11)
        # c13 = Class(class_name='11B3', class_type=ClassType.K11)
        # c14 = Class(class_name='11B4', class_type=ClassType.K11)
        # c15 = Class(class_name='11B5', class_type=ClassType.K11)
        # c16 = Class(class_name='11B6', class_type=ClassType.K11)
        # c112 = Class(class_name='12C1', class_type=ClassType.K12)
        # c21 = Class(class_name='12C2', class_type=ClassType.K12)
        # c31 = Class(class_name='12C3', class_type=ClassType.K12)
        # c41 = Class(class_name='12C4', class_type=ClassType.K12)
        # c51 = Class(class_name='12C5', class_type=ClassType.K12)
        # c61 = Class(class_name='12C6', class_type=ClassType.K12)
        #
        # db.session.add_all([c1, c2, c3, c4, c5, c6, c11, c12, c13, c14, c15, c16, c112, c21, c31, c41, c51, c61])
        # db.session.commit()






