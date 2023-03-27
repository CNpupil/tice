from django.conf.urls import url
from main.views.user import User, Login


urlpatterns = [
    url('user', User.User.as_view()),
    url('login', Login.Login.as_view()),
]