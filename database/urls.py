from django.urls import path

from database import views
app_name='databaseapp'
urlpatterns = [
    path('recost/',views.reducecost,name='recost'),
]