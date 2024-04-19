from django.shortcuts import render, redirect
from SchoolApp.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def Home(request):
    return render(request, 'Student/home.html')

def Student_Notification(request):
    student = Student.objects.filter(admin=request.user.id)
    for i in student:
        student_id = i.id 
        notification = StudentNotification.objects.filter(student_id = student_id)
        context = {
            'notification': notification
        }
        return render(request, 'Student/notification.html', context)
    
@login_required(login_url='/')    
def MarkAsDoneStd(request, status):
    notification = StudentNotification.objects.get(id=status)
    notification.status = 1
    notification.save()
    return redirect('student_notification')

@login_required(login_url='/')
def StdFeedback(request):
    student_id = Student.objects.get(admin=request.user.id)
    feedback_history = StudentFeedBack.objects.filter(student_id = student_id)
    context = {
        'feedback_history': feedback_history
    }
    return render(request, 'Student/stdfeedback.html', context)

@login_required(login_url='/')
def StdFeedbackSave(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback')
        student = Student.objects.get(admin = request.user.id)
        feedbacks = StudentFeedBack(
            student_id = student,
            feedback = feedback,
            feedback_reply = "",
        )
        feedbacks.save()
        messages.success(request, 'Feedback Sent Successfully')
        return redirect('std_feedback')

# @login_required(login_url='/')
# def StudentLeaves(request):
#     student = Student.objects.filter(admin=request.user.id)
#     for i in student:
#         student_id = i.id
#         stdleavehistory = StudentLeave.objects.filter(student_id=student_id)
#         context = {
#             'stdleavehistory':stdleavehistory
#         }
#     return render(request, 'Student/applyleave.html', context)

@login_required(login_url='/')
def StudentLeaves(request):
    student = Student.objects.get(admin=request.user.id)
    stdleavehistory = StudentLeave.objects.filter(student_id = student)
    context = {
        'stdleavehistory':stdleavehistory
    }
    return render(request, 'Student/applyleave.html', context)


@login_required(login_url='/')
def StudentLeaveSave(request):
    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        student = Student.objects.get(admin = request.user.id)

        leave = StudentLeave(
            student_id = student,
            date = leave_date,
            message = leave_message
        )
        leave.save()
        messages.success(request, 'Message Sent Successfully')
        return redirect('stdapply_leave')

def StudentViewAttendance(request):
    student = Student.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(course = student.course_id)
    action = request.GET.get('action')
    get_subject = None
    attendance_report = None
    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            get_subject = Subject.objects.get(id=subject_id)
            attendance_report = AttendanceReport.objects.filter(student_id=student, attendance_id__subject_id=subject_id)
    context = {
        'subjects': subjects, 'action': action, 'get_subject': get_subject,
        'attendance_report': attendance_report,
    }
    return render(request, 'Student/view_attendance.html', context)

def ViewResult(request):
    marks = None
    student = Student.objects.get(admin=request.user.id)
    result = StudentResult.objects.filter(student_id = student)
    for i in result:
        assignment_marks = i.assignment_marks
        exam_marks = i.exam_marks
        marks = assignment_marks + exam_marks
    context = {
        'result': result, 'marks': marks
    }
    return render(request, 'Student/view_result.html', context)