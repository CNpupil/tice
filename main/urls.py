from django.conf.urls import url
from main.views.User import User, Login, Register, ChangePassword
from main.views.UploadData import UploadStudentInfomation


urlpatterns = [
    url('user', User.as_view()),
    url('login', Login.as_view()),
    url('register', Register.as_view()),
    url('changepassword', ChangePassword.as_view()),
    url('uploadStudentInfomation', UploadStudentInfomation.as_view()),
]