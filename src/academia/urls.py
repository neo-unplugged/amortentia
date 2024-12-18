from django.urls import path
from .views import home_view, detail_view 

urlpatterns = [
    path('', home_view, name='homepage'),
    path('<str:id>', detail_view, name='details')
]