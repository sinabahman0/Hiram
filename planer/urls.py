from django.urls import path
from . import views

urlpatterns = [
    path('planing/', views.StudentPlaningView.as_view(), name='student_planing'),
    path('plan/', views.StudentPlaningView.as_view(), name='student_plan'),
    path('progress/', views.StudentPlaningView.as_view(), name='student_progress'),
    path('call/', views.StudentPlaningView.as_view(), name='student_call')
]