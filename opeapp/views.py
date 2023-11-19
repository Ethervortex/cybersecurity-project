from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Student, Course, CourseStudent
from django.contrib.auth import get_user_model
from django.db.models import Q

@login_required
def home_view(request):
    context = {}
    return render(request, 'home.html', context)

def login_view(request):
    context = {}
    #if request.user.is_authenticated:
    #    return render(request, 'home.html')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'home.html', context)
        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'login.html', context)

def signup_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        User = get_user_model()
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            # Create a new user
            user = User.objects.create_user(username=username, password=password1)
            user.save()
            messages.success(request, 'Your account has been created. You can now log in.')
            return render(request, 'login.html', context)

    return render(request, 'signup.html', context)

def logout_view(request):
    logout(request)
    return render(request, 'login.html')

@login_required
def students_view(request):
    if request.method == "POST":
        student_name = request.POST.get('student_name')
        creator_id = request.user.id
        print('Student name: ', student_name, ' creator id: ', creator_id)
        existing_student = Student.objects.filter(name=student_name, creator=creator_id).exists()

        if existing_student:
            messages.error(request, "A student with this name already exists.")
        else:
            new_student = Student(name=student_name, creator=request.user) # Ei toimi auth.user kanssa, selvitä
            print('new student: ', new_student)
            new_student.save()
            messages.success(request, f"{student_name} added successfully.")

    # Fetch all students associated with the current user
    creator_id = request.user.id
    search_query = request.GET.get('search_query')

    if search_query:
        # If there is a search query, filter students based on the query
        students = Student.objects.filter(Q(name__icontains=search_query) & Q(creator=creator_id))
    else:
        # If no search query, get all students for the current user
        students = Student.objects.filter(creator=creator_id)

    context = {
        'students': students
    }
    print('Creator_id: ', creator_id)
    return render(request, 'students.html', context)

@login_required
def courses_view(request):
    if request.method == "POST":
        course_name = request.POST.get('course_name')
        creator_id = request.user.id
        print('Course name: ', course_name, ' creator id: ', creator_id)
        existing_course = Course.objects.filter(name=course_name, creator=creator_id).exists()

        if existing_course:
            messages.error(request, "A course with this name already exists.")
        else:
            creator = request.user
            new_course = Course(name=course_name, creator=creator)
            print('new course: ', new_course)
            new_course.save()
            messages.success(request, f"{course_name} added successfully.")

    # Fetch all students associated with the current user
    creator_id = request.user.id
    courses = Course.objects.filter(creator=creator_id)

    context = {
        'courses': courses
    }
    print('Creator_id: ', creator_id)
    return render(request, 'courses.html', context)

@login_required
def add_course_students(request, course_id):
    if request.method == 'POST':
        student_ids = request.POST.getlist('student_ids')
        course = Course.objects.get(pk=course_id)

        CourseStudent.objects.filter(course=course).delete()
        print('Student_ids: ', student_ids)
        for student_id in student_ids:
            student = Student.objects.get(pk=student_id)
            print('Student: ', student)
            CourseStudent.objects.create(course=course, student=student)

        messages.success(request, "Course students updated successfully.")
        courses = Course.objects.filter(creator=request.user.id)
        return render(request, 'courses.html', {'courses': courses})

    course = Course.objects.get(pk=course_id)
    students = Student.objects.all()
    course_students = CourseStudent.objects.filter(course=course)
    associated_student_ids = [cs.student.id for cs in course_students]
    print('Associated student ids: ', associated_student_ids, course_students, course)
    context = {
        'course_name': course.name,
        'course_id': course.id,
        'students': students,
        'associated_student_ids': associated_student_ids,
    }

    return render(request, 'course.html', context)

@login_required
def grades_view(request):
    if request.method == 'POST':
        for key in request.POST:
            if key.startswith('grade-'):
                _, student_id, course_id = key.split('-')
                grade = request.POST[key]

                course_student = CourseStudent.objects.get(
                    course_id=int(course_id),
                    student_id=int(student_id)
                )
                course_student.grade = int(grade)
                course_student.save()
        messages.success(request, "Grades updated successfully.")

        # After updating grades, re-fetch the data and render the template
        courses = Course.objects.filter(creator=request.user)
        students_courses = {}

        for course in courses:
            associated_students = CourseStudent.objects.filter(course=course)
            student_data = []
            for student in associated_students:
                student_data.append({
                    'student_id': student.student.id,
                    'student_name': student.student.name,
                    'course_id': student.course.id,
                    'grade': student.grade,
                })

            students_courses[course.name] = {'students': student_data}

        context = {
            'courses': courses,
            'students_courses': students_courses,
        }
        return render(request, 'grades.html', context)
    
    # If it's a GET request, initially render the page with the course and student data
    courses = Course.objects.filter(creator=request.user)
    students_courses = {}

    for course in courses:
        associated_students = CourseStudent.objects.filter(course=course)
        student_data = []
        for student in associated_students:
            student_data.append({
                'student_id': student.student.id,
                'student_name': student.student.name,
                'course_id': student.course.id,
                'grade': student.grade,
            })

        students_courses[course.name] = {'students': student_data}

    context = {
        'courses': courses,
        'students_courses': students_courses,
    }
    return render(request, 'grades.html', context)

@login_required
def student_details(request, student_id):
    student = Student.objects.get(pk=student_id)

    course_students = CourseStudent.objects.filter(student=student)
    student_courses = {}

    for course_student in course_students:
        course_name = course_student.course.name
        grade = course_student.grade

        student_courses[course_name] = {'grade': grade}

    context = {
        'student_name': student.name,
        'course_students': student_courses
    }

    return render(request, 'student.html', context)