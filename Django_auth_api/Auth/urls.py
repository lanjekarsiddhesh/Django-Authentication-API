
from django.urls import path
from .views import *

urlpatterns = [
    path('Registration/', Registration_API.as_view()),
    path('Login/', Login_API.as_view()),
    # path('Authentication/<int:pk>/', Registration_API.as_view()),
    path('changePassword/',ChangePassword.as_view()),
    path('Send-Email-To-ResetPassword/',SendEmailToResetPassword.as_view()),
    path('ResetPassword/<uuid>/<token>/',resetPassword.as_view()),
    path('Profile/',UserView.as_view())
]
