"""SchoolProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from telnetlib import STATUS
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views, Hod_views, Staff_views, Student_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),

    # Login Path 
    path('', views.LOGIN, name='login'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('doLogout', views.doLogout, name='logout'),  

    path('hod/Home', Hod_views.HOME, name='hod_home'),

    path('profile', views.PROFILE, name='profile'),
    path('profile/update', views.PROFILE_UPDATE, name='profile_update'),

    path('hod/student/add', Hod_views.ADD_STUDENT, name='add_student'),
    path('hod/student/view', Hod_views.VIEW_STUDENT, name="view_student"),
    path('hod/student/edit/<str:id>', Hod_views.EDIT_STUDENT, name="edit_student"),
    path('hod/student/update/', Hod_views.UPDATE_STUDENT, name="update_student"),
    path('hod/student/delete/<str:admin>', Hod_views.DELETE_STUDENT, name='delete_student'),

    path('hod/course/add', Hod_views.Add_Course, name="add_course"),
    path('hod/course/view', Hod_views.View_Course, name="view_course"),
    path('hod/course/edit/<str:id>', Hod_views.Edit_Course, name='edit_course'),
    path('hod/course/update/', Hod_views.Update_Course, name='update_course'),
    path('ho/course/delete/<str:id>', Hod_views.Delete_Course, name='delete_course'),

    path('hod/staff/add', Hod_views.Add_Staff, name="add_staff"),
    path('hod/staff/view', Hod_views.View_Staff, name="view_staff"),
    path('hod/staff/edit/<str:id>', Hod_views.Edit_Staff, name="edit_staff"),
    path('hod/staff/update/', Hod_views.Update_Staff, name="update_staff"),
    path('hod/staff/delete/<str:id>', Hod_views.Delete_Staff, name="delete_staff"),

    path('hod/subject/add', Hod_views.Add_Subject, name='add_subject'),
    path('hod/subject/view', Hod_views.View_Subject, name='view_subject'),
    path('hod/subject/edit/<str:id>', Hod_views.Edit_Subject, name='edit_subject'),
    path('hod/subject/update/', Hod_views.Update_Subject, name='update_subject'),
    path('hod/subject/delete/<str:id>', Hod_views.Delete_Subject, name="delete_subject"),

    path('hod/session/add', Hod_views.Add_Session, name='add_session'),
    path('view/session', Hod_views.View_Session, name='view_session'),
    path('edit/session/<str:id>', Hod_views.Edit_Session, name='edit_session'),
    path('update/session/', Hod_views.Update_Session, name='update_session'),
    path('delete/session/<str:id>', Hod_views.Delete_Session, name='delete_session'),

    path('hod/Staff/Send_Notification', Hod_views.SendStaffNotification, name='send_Staff_notification'),
    path('hod/Staff/save_notification', Hod_views.SaveStaffNotification, name='save_Staff_notification'),

    path('hod/Staff/leave_view', Hod_views.StaffLeaveView, name='staff_leave_view'),
    path('hod/Staff/approve_leave/<str:id>', Hod_views.ApproveLeave, name='approve_leave'),
    path('hod/Staff/disapprove_leave/<str:id>', Hod_views.DisApproveLeave, name='disapprove_leave'),

    path('hod/Student/leave_view', Hod_views.StudentLeaveView, name='stdleave_view'),
    path('hod/Student/approve_leave/<str:id>', Hod_views.StudentApproveLeave, name='stdapprove_leave'),
    path('hod/Student/disapprove_leave/<str:id>', Hod_views.StudentDisApproveLeave, name='stddisapprove_leave'),



    path('hod/Staff/feedback', Hod_views.Staff_Feedback, name='stafffeedback'),
    path('hod/Staff/feedback/save', Hod_views.Staff_FeedbackSave, name='stafffeedback_save'),

    path('hod/Student/feedback', Hod_views.Student_Feedback, name='studentfeedback'),
    path('hod/Student/feedback/save', Hod_views.Student_FeedbackSave, name='stdfeedback_save'),
    path('hod/view/attendance', Hod_views.ViewAttendance, name='view_attendance'),


    path('staff/home', Staff_views.Home, name='staff_home'),
    path('staff/Notifications', Staff_views.Staff_Notification, name='staff_notification'),
    path('staff/mark_as_done/<str:status>', Staff_views.MarkAsDone, name='mark_as_done'),
    path('staff/apply_leave', Staff_views.ApplyLeave, name='apply_leave'),
    path('staff/apply_leave_save', Staff_views.ApplyLeaveSave, name='apply_leave_save'),
    path('staff/feedback', Staff_views.StaffFeedback, name='staff_feedback'),
    path('staff/feedback/save', Staff_views.StaffFeedbackSave, name='staff_feedback_save'),
    path('staff/take/attendance', Staff_views.StaffTakeAttendance, name='staff_take_attnd'),
    path('staff/save/attendance', Staff_views.StaffSaveAttendance, name='staff_save_attnd'),
    path('staff/view/attendance', Staff_views.StaffViewAttendance, name='staff_view_attnd'),
    path('staff/add/result', Staff_views.AddResult, name='add_result'),
    path('staff/save/result', Staff_views.SaveResult, name='save_result'),

    # urls for student 

    path('student/home', Student_views.Home, name='student_home'),

    path('hod/Student/Send_Notification', Hod_views.SendStudentNotification, name='send_Std_notification'),
    path('hod/Student/save_notification', Hod_views.SaveStudentNotification, name='save_Std_notification'),

    path('student/Notifications', Student_views.Student_Notification, name='student_notification'),
    path('student/mark_as_donestd/<str:status>', Student_views.MarkAsDoneStd, name='mark_as_donestd'),

    path('student/feedback', Student_views.StdFeedback, name='std_feedback'),
    path('student/feedback/save', Student_views.StdFeedbackSave, name='std_feedback_save'),

    path('Student/applyleave', Student_views.StudentLeaves, name='stdapply_leave'),
    path('Student/leave/save', Student_views.StudentLeaveSave, name='std_leave_save'),
    path('Student/view/attendance', Student_views.StudentViewAttendance, name='std_view_attnd'),
    path('Student/view/result', Student_views.ViewResult, name='view_result'),



] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
