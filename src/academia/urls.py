from django.urls import path
from . import views

urlpatterns = [
   path('', views.academic_year_list, name="academic_years"),
   path('<str:academic_year>/', views.course_list, name="courses"),
   path('<str:academic_year>/<slug:course_slug>/', views.chapter_list, name="chapters"),
   path('<str:academic_year>/<slug:course_slug>/<slug:topic_slug>/', views.topic_detail, name="topic"),
]