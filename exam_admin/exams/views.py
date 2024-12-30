from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.contrib import messages
from exams.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Exam, Question, Option, Answer, Result
from .forms import UserRegistrationForm, AnswerForm
from django.http import HttpResponse
from django.contrib.auth import get_user_model

def home(request):
    return render(request, 'home.html') 

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  
            user.save()

            messages.success(request, "Registration successful. You can now log in.")
            return redirect('exam_list')
        else:
            messages.error(request, "There was an error with your registration. Please try again.")
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user_instance = User.objects.get(username=username)

        user_authenticated = authenticate(request, username=username, password=password)
        if user_authenticated is not None:
            login(request, user_authenticated)
            return redirect('exam_list')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('home')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'exam_list.html', {'exams': exams})

@login_required
def take_exam(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    questions = exam.questions.all()

    if request.method == 'POST':
        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            Answer.objects.create(
                student=request.user,
                question=question,
                selected_option=selected_option
            )
        return redirect('exam_result', exam_id=exam.id)

    context = {'exam': exam, 'questions': questions}
    return render(request, 'take_exam.html', context)

@login_required
def exam_result(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    questions = exam.questions.all()
    correct_answers = 0

    for question in questions:
        answer = Answer.objects.get(student=request.user, question=question)
        if answer.selected_option == question.correct_answer:
            correct_answers += 1

    score = (correct_answers / len(questions)) * 100
    status = 'pass' if score >= 50 else 'fail'

    Result.objects.create(student=request.user, exam=exam, score=score, status=status)
    
    return render(request, 'exam_result.html', {'score': score, 'status': status})
