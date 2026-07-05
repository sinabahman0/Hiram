from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView, TemplateView


class StudentPlaningView(LoginRequiredMixin, TemplateView):
    template_name = 'planer/student_planing.html'
    login_url = 'login'


