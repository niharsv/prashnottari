from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Question, Answer, Profile
from .forms import QuestionForm, AnswerForm, ProfileForm

# Create your views here.
@login_required
def home(request):
    questions = Question.objects.all().order_by('-created_date')
    answers = Answer.objects.all().order_by('-added_date')

    return render(request, 'home.html', {'questions': questions, 'answers': answers})

@login_required
def unanswered(request):
    questions = Question.objects.all().order_by('-created_date')
    answers = Answer.objects.all().order_by('-added_date')

    qpks = set()
    apks = set()
    for answer in answers:
        apks.add(answer.question.pk)
    for question in questions:
        qpks.add(question.pk)
    uqpks = qpks - apks

    return render(request, 'unanswered_questions.html', {'questions': questions, 'unanswered_question_pks': uqpks})

@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk = pk)
    answers = Answer.objects.filter(question = question)

    return render(request, 'question_detail.html', {'question': question, 'answers': answers})

@login_required
def write_answer(request, pk):
    question = get_object_or_404(Question, pk = pk)

    try:
        answer = Answer.objects.get(question = question, answerer__username = request.user.get_username())
    except Answer.DoesNotExist:
        answer = Answer()
        answer.question = question

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.answerer = request.user
            answer.added_date = timezone.now()
            answer.save()
            return redirect('question_detail', pk=pk)
    else:
        form = AnswerForm(instance=answer)

    return render(request, 'write_answer.html', {'question': question, 'answer': answer, 'form': form})

@login_required
def ask(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.asker = request.user
            question.created_date = timezone.now()
            question.save()
            return redirect('home')
    else:
        form = QuestionForm()

    return render(request, 'ask.html', {'form': form})

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, name = request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance = profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.name = request.user
            profile.save()
            return redirect('home')
    else:
        form = ProfileForm(instance = profile)

    return render(request, 'profile.html', {'profile' : profile, 'form': form})

@login_required
def my_questions(request):
    questions = Question.objects.filter(asker__username = request.user.get_username()).order_by('-created_date')

    return render(request, 'my_questions.html', {'questions': questions})

@login_required
def my_answers(request):
    answers = Answer.objects.filter(answerer__username = request.user.get_username()).order_by('-added_date')

    return render(request, 'my_answers.html', {'answers': answers})
