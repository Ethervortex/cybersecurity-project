from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Student
from django.contrib.auth import get_user_model

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
    students = Student.objects.filter(creator=creator_id)

    context = {
        'students': students
    }
    print('Creator_id: ', creator_id)
    return render(request, 'students.html', context)