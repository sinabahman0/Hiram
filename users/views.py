from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView, View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import User
from .forms import SignUpForm, LoginForm, CompleteProfileForm


class SignUpView(FormView):
    template_name = 'users/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('complete_profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ثبت‌نام'
        return context


class CompleteProfileView(LoginRequiredMixin, FormView):
    template_name = 'users/complete_profile.html'
    form_class = CompleteProfileForm
    success_url = reverse_lazy('home')
    login_url = 'login'

    def get_object(self):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تکمیل پروفایل'
        return context

    def get(self, request, *args, **kwargs):
        # اگر پروفایل قبلاً تکمیل شده بود، به home برو
        if request.user.profile_completed:
            return redirect('home')
        return super().get(request, *args, **kwargs)


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.get_user()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ورود'
        return context


class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'users/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class HomeView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        try:
            user = request.user

            # اگر دانش‌اموز است و پروفایل تکمیل نشده باشد
            if user.user_type == 'student' and not user.profile_completed:
                return redirect('complete_profile')

            if user.user_type == 'student':
                return redirect('student_home')

            elif user.user_type == 'admin':
                return redirect('admin_home')

            elif user.user_type == 'advisor':
                return redirect('advisor_home')

            elif user.is_superuser:
                return redirect('admin_home')
            else:
                # اگر user_type تنظیم نشده باشد
                return HttpResponse('خطا: نقش کاربر تنظیم نشده است', status=400)
        except Exception as e:
            return HttpResponse(f'خطا: {str(e)}', status=500)


class StudentHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'users/student_home.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user

        try:
            relationship = user.as_student
            context['advisor'] = relationship.advisor
            context['admin'] = relationship.admin
        except:
            context['advisor'] = None
            context['admin'] = None

        return context

    def get(self, request, *args, **kwargs):
        if request.user.user_type != 'student':
            return redirect('home')
        if not request.user.profile_completed:
            return redirect('complete_profile')
        return super().get(request, *args, **kwargs)


class AdminHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'users/admin_home.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user

        students = user.students_under_admin.all()
        context['students'] = students

        return context

    def get(self, request, *args, **kwargs):
        if request.user.user_type != 'admin' and not request.user.is_superuser:
            return redirect('home')
        return super().get(request, *args, **kwargs)


class AdvisorHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'users/advisor_home.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user

        students = user.students_under_advisor.all()
        context['students'] = students

        return context

    def get(self, request, *args, **kwargs):
        if request.user.user_type != 'advisor':
            return redirect('home')
        return super().get(request, *args, **kwargs)
