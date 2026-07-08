from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView, TemplateView
from django.http import JsonResponse
from django.db.models import Q
from .models import Topic, Plan, Tasks
from users.models import UserRelationship
import json


class StudentPlaningView(LoginRequiredMixin, TemplateView):
    template_name = 'planer/student_planing.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # دریافت relationship دانش‌آموز
        try:
            relationship = user.as_student
            context['relationship'] = relationship
        except UserRelationship.DoesNotExist:
            relationship = None
        
        # تمام درس‌های منحصر به فرد
        lessons = Topic.objects.filter(field=user.field).values_list('lesson', flat=True).distinct()
        context['lessons'] = [(lesson, dict(Topic.LESSON_CHOICES).get(lesson, lesson)) for lesson in lessons]
        
        # تمام آدرس‌های منحصر به فرد
        addresses = Topic.objects.filter(field=user.field).values_list('address', flat=True).distinct()
        context['addresses'] = [(address, dict(Topic.ADDRESS_CHOICES).get(address, address)) for address in addresses]
        
        # تمام فصل‌های منحصر به فرد
        seasons = Topic.objects.filter(field=user.field).values_list('season', flat=True).distinct()
        context['seasons'] = [(season, dict(Topic.SEASON_CHOICES).get(season, season)) for season in seasons]
        
        return context

    def get(self, request, *args, **kwargs):
        if request.user.user_type != 'student':
            return redirect('home')
        if not request.user.profile_completed:
            return redirect('complete_profile')
        return super().get(request, *args, **kwargs)


class GetTopicsAPIView(LoginRequiredMixin, View):
    """API برای دریافت topics بر اساس lesson و address"""
    
    def get(self, request):
        user = request.user
        lesson = request.GET.get('lesson')
        address = request.GET.get('address')
        
        # فیلتر topics بر اساس field، lesson و address
        topics = Topic.objects.filter(
            field=user.field,
            lesson=lesson,
            address=address
        ).values('id', 'title', 'season')
        
        # گروه‌بندی بر اساس season
        grouped_topics = {}
        for topic in topics:
            season = topic['season']
            season_name = dict(Topic.SEASON_CHOICES).get(season, season)
            
            if season_name not in grouped_topics:
                grouped_topics[season_name] = []
            
            grouped_topics[season_name].append({
                'id': topic['id'],
                'title': topic['title']
            })
        
        return JsonResponse({'topics': grouped_topics})


class CreatePlanView(LoginRequiredMixin, View):
    """ایجاد Plan با topics انتخاب‌شده"""
    
    def post(self, request):
        user = request.user
        
        if user.user_type != 'student':
            return JsonResponse({'error': 'تنها دانش‌آموزان می‌توانند برنامه ایجاد کنند'}, status=403)
        
        try:
            relationship = user.as_student
        except UserRelationship.DoesNotExist:
            return JsonResponse({'error': 'ارتباط دانش‌آموز یافت نشد'}, status=404)
        
        try:
            data = json.loads(request.body)
            selected_topic_ids = data.get('topic_ids', [])
            
            if not selected_topic_ids:
                return JsonResponse({'error': 'هیچ موضوعی انتخاب نشده است'}, status=400)
            
            # ایجاد Plan
            plan = Plan.objects.create(
                relation=relationship,
                start=None,
                days=None
            )
            
            # اضافه کردن topics انتخاب‌شده به Plan
            selected_topics = Topic.objects.filter(id__in=selected_topic_ids, field=user.field)
            plan.topics.set(selected_topics)
            
            return JsonResponse({
                'success': True,
                'message': 'برنامه با موفقیت ایجاد شد!',
                'plan_id': plan.id
            })
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'داده ارسالی نامعتبر است'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
