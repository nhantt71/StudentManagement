from datetime import date

import dao
import models


def check_admission_condition(r_student_id):
    r_student = dao.get_reception_student_by_id(r_student_id)

    age = date.today().year - r_student.birth.year if (
            (date.today().month, date.today().day) < (r_student.birth.month, r_student.birth.day)
    ) else (date.today().year - r_student.birth.year) - 1

    if age < models.ReceptionAge.MIN.value or age > models.ReceptionAge.MAX.value:
        return False

    r_class = dao.get_random_class_by_class_type(r_student.class_type)
    if r_class is None:
        return False

    return True
