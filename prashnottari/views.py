from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Question, Answer, Profile, Bookmark
from .forms import QuestionForm, AnswerForm, ProfileForm, SignUpForm

# Create your views here.
@login_required
def home(request):
    #questions = Question.objects.all().order_by('-created_date')
    answers = Answer.objects.all().order_by('-added_date')
    bookmarks = request.user.bookmarks.filter(bookmarked_answer__in = answers).values_list('bookmarked_answer', flat=True)

    return render(request, 'home.html', {'answers': answers, 'bookmarked_pks': bookmarks})

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

    unanswered_questions = questions.filter(pk__in=uqpks)

    return render(request, 'unanswered_questions.html', {'questions': unanswered_questions})

@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk = pk)
    answers = Answer.objects.filter(question = question)
    bookmarks = request.user.bookmarks.filter(bookmarked_answer__in = answers).values_list('bookmarked_answer', flat=True)
    try:
        user_answer = answers.get(answerer__username = request.user.get_username())
    except  Answer.DoesNotExist:
        user_answer = None

    return render(request, 'question_detail.html', {'question': question, 'answers': answers, 'user_answer': user_answer, 'bookmarked_pks': bookmarks})

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
            return redirect('question_detail', pk = pk)
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
            return redirect('my_questions')
    else:
        form = QuestionForm()

    return render(request, 'ask.html', {'form': form})

@login_required
def edit_profile(request):
    try:
        profile = Profile.objects.get(name = request.user)
    except Profile.DoesNotExist:
        profile = Profile()
        profile.name = request.user

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
    #questions = Question.objects.filter(asker__username = request.user.get_username()).order_by('-created_date')
    questions = request.user.questions.all().order_by('-created_date')

    return render(request, 'my_questions.html', {'questions': questions})

@login_required
def my_answers(request):
    #answers = Answer.objects.filter(answerer__username = request.user.get_username()).order_by('-added_date')
    answers = request.user.answers.all().order_by('-added_date')
    bookmarks = request.user.bookmarks.filter(bookmarked_answer__in = answers).values_list('bookmarked_answer', flat=True)

    return render(request, 'my_answers.html', {'answers': answers, 'bookmarked_pks': bookmarks})

@login_required
def my_bookmarks(request):

    bookmarked_answer_pks = request.user.bookmarks.all().values('bookmarked_answer').order_by('-bookmarking_time')
    bmpks = [item['bookmarked_answer'] for item in bookmarked_answer_pks]
    bookmarked_answers = Answer.objects.filter(pk__in = bookmarked_answer_pks)
    bookmarked_answers = dict([(answer.pk, answer) for answer in bookmarked_answers])
    bookmarked_answers = [bookmarked_answers[pk] for pk in bmpks]

    return render(request, 'my_bookmarks.html', {'bookmarked_answers': bookmarked_answers})    

@login_required
def delete_question(request, pk):
    question = get_object_or_404(Question, pk = pk)
    if request.user == question.asker:
        question.delete()

    return redirect('my_questions')

@login_required
def delete_answer(request, pk):
    answer = get_object_or_404(Answer, pk = pk)
    if request.user == answer.answerer:
        answer.delete()

    return redirect('question_detail', pk = answer.question.pk)

@login_required
def bookmark(request):
        if request.method == 'GET':
               ans_pk = request.GET['anspk']
               answer = get_object_or_404(Answer, pk = ans_pk)

               try:
                   bookmark = Bookmark.objects.get(bookmarker_user = request.user, bookmarked_answer = answer)
                   bookmark.delete()
               except Bookmark.DoesNotExist:
                   new_bookmark = Bookmark(bookmarker_user = request.user, bookmarked_answer = answer, bookmarking_time = timezone.now())
                   new_bookmark.save()

               return HttpResponse("Success!") # Sending an success response
        else:
               return HttpResponse("Request method is not a GET")

def signup(request):
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()    
    return render(request, 'signup.html', {'form': form})
               

def error_404_view(request, exception):
    data = {}
    return render(request,'error_404.html', data)               