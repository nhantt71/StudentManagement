from sqlalchemy.orm import relationship
from smapp import db
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Enum, DateTime, Boolean, select, column
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import enum


class UserRoleEnum(enum.Enum):
    TEACHER = 1
    ADMIN = 2


class Gender(enum.Enum):
    MALE = 1
    FEMALE = 2


class Reception(enum.Enum):
    IDLE = 1
    ACCEPTED = 2


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
    class_type_name = Column(String(50), unique=True, nullable=False)
    classes = relationship('Class', backref='classtype', lazy=True)

    def __str__(self):
        return self.class_type_name


class Class(BaseModel):
    class_name = Column(String(50), nullable=False)
    maximum_number_of_attendants = Column(Integer, default=40)
    class_type_id = Column(Integer, ForeignKey(ClassType.id), nullable=False)
    official_students = relationship('OfficialStudent', backref='class', lazy=True)

    def __str__(self):
        return self.className


class Student(BaseModel):
    __abstract__ = True

    first_name = Column(String(20), nullable=False)
    last_name = Column(String(50), nullable=False)
    gender = Column(Enum(Gender))
    birth = Column(String(10))
    address = Column(String(100))
    phone_number = Column(String(10))
    email = Column(String(50))

    def __str__(self):
        return self.last_name + self.first_name


class ReceptionStudent(Student):
    acceptation = Column(Enum(Reception), nullable=False, default=Reception.IDLE)


class OfficialStudent(Student):
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)
    subjects = relationship('StudentSubject', backref='official_student', lazy=True)


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
    official_students = relationship('StudentSubject', backref='subject', lazy=True)

    def __str__(self):
        return self.subject_name


class StudentSubject(BaseModel):
    student_id = Column(Integer, ForeignKey(OfficialStudent.id), primary_key=True, nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.id), primary_key=True, nullable=False)
    one_period_tests = relationship('OnePeriodTest', backref='student_subject', lazy=True)
    quarter_hour_tests = relationship('QuarterHourTest', backref='student_subject', lazy=True)
    semester_tests = relationship('SemesterTest', backref='student_subject', lazy=True, uselist=False)


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

        import hashlib
        u1 = User(name='Admin',
                 username='admin',
                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRoleEnum.ADMIN)

        db.session.add(u1)
        db.session.commit()
        #
        # u2 = User(name='Teacher1',
        #          username='teacher',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.TEACHER)
        #
        # db.session.add_all([u1, u2])
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
        #
        # ct1 = ClassType(class_type_name="Khối 10")
        # ct2 = ClassType(class_type_name="Khối 11")
        # ct3 = ClassType(class_type_name="Khối 12")
        #
        # db.session.add_all([ct1, ct2, ct3])
        #
        # c1 = Class(class_name='10A1', class_type_id=1)
        # c2 = Class(class_name='10A2', class_type_id=1)
        # c3 = Class(class_name='10A3', class_type_id=1)
        # c4 = Class(class_name='10A4', class_type_id=1)
        # c5 = Class(class_name='10A5', class_type_id=1)
        # c6 = Class(class_name='10A6', class_type_id=1)
        #
        # c11 = Class(class_name='11B1', class_type_id=2)
        # c21 = Class(class_name='11B2', class_type_id=2)
        # c31 = Class(class_name='11B3', class_type_id=2)
        # c41 = Class(class_name='11B4', class_type_id=2)
        # c51 = Class(class_name='11B5', class_type_id=2)
        # c61 = Class(class_name='11B6', class_type_id=2)
        #
        # c12 = Class(class_name='12C1', class_type_id=3)
        # c22 = Class(class_name='12C2', class_type_id=3)
        # c32 = Class(class_name='12C3', class_type_id=3)
        # c42 = Class(class_name='12C4', class_type_id=3)
        # c52 = Class(class_name='12C5', class_type_id=3)
        # c62 = Class(class_name='12C6', class_type_id=3)
        #
        # db.session.add_all([c1, c2, c3, c4, c5, c6, c11, c21, c31, c41, c51, c61, c12, c22, c32, c42, c52, c62])
        #
        # db.session.commit()


