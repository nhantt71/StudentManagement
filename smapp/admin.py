from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from smapp import app, db
from smapp.models import *
from flask_login import logout_user, current_user
from flask import redirect, request

admin = Admin(app=app, name='QUẢN LÝ HỌC SINH', template_mode='bootstrap4')


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class AuthenticatedHideView(ModelView):
    def is_visible(self):
        return False


class MyClassView(AuthenticatedAdmin):
    column_display_pk = True
    form_columns = ['class_name', 'number_of_attendants', 'class_type', 'official_students']
    can_delete = True
    can_edit = True
    can_create = True
    can_view_details = True


class MyOfficialStudentView(AuthenticatedAdmin):
    column_display_pk = True
    column_searchable_list = ['last_name', 'first_name', 'gender']
    can_export = True
    can_view_details = True
    can_edit = True
    can_create = True
    can_delete = True


class MySubjectManagementView(AuthenticatedAdmin):
    column_display_pk = True
    column_list = ['subject_name', 'semester']
    can_delete = True
    can_edit = True
    can_create = True
    column_searchable_list = ['subject_name']
    can_view_details = True


class MyStatsView(AuthenticatedUser):
    @expose("/")
    def index(self):
        return self.render('admin/stats.html')


class MyLogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')


class MyChangeRegulationView(AuthenticatedUser):
    @expose("/")
    def index(self):
        return self.render('admin/regulations.html')


admin.add_view(MyClassView(Class, db.session, name='Danh Sách Lớp'))
admin.add_view(MyOfficialStudentView(OfficialStudent, db.session, name='Danh Sách Học Sinh'))
admin.add_view(MySubjectManagementView(Subject, db.session, name='Quản Lý Môn Học'))
admin.add_view(MyChangeRegulationView(name='Quy định'))
admin.add_view(MyStatsView(name='Thống kê báo cáo'))
admin.add_view(MyLogoutView(name='Đăng xuất'))
