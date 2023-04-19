from django.conf.urls import url
from main.views.user import User, Login, Register, ChangePassword
from main.views.upload import UploadStudentInfomation


urlpatterns = [
    url('user', User.as_view()),
    url('login', Login.as_view()),
    url('register', Register.as_view()),
    url('changepassword', ChangePassword.as_view()),
    url('uploadStudentInfomation', UploadStudentInfomation.as_view()),
]