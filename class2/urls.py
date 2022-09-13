from django import VERSION
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CourseDetailView, CourseListView, YourCourses, ProfileDetailView
from . import views


from . import views

urlpatterns = [
	path("", CourseListView.as_view(), name="index"),
    path("login", auth_views.LoginView.as_view(template_name='class/login.html'), name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<slug>", CourseDetailView.as_view(), name="course"),
    path('get_enrolled/<slug>/', views.get_enrolled, name='get_enrolled'),
    path('your_courses/', YourCourses.as_view(), name='your_courses'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
]