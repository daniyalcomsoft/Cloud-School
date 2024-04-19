from email.policy import default
from ftplib import MAXLINE
from operator import truediv
from pyexpat import model
from secrets import choice
from tabnanny import verbose
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    USER = (
        (1,'HOD'),
        (2, 'STAFF'),
        (3, 'STUDENT')
    )
    user_type = models.CharField(choices=USER, max_length=50, default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic')

class Course(models.Model):       
    name = models.CharField(max_length=100, verbose_name="Course Name")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Updated At")

    def __str__(self):
        return self.name

class SchoolSession(models.Model):
    SessionStart = models.DateField(auto_now_add=False, blank=True, null=True, verbose_name="Session Start")
    SessionEnd = models.DateField(auto_now_add=False, blank=True, null=True, verbose_name="Session End")

    def __str__(self):
        return str(self.SessionStart) + ' - ' + str(self.SessionEnd)   

class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField(verbose_name="Address")
    gender = models.CharField(max_length=255, verbose_name="Gender")
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING, verbose_name="Course")
    session_id = models.ForeignKey(SchoolSession, on_delete=models.DO_NOTHING, verbose_name="Session Year")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    update_at = models.DateTimeField(auto_now_add=True, verbose_name="Updated At") 

    def __str__(self):
        return self.admin.first_name + ' ' + self.admin.last_name   

class Staff(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField(verbose_name="Address")
    gender = models.CharField(max_length=100, verbose_name="Gender")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.admin.username 

class Subject(models.Model):
    name = models.CharField(max_length=125, verbose_name="Subject Name")
    course = models.ForeignKey(Course, verbose_name='Course Name', on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, verbose_name='Staff Name', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
    
class StaffNotification(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.staff_id.admin.first_name
    
class StaffLeave(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    message = models.TextField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.staff_id.admin.first_name + self.staff_id.admin.last_name
    
class StaffFeedBack(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.staff_id.admin.first_name + " " + self.staff_id.admin.last_name



class StudentNotification(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_id.admin.first_name


class StudentFeedBack(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_id.admin.first_name + " " + self.student_id.admin.last_name
    

class StudentLeave(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    message = models.TextField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_id.admin.first_name + self.student_id.admin.last_name
    
class Attendance(models.Model):
    subject_id = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    date = models.DateField()
    session_year_id = models.ForeignKey(SchoolSession, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.subject_id.name
    
class AttendanceReport(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.student_id.admin.first_name

class StudentResult(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    subject_id = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    assignment_marks = models.IntegerField()
    exam_marks = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.student_id.admin.first_name