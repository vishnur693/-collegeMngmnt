from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name='loginPage'),
    path('adminHome', views.adminHome, name='adminHome'),
    path('signup', views.signupPage, name='signupPage'),
    path('submitSignup', views.submitSignup, name='submitSignup'),
    path('loginBtn', views.loginBtn, name='loginBtn'),
    path('teacherHome', views.teacherHome, name='teacherHome'),
    path('addCourse', views.addCourse, name='addCourse'),
    path('course_db', views.course_db, name='course_db'),
    path('addStudent', views.addStudent, name='addStudent'),
    path('addStudent_db', views.addStudent_db, name='addStudent_db'),
    path('showStudents', views.showStudents, name='showStudents'),
    path('editStudent/<int:student_id>/', views.editStudent, name='editStudent'),
    path('deleteStudent/<int:student_id>/', views.deleteStudent, name='deleteStudent'),
    path('addTeacher', views.addTeacher, name='addTeacher'),
    path('editProfilePage/<int:id>/', views.editProfilePage, name='editProfilePage'),
    path('viewTeacher', views.viewTeacher, name='viewTeacher'),
    path('logout', views.logout_view, name='logout_view'),
    path('deleteTeacher/<int:teacher_id>/', views.deleteTeacher, name='deleteTeacher'),
     path('showTeachers',views.showTeachers,name='showTeachers'),
   

]
