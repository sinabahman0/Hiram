from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('complete-profile/', views.CompleteProfileView.as_view(), name='complete_profile'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('student-home/', views.StudentHomeView.as_view(), name='student_home'),
    path('admin-home/', views.AdminHomeView.as_view(), name='admin_home'),
    path('advisor-home/', views.AdvisorHomeView.as_view(), name='advisor_home')
]