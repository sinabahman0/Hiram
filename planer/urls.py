from django.urls import path
from . import views

urlpatterns = [
    path('planing/', views.StudentPlaningView.as_view(), name='student_planing'),
    path('api/get-topics/', views.GetTopicsAPIView.as_view(), name='get_topics'),
    path('api/create-plan/', views.CreatePlanView.as_view(), name='create_plan'),
    path('plan/', views.StudentPlaningView.as_view(), name='student_plan'),
    path('progress/', views.StudentPlaningView.as_view(), name='student_progress'),
    path('call/', views.StudentPlaningView.as_view(), name='student_call')
]
