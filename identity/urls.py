from django.urls import path
from identity.views.account import Register, CustomLoginView, CustomPasswordChangeView

app_name='identity'
urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/',CustomLoginView.as_view(),name='login'),
    path('passwordchange/',CustomPasswordChangeView.as_view(),name='passwordchange'),
]