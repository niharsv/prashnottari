from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('unanswered', views.unanswered, name='unanswered'),
    path('ask', views.ask, name='ask'),
    path('my_questions', views.my_questions, name='my_questions'),
    path('my_answers', views.my_answers, name='my_answers'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('question/<int:pk>/write_answer', views.write_answer, name='write_answer'),
]
