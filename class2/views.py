from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.db.models import query
from django.forms.forms import Form
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.http.response import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django import forms
import datetime
import json
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from .forms import UserRegisterForm, ProfileForm
from .models import Profile, Class, Course
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


def home(request):
    context = {
        'courses': Course.objects.all()
    }
    return render(request, 'class/index.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            username = form.cleaned_data.get('username')
            return HttpResponseRedirect(reverse("login"))
    else:
        form = UserRegisterForm()
        profile_form = ProfileForm()
    return render(request, 'class/register.html', {'form': form, 'profile_form': profile_form})


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'class/course.html'
    

class CourseListView(ListView):
    model = Course
    template_name = 'class/index.html'
    context_object_name = 'courses'


@login_required
@require_POST
def get_enrolled(request, slug):
    get_course = get_object_or_404(Course, slug=slug)
    get_course.enrolled_students.add(request.user)
    messages.success(request, 'Enrolled Successfully')
    return redirect("course",slug=get_course.slug)


class YourCourses(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'class/your_courses.html'
    context_object_name = 'your_courses'

    def get_queryset(self):
        return Course.objects.filter(enrolled_students=self.request.user)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile

    def get_object(self):
        return get_object_or_404(self.model, user=self.request.user)

