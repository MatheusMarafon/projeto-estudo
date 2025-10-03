from django.urls import path
from . import views

app_name = "estudos"

urlpatterns = [
    path("", views.home, name="home"),
    path("django/", views.django_view, name="django"),
    path("bootstrap/", views.bootstrap_view, name="bootstrap"),
    path("rd-station/", views.rd_station_view, name="rd_station"),
    path("d4sign/", views.d4sign_view, name="d4sign"),
    path("chatbot/send/", views.chatbot_send, name="chatbot_send"),
    path("atividades/", views.atividades_view, name="atividades"),
    path("api/quiz-questions/", views.quiz_questions_api, name="quiz_api"),
]
