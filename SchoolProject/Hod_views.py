import re
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from SchoolApp.models import *
from django.contrib import messages
from datetime import datetime


@login_required(login_url='/')
def HOME(request):
    student_count = Student.objects.all().count()
    staff_count = Staff.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count = Subject.objects.all().count()

    student_gender_male = Student.objects.filter(gender = 'male').count()
    student_gender_female = Student.objects.filter(gender = 'female').count()

    # print(student_gender_male)
    # print(student_gender_female)

    context = {
        'student_count':student_count, 'staff_count':staff_count, 'course_count':course_count, 'subject_count':subject_count,
        'student_gender_male':student_gender_male, 'student_gender_female':student_gender_female
    }
    
    return render(request, 'hod/Home.html', context)


@login_required(login_url='/')
def ADD_STUDENT(request):
    course = Course.objects.all()
    session = SchoolSession.objects.all()

    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_id = request.POST.get('session_id')
        # print(profile_pic,first_name,last_name,email,username,password,address,gender,course_id,session_id)

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, "Email is already taken")
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, "Username is already taken")
            return redirect('add_student')
        else:
            user = CustomUser(
                profile_pic = profile_pic,
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                user_type = 3
            )
            user.set_password(password)
            user.save()

            course = Course.objects.get(id=course_id)
            session_y = SchoolSession.objects.get(id=session_id)
            student = Student(
                admin = user,
                address = address,
                session_id = session_y,
                course_id = course,
                gender = gender,
            )
            student.save()
            messages.success(request, user.first_name+ '-' + user.last_name + " are successfully added")
            return redirect('add_student')

    context = {
        "course":course,
        "session":session,

    }
    return render(request, 'Hod/add_student.html', context)

@login_required(login_url='/')
def VIEW_STUDENT(request):
    student = Student.objects.all()
    context = {
        'student':student 
    }
    return render(request, 'Hod/view_student.html', context)

@login_required(login_url='/')
def EDIT_STUDENT(request, id):
    student = Student.objects.get(id=id)
    course = Course.objects.all()
    session = SchoolSession.objects.all()
    
    context = {
        'student':student,
        'course':course,
        'session':session,
    }
    return render(request, 'Hod/edit_student.html', context)
    
@login_required(login_url='/')
def UPDATE_STUDENT(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_id = request.POST.get('session_id')

        user = CustomUser.objects.get(id=student_id)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.password = password
        if password !=None and password != "":
            user.set_password(password)
        if profile_pic !=None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()

        student = Student.objects.get(admin=student_id)
        student.address = address
        student.gender = gender

        course = Course.objects.get(id=course_id)
        student.course_id = course

        session = SchoolSession.objects.get(id=session_id)
        student.session_id = session
        student.save()
        messages.success(request, "Record has been updated successfully!")
        return redirect('view_student')


    return render(request, 'Hod/edit_student.html')

@login_required(login_url='/')
def DELETE_STUDENT(request, admin):
    student = CustomUser.objects.get(id=admin)
    student.delete()
    messages.success(request, 'Record are successfully deleted!')
    return redirect('view_student')

@login_required(login_url='/')
def Add_Course(request):
    if request.method == "POST":
        course_name = request.POST.get('course_name')
        course = Course(
            name = course_name
        )
        course.save()
        messages.success(request, "Course has been added successfully !")
        return redirect('add_course')
    return render(request, 'Hod/add_course.html')

@login_required(login_url='/')
def View_Course(request):
    course = Course.objects.all()
    context = {
        'course':course,
    }
    return render(request, 'Hod/view_course.html', context)

@login_required(login_url='/')
def Edit_Course(request, id):
    course = Course.objects.get(id=id)
    context = {
        'course':course,
    }
    return render(request, 'Hod/edit_course.html', context)

@login_required(login_url='/')
def Update_Course(request):
    if request.method == "POST":
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course_name')
        course = Course.objects.get(id=course_id)
        course.name = course_name
        course.save()
        messages.success(request, "Course has been updated successfully")
        return redirect('view_course')

    return render(request, 'Hod/edit_course.html')

@login_required(login_url='/')
def Delete_Course(request, id):
    course = Course.objects.get(id=id)
    course.delete()
    messages.success(request, 'Course Has been deleted successfully!')
    return redirect('view_course')

@login_required(login_url='/')
def Add_Staff(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, "Email is already taken")
            return redirect('add_staff')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, "Username is already taken")
            return redirect('add_staff')
        else:
            user = CustomUser(
                profile_pic = profile_pic,
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                user_type = 2
            )
            user.set_password(password)
            user.save()

            staff = Staff(
                admin = user,
                address = address,
                gender = gender,
            )
            staff.save()
            messages.success(request, "Staff are successfully added")
            return redirect('add_staff')

    return render(request, 'Hod/add_staff.html')

@login_required(login_url='/')
def View_Staff(request):
    staff = Staff.objects.all()
    context = {
        'staff':staff
    }

    return render(request, 'Hod/view_staff.html', context)

@login_required(login_url='/')
def Edit_Staff(request, id):
    staff = Staff.objects.get(id=id)

    context = {
        'staff':staff
    }
    return render(request, 'Hod/edit_staff.html', context)

@login_required(login_url='/')
def Update_Staff(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')

        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        address = request.POST.get('address')
        gender = request.POST.get('gender')

        user = CustomUser.objects.get(id=staff_id)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        

        if password !=None and password != "":
            user.set_password(password)
        if profile_pic !=None and profile_pic != "":
            user.profile_pic = profile_pic

        user.save()

        staff = Staff.objects.get(id=staff_id)
        staff.gender = gender
        staff.address = address

        staff.save()
        messages.success(request, 'staff updated scuccefffully')
        return redirect('view_staff')

    return render(request, 'Hod/edit_staff.html')

@login_required(login_url='/')
def Delete_Staff(request, id):
    staff = CustomUser.objects.get(id=id)
    staff.delete()
    messages.success(request, 'Record Has been deleted successfully!')
    return redirect('view_staff')

@login_required(login_url='/')
def Add_Subject(request):
    course = Course.objects.all()
    staff = Staff.objects.all()

    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        course = Course.objects.get(id=course_id)
        staff = Staff.objects.get(id=staff_id)
        
        subject = Subject(
            name = subject_name,
            course = course,
            staff = staff,
        )
        subject.save()
        messages.success(request, 'Your Subject has been saved successfully!')
        return redirect('add_subject')

    context = {
        'course':course,
        'staff':staff,
    }
    return render(request, 'Hod/add_subject.html', context)

@login_required(login_url='/')
def View_Subject(request):
    subject = Subject.objects.all()
    context = {
        'subject':subject
    }
    return render(request, 'Hod/view_subject.html', context)

@login_required(login_url='/')
def Edit_Subject(request, id):
    subject = Subject.objects.get(id=id)
    course = Course.objects.all()
    staff = Staff.objects.all()
    context = {
        'subject':subject,
        'course':course,
        'staff':staff,
    }
    return render(request, 'Hod/edit_subject.html', context)

@login_required(login_url='/')
def Update_Subject(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')

        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')
        

        course = Course.objects.get(id=course_id)
        staff = Staff.objects.get(id=staff_id)

        subject = Subject(
            id = subject_id,
            name = subject_name,
            course = course,
            staff = staff

        )
        subject.save()
        messages.success(request, 'Subject has been updated successfully')
        return redirect('view_subject')
    # return render(request, 'Hod/view_subject.html')

@login_required(login_url='/')
def Delete_Subject(request, id):
    subject = Subject.objects.get(id=id)
    subject.delete()
    messages.success(request, 'Subject has been deleted successfully')
    return redirect('view_subject')

@login_required(login_url='/')
def Add_Session(request):
    if request.method == "POST":
        # sess_start = request.POST.get('sess_start')
        # sess_end = request.POST.get('sess_end')

        sess_start = datetime.strptime(request.POST['sess_start'], '%d/%m/%Y')
        sess_end = datetime.strptime(request.POST['sess_end'], '%d/%m/%Y')

        syear = SchoolSession(
            SessionStart = sess_start,
            SessionEnd = sess_end,
        )
        syear.save()
        messages.success(request, 'Session has been saved successfully!')
        return redirect('view_session')
    return render(request, 'Hod/Session/add_session.html')

@login_required(login_url='/')
def View_Session(request):
    schsession = SchoolSession.objects.all()
    context = {
        'schsession':schsession,
    }
    return render(request, 'Hod/Session/view_session.html', context)

@login_required(login_url='/')
def Edit_Session(request, id):
    schsession = SchoolSession.objects.get(id=id)
    context = {
        'schsession':schsession,
    }
    return render(request, 'Hod/Session/edit_session.html', context)

@login_required(login_url='/')
def Update_Session(request):
    if request.method == "POST":
        sess_id = request.POST.get('sess_id')
        # sess_start = request.POST.get('sess_start')
        # sess_end = request.POST.get('sess_end')

        sess_start = datetime.strptime(request.POST['sess_start'], '%d/%m/%Y')
        sess_end = datetime.strptime(request.POST['sess_end'], '%d/%m/%Y')

        syear = SchoolSession(
            id = sess_id,
            SessionStart = sess_start,
            SessionEnd = sess_end,
        )
        syear.save()
        messages.success(request, 'Session has been updated successfully!')
        return redirect('view_session')
    return render(request, 'Hod/Session/update_session.html')

@login_required(login_url='/')
def Delete_Session(request, id):
    schsession = SchoolSession.objects.get(id=id)
    schsession.delete()
    messages.success(request, 'Session has been deleted successfully')
    return redirect('view_session')

@login_required(login_url='/')
def SendStaffNotification(request):
    staff = Staff.objects.all()
    see_notification = StaffNotification.objects.all().order_by('-id')[0:5]
    context = {
        'staff': staff, 'see_notification': see_notification
    }
    return render(request, 'Hod/send_staff_notification.html', context)

@login_required(login_url='/')
def SaveStaffNotification(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')

        staff = Staff.objects.get(admin = staff_id)
        notification = StaffNotification(
            staff_id = staff,
            message = message
        )
        notification.save()
        messages.success(request, 'Notification Successfully Send')
    return redirect('send_Staff_notification')

@login_required(login_url='/')
def StaffLeaveView(request):
    staff_leave = StaffLeave.objects.all()
    context = {
        'staff_leave':staff_leave
    }
    return render(request, 'Hod/staff_leave.html', context)

@login_required(login_url='/')
def ApproveLeave(request, id):
    leave = StaffLeave.objects.get(id = id)
    leave.status = 1
    leave.save()
    return redirect('staff_leave_view')

@login_required(login_url='/')
def DisApproveLeave(request, id):
    leave = StaffLeave.objects.get(id = id)
    leave.status = 2
    leave.save()
    return redirect('staff_leave_view')

@login_required(login_url='/')
def Staff_Feedback(request):
    feedback = StaffFeedBack.objects.all()
    feedback_history = StaffFeedBack.objects.all().order_by('-id')[0:5]
    context = {
        'feedback': feedback, 'feedback_history':feedback_history
    }
    return render(request, 'Hod/staff_feedback.html', context)

@login_required(login_url='/')
def Staff_FeedbackSave(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')
        feeback = StaffFeedBack.objects.get(id = feedback_id)
        feeback.feedback_reply = feedback_reply
        feeback.status = 1
        feeback.save() 
        return redirect('stafffeedback')
    

def SendStudentNotification(request):
    student = Student.objects.all()
    notification = StudentNotification.objects.all()
    context = {
        'student': student, 'notification':notification
    }
    return render(request, 'Hod/student_notification.html', context)

def SaveStudentNotification(request):
    if request.method == "POST":
        message = request.POST.get('message')
        student_id = request.POST.get('student_id')
        student = Student.objects.get(admin = student_id)
        std_notifitcation = StudentNotification(
            student_id = student,
            message = message
        )
        std_notifitcation.save()
        messages.success(request, "Notification has been send successfully!")
    return redirect('send_Std_notification')


@login_required(login_url='/')
def Student_Feedback(request):
    feedback = StudentFeedBack.objects.all()
    feedback_history = StudentFeedBack.objects.all().order_by('-id')[0:5]

    context = {
        'feedback': feedback, 'feedback_history': feedback_history
    }
    return render(request, 'Hod/std_feedback.html', context) 

@login_required(login_url='/')
def Student_FeedbackSave(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')
        feeback = StudentFeedBack.objects.get(id = feedback_id)
        feeback.feedback_reply = feedback_reply
        feeback.status = 1
        feeback.save() 
        return redirect('studentfeedback')
    

@login_required(login_url='/')
def StudentLeaveView(request):
    std_leave = StudentLeave.objects.all()
    context = {
        'std_leave':std_leave
    }
    return render(request, 'Hod/student_leave.html', context)

@login_required(login_url='/')
def StudentApproveLeave(request, id):
    leave = StudentLeave.objects.get(id = id)
    leave.status = 1
    leave.save()
    return redirect('stdleave_view')

@login_required(login_url='/')
def StudentDisApproveLeave(request, id):
    leave = StudentLeave.objects.get(id = id)
    leave.status = 2
    leave.save()
    return redirect('stdleave_view')


# def ViewAttendance(request):
#     return render(request, 'Hod/view_attendance.html')

def ViewAttendance(request):
    subject = Subject.objects.all()
    session_year = SchoolSession.objects.all()

    action = request.GET.get('action')
    get_subject = None
    get_session_year = None
    attendance_date = None
    attendance_report = None
    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')
            attendance_date = request.POST.get('attendance_date')

            get_subject = Subject.objects.get(id=subject_id)
            get_session_year = SchoolSession.objects.get(id=session_year_id)
            attendance = Attendance.objects.filter(subject_id=get_subject, date = attendance_date)
            for i in attendance:
                attendance_id = i.id
                attendance_report = AttendanceReport.objects.filter(attendance_id=attendance_id)

    context = {
        'subject': subject, 'session_year': session_year, 'action': action, 'get_subject': get_subject, 'get_session_year': get_session_year,
        'attendance_date': attendance_date, 'attendance_report': attendance_report  
    }
    return render(request, 'Hod/view_attendance.html', context)