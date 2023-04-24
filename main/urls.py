from django.conf.urls import url
from main.views.user import User, Login, Register, ChangePassword
from main.views.upload import UploadStudentInfomation, UploadStudentScore
from main.views.task import Task


urlpatterns = [
    url('user', User.as_view()),
    url('task', Task.as_view()),
    url('login', Login.as_view()),
    url('register', Register.as_view()),
    url('changepassword', ChangePassword.as_view()),
    url('uploadstudentinfomation', UploadStudentInfomation.as_view()),
    url('uploadstudentscore', UploadStudentScore.as_view()),
]