from django.urls import path
from .views import Home, PostView, Programs,UserloginForm,SignUpFormView,Contact
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('home/', Home.as_view(), name='home'),
    path('category/<slug:slug>/', PostView.as_view(), name="category-detail"),
    path('program/', Programs.as_view(), name='program'),
    path('',UserloginForm.as_view(), name="login"),
    path('register/',SignUpFormView.as_view(), name="register"),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('contact/',Contact, name="contact")
]