from django.contrib import auth, messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from accounts.forms import StudentSignUpForm, ParentSignUpForm, UserRegister
from accounts.models import Student
from adminmodule import views, studentviews, parentviews
from adminmodule.forms import AddReviewForm
from adminmodule.models import Review


def home(request):
    review = Review.objects.all().order_by('-id')[:6
             ]
    form = AddReviewForm()
    if request.method == 'POST':
        form = AddReviewForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('/')
    return render(request, 'home.html',{'data':review,'form':form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_page')
        elif user is not None and user.is_parent:
            if user.parent.approval_status == True:
                login(request, user)
                return redirect('parent_page')
            else:
                messages.info(request, 'You are not Approved to login')
        elif user is not None and user.is_student:
            if user.student.approval_status == True:
                login(request, user)
                return redirect('student_page')
            else:
                messages.info(request, 'You are not Approved to login')

        else:
            messages.info(request, 'Invalid Credentials')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/')


def select_role(request):
    if request.method == 'POST':
        role = request.POST.get('role')

        if role == 'Student':
            return redirect('accounts:student_register')
        elif role == 'Parent':
            return redirect('accounts:parent_register')
        else:
            messages.info(request, 'Please Choose Your Type')

    return render(request, 'select_role.html')


def student_register(request):
    u_form = UserRegister()
    form = StudentSignUpForm()
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST,request.FILES)
        u_form = UserRegister(request.POST)
        if form.is_valid() and u_form.is_valid():
            user = u_form.save(commit=False)
            user.is_student = True
            user.save()
            student = form.save(commit=False)
            student.role = 'Student'
            student.user = user
            student.save()
            messages.info(request, 'Student registered Successfully')
            return redirect('accounts:login_view')
    return render(request, 'student_register.html', {'form': form, 'u_form': u_form})


def parent_register(request):
    u_form = UserRegister()
    form = ParentSignUpForm()
    if request.method == 'POST':
        u_form = UserRegister(request.POST)
        form = ParentSignUpForm(request.POST)
        if form.is_valid() and u_form.is_valid():
            user = u_form.save(commit=False)
            user.is_parent = True
            user.save()
            parent = form.save(commit=False)
            parent.role = 'Parent'
            parent.user = user
            parent.save()
            messages.info(request, 'Parent registered Successfully')
            return redirect('accounts:login_view')
    return render(request, 'parent_register.html', {'form': form, 'u_form': u_form})
