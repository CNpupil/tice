from django.conf.urls import url
from main.views.user import User, Login, Register, ChangePassword, Teacher
from main.views.upload import UploadStudentInfomation, UploadStudentScore
from main.views.task import Task, TaskList, DistributeTeacher, TaskByTeacher, StudentFromTaskByTeacher, TaskProgress
from main.views.score import ScoreStandard, ScoreOnStudent, ScoreStatics, ScoreOnSearch, ClassInfomation


urlpatterns = [
    url('user', User.as_view()),
    # task
    url(r'^tasklist$', TaskList.as_view()),
    url(r'^task$', Task.as_view()),
    url(r'^uploadstudentinfomation$', UploadStudentInfomation.as_view()),
    url(r'^distributeteacher$', DistributeTeacher.as_view()),
    url(r'^uploadstudentscore$', UploadStudentScore.as_view()),
    url(r'^scorestandard$', ScoreStandard.as_view()),
    url(r'^taskprogress$', TaskProgress.as_view()),
    url(r'^scorestatics$', ScoreStatics.as_view()),
    url(r'^scoresearch$', ScoreOnSearch.as_view()),
    url(r'^classinfomation$', ClassInfomation.as_view()),
    # user
    url(r'^teacher$', Teacher.as_view()),
    url(r'^login$', Login.as_view()),
    url(r'^register$', Register.as_view()),
    url(r'^changepassword$', ChangePassword.as_view()),
    # teacher
    url(r'^taskbyteacher$', TaskByTeacher.as_view()),
    url(r'^studentfromtaskbyteacher$', StudentFromTaskByTeacher.as_view()),
    # student
    url(r'^scoreonstudent$', ScoreOnStudent.as_view()),
]