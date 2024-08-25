from django.urls import path
from . import views


urlpatterns = [
    path('register/' , views.UserRegiterView.as_view()),
    path('verify/' , views.VerifyRegistartions.as_view()),
    path('login/' , views.LoginUserView.as_view()),
    path("resend/code/", views.ResendVerifyCode.as_view()),
    path("password/forget/", views.UserForgetPasswordToEmail.as_view()),
    path("password/update/", views.UserResetPasswordView.as_view()),
    path("update/", views.UserUpdateView.as_view()),
    path("me/", views.UserdetailView.as_view()),
]