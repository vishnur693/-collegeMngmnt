from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from myapp.models import courseDB, studentDB, teacherDB
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from myapp.models import teacherDB
from django.views.decorators.csrf import csrf_protect



def loginPage(request):
    return render(request, 'loginPage.html')

@login_required
def adminHome(request):
    return render(request, 'adminHome.html')

def signupPage(request):
    courses = courseDB.objects.all()
    return render(request, 'signup.html', {"courses": courses})

@login_required
def teacherHome(request):
    teacher = get_object_or_404(teacherDB, t_user=request.user)
    return render(request, 'teacherHome.html', {'teacher_name': teacher.t_user.username})

@csrf_protect
def submitSignup(request):
    if request.method == 'POST':
        fname = request.POST['fullname']
        mail = request.POST['email']
        pswrd = request.POST['password']
        cpswrd = request.POST['confirm_password']

        if pswrd == cpswrd:
            if User.objects.filter(email=mail).exists():
                messages.info(request, 'This email already exists!')
                return redirect('signupPage')
            else:
                user = User.objects.create_user(
                    username=fname,
                    email=mail,
                    password=pswrd
                )
                user.save()
                return redirect('homePage')
        else:
            messages.info(request, "Password doesn't match!")
            return redirect('signupPage')
    return render(request, 'signup.html')

@csrf_protect
def loginBtn(request):
    if request.method == 'POST':
        uname = request.POST['username']
        pswrd = request.POST['password']

        user = auth.authenticate(username=uname, password=pswrd)

        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('adminHome')
            else:
                return redirect('teacherHome')
        else:
            messages.info(request, "Invalid credentials")
            return redirect('loginPage')
    return render(request, 'loginPage.html')

@login_required
def addCourse(request):
    return render(request, 'addCourse.html')

@csrf_protect
@login_required
def course_db(request):
    if request.method == 'POST':
        name = request.POST['courseName']
        fee = request.POST['courseFee']

        details = courseDB(course_name=name, course_fee=fee)
        details.save()
        return redirect('addStudent')

@login_required
def addStudent(request):
    courses = courseDB.objects.all()
    return render(request, 'addStudent.html', {"courses": courses})

@csrf_protect
@login_required
def addStudent_db(request):
    if request.method == "POST":
        sname = request.POST.get('studentName')
        saddress = request.POST.get('address')
        sage = request.POST.get('age')
        sel = request.POST.get('course')
        
        if not all([sname, saddress, sage, sel]):
            return HttpResponseBadRequest("Missing fields")

        course1 = get_object_or_404(courseDB, id=sel)
        student = studentDB(student_name=sname, address=saddress, age=sage, course=course1)
        student.save()
        return redirect('showStudents')

@login_required
def showStudents(request):
    students = studentDB.objects.all()
    return render(request, 'showStudents.html', {'students': students})

@csrf_protect
@login_required
def editStudent(request, student_id):
    student = get_object_or_404(studentDB, id=student_id)
    courses = courseDB.objects.all()
    if request.method == 'POST':
        student.student_name = request.POST['studentName']
        student.address = request.POST['address']
        student.age = request.POST['age']
        course_id = request.POST['course']
        student.course = get_object_or_404(courseDB, id=course_id)
        student.save()
        return redirect('showStudents')
    return render(request, 'editStudent.html', {'student': student, 'courses': courses})

@csrf_protect
@login_required
def deleteStudent(request, student_id):
    student = get_object_or_404(studentDB, id=student_id)
    student.delete()
    return redirect('showStudents')

@csrf_protect
def addTeacher(request):
    if request.method == 'POST':
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        uname = request.POST['username']
        em = request.POST['email']
        pswd = request.POST['password']
        cpswd = request.POST['cpassword']

        tradd = request.POST['address']
        trage = request.POST['age']
        trcno = request.POST['contact_number']
        trpht = request.FILES['teacher_image']
        trselcrs = request.POST['course']
        crs = get_object_or_404(courseDB, id=trselcrs)
        
        if pswd == cpswd:
            if User.objects.filter(username=uname).exists():
                messages.info(request, 'Entered username already exists')
                return redirect('signupPage')
            else:
                usr = User.objects.create_user(first_name=fname, last_name=lname, username=uname, email=em, password=pswd)
                usr.save()
                t = teacherDB(t_add=tradd, t_age=trage, t_cno=trcno, t_pht=trpht, t_course=crs, t_user=usr)
                t.save()
                return redirect('loginPage')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signupPage')
    return render(request, 'signup.html')

@login_required
def editProfilePage(request, id):
    teacher = get_object_or_404(teacherDB, id=id)
    courses = courseDB.objects.all()
    if request.method == 'POST':
        teacher.t_user.first_name = request.POST['firstname']
        teacher.t_user.last_name = request.POST['lastname']
        teacher.t_user.username = request.POST['username']
        teacher.t_user.email = request.POST['email']
        teacher.t_user.save()
        
        teacher.t_add = request.POST['address']
        teacher.t_age = request.POST['age']
        teacher.t_cno = request.POST['contact_number']
        if 'teacher_image' in request.FILES:
            teacher.t_pht = request.FILES['teacher_image']
        teacher.t_course = get_object_or_404(courseDB, id=request.POST['course'])
        teacher.save()
        
        return redirect('viewTeacher')
    return render(request, 'editProfile.html', {'teacher': teacher, 'courses': courses})

@login_required
def viewTeacher(request):
    teacher = get_object_or_404(teacherDB, t_user=request.user)
    return render(request, 'viewProfile.html', {'teacher': teacher})

@login_required
def logout_view(request):
    logout(request)
    return redirect('loginPage')
@login_required
def teacherHome(request):
    try:
        teacher = get_object_or_404(teacherDB, t_user=request.user)
    except teacherDB.DoesNotExist:
        # Redirect to a page informing the user that their profile is not complete or create a new profile
        return redirect('signupPage')  # Or any other appropriate page

    return render(request, 'teacherHome.html', {
        'teacher_name': teacher.t_user.username,
        'teacher_id': teacher.id
    })

def editProfilePage(request, id):
    teacher = get_object_or_404(teacherDB, id=id)
    courses = courseDB.objects.all()
    if request.method == 'POST':
        teacher.t_user.first_name = request.POST['firstname']
        teacher.t_user.last_name = request.POST['lastname']
        teacher.t_user.username = request.POST['username']
        teacher.t_user.email = request.POST['email']
        teacher.t_user.save()

        teacher.t_add = request.POST['address']
        teacher.t_age = request.POST['age']
        teacher.t_cno = request.POST['contact_number']
        if 'teacher_image' in request.FILES:
            teacher.t_pht = request.FILES['teacher_image']
        teacher.t_course = get_object_or_404(courseDB, id=request.POST['course'])
        teacher.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('viewTeacher')
    return render(request, 'editProfile.html', {'teacher': teacher, 'courses': courses})
@csrf_protect
@login_required
def deleteTeacher(request, teacher_id):
    teacher = get_object_or_404(teacherDB, id=teacher_id)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Teacher deleted successfully.')
    return redirect('adminHome')  # Redirect back to admin dashboard after deletion
def showTeachers(request):
    teacher=teacherDB.objects.all()
    return render(request,'showTeachers.html',{'teachers':teacher})
@csrf_protect
def addTeacher(request):
    if request.method == 'POST':
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        uname = request.POST['username']
        em = request.POST['email']
        pswd = request.POST['password']
        cpswd = request.POST['cpassword']

        tradd = request.POST['address']
        trage = request.POST['age']
        trcno = request.POST['contact_number']
        trpht = request.FILES['teacher_image']
        trselcrs = request.POST['course']
        crs = get_object_or_404(courseDB, id=trselcrs)
        
        if pswd == cpswd:
            if User.objects.filter(username=uname).exists():
                messages.info(request, 'Entered username already exists')
                return redirect('signupPage')
            else:
                usr = User.objects.create_user(first_name=fname, last_name=lname, username=uname, email=em, password=pswd)
                usr.save()
                t = teacherDB(t_add=tradd, t_age=trage, t_cno=trcno, t_pht=trpht, t_course=crs, t_user=usr)
                t.save()
                return redirect('loginPage')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signupPage')
    return render(request, 'signup.html')
