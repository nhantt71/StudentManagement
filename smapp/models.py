from sqlalchemy.orm import relationship
from smapp import db
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Enum, DateTime, Boolean
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import enum


class UserRoleEnum(enum.Enum):
    TEACHER = 1
    ADMIN = 2


class Gender(enum.Enum):
    MALE = 1
    FEMALE = 2


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

    def __str__(self):
        return self.name


class ClassType(BaseModel):
    class_type_name = Column(String(50), nullable=False)
    classes = relationship('Class', backref='classtype', lazy=True)

    def __str__(self):
        return self.class_type_name


class Class(BaseModel):
    class_name = Column(String(50), nullable=False)
    number_of_attendants = Column(Integer)
    class_type_id = Column(Integer, ForeignKey(ClassType.id), nullable=False)
    students = relationship('Student', backref='class', lazy=True)

    def __str__(self):
        return self.className


class Student(BaseModel):
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(50), nullable=False)
    gender = Column(Enum(Gender))
    birth = Column(String(10))
    address = Column(String(100))
    phone_number = Column(String(10))
    email = Column(String(50))
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)
    subjects = relationship('StudentSubject', backref='student')

    def __str__(self):
        return self.last_name + self.first_name


class Year(BaseModel):
    year = Column(String(10), nullable=False)
    semesters = relationship('Semester', backref='year', lazy=True)

    def __str__(self):
        return self.year


class Semester(BaseModel):
    semester = Column(String(50), nullable=False)
    year_id = Column(Integer, ForeignKey(Year.id), nullable=False)
    subjects = relationship('Subject', backref='semester', lazy=True)

    def __str__(self):
        return self.semester


class Score(BaseModel):
    __abstract__ = True

    score = Column(Float, nullable=False)

    def __str__(self):
        return self.score


class Subject(BaseModel):
    subject_name = Column(String(50), nullable=False)
    semester_id = Column(Integer, ForeignKey(Semester.id), nullable=False)
    students = relationship('StudentSubject', backref='subject')

    def __str__(self):
        return self.subject_name


class StudentSubject(BaseModel):
    student_id = Column(Integer, ForeignKey(Student.id), primary_key=True, nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.id), primary_key=True, nullable=False)
    one_period_tests = relationship('OnePeriodTest', backref='studentsubject', lazy=True)
    quarter_hour_tests = relationship('QuarterHourTest', backref='studentsubject', lazy=True)
    semester_tests = relationship('SemesterTest', backref='studentsubject', lazy=True)


class OnePeriodTest(Score):
    student_subject_id = Column(Integer, ForeignKey(StudentSubject.id), nullable=False)


class QuarterHourTest(Score):
    student_subject_id = Column(Integer, ForeignKey(StudentSubject.id), nullable=False)


class SemesterTest(Score):
    student_subject_id = Column(Integer, ForeignKey(StudentSubject.id), nullable=False)


if __name__ == '__main__':
    from smapp import app
    with app.app_context():
        # db.create_all()

        # import hashlib
        # u1 = User(name='Admin',
        #          username='admin',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.ADMIN)
        #
        # u2 = User(name='Teacher1',
        #          username='teacher',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.TEACHER)
        #

        # y1 = Year(year='2023-2024')
        # y2 = Year(year='2024-2025')
        #
        # s1 = Semester(semester='Học Kỳ 1', year_id=1)
        # s2 = Semester(semester='Học Kỳ 1', year_id=2)
        # s3 = Semester(semester='Học Kỳ 2', year_id=1)
        # s4 = Semester(semester='Học Kỳ 2', year_id=2)
        #
        # sub1 = Subject(subject_name='Hóa Học', semester_id=1)
        # sub2 = Subject(subject_name='Hóa Học', semester_id=2)
        # sub3 = Subject(subject_name='Vật Lý', semester_id=3)
        # sub4 = Subject(subject_name='Ngữ Văn', semester_id=4)
        # sub5 = Subject(subject_name='Ngữ Văn', semester_id=1)
        #
        # db.session.add_all([y1, y2])
        # db.session.add_all([s1, s2, s3, s4])
        # db.session.add_all([sub1, sub2, sub3, sub4, sub5])
        db.session.commit()


