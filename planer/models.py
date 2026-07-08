from django.db import models
from users.models import UserRelationship


class Topic(models.Model):

    LESSON_CHOICES = [
        ('bio', 'زیست'),
        ('dynamic', 'فیزیک'),
        ('math', 'ریاضی'),
        ('chemistry', 'شیمی'),
    ]
    FIELD_CHOICES = [
        ('general', 'نهم'),
        ('experimental', 'تجربی'),
        ('mathematical', 'ریاضی'),
        ('humanities', 'انسانی'),
    ]

    SEASON_CHOICES = [
        ('1', 'فصل اول'),
        ('2', 'فصل دوم'),
        ('3', 'فصل سوم'),
        ('4', 'فصل چهارم'),
        ('5', 'فصل پنجم'),
        ('6', 'فصل ششم'),
        ('7', 'فصل هفتم'),
        ('8', 'فصل هشتم'),
        ('9', 'فصل نهم'),
        ('10', 'فصل دهم'),
        ('base', 'هندسه پایه'),
        ('tahlil', 'هندسه تحلیلی')
    ]

    ADDRESS_CHOICES = [
        ('10th', 'دهم'),
        ('11th', 'یازدهم'),
        ('12th', 'دوازدهم'),
        ('problem', 'مسائل'),
        ('function', 'تابع'),
        ('grade2', 'معادله و تابع درجه دو'),
        ('equation', 'معادله و نا معادله'),
        ('bro', 'قدر مطلق و براکت'),
        ('logarithm', 'تابع نمایی و لگاریتمی'),
        ('triangles', 'مثلثات'),
        ('had', 'حد و پیوستگی'),
        ('moshtaba', 'مشتق'),
        ('usemoshtaba', 'کاربرد مشتق'),
        ('olgoo', 'مجموعه،الگو و دنباله'),
        ('tavan', 'توان گویا و عبارت جبری'),
        ('geometry', 'هندسه'),
        ('amar', 'امار'),
        ('shomaresh', 'شمارش بدون شمردن'),
        ('probability', 'احتمال')
    ]

    title = models.CharField(max_length=200, default='', verbose_name= 'نام مبحث', blank=True )

    lesson = models.CharField(
        max_length=20,
        choices=LESSON_CHOICES,
        blank=True,
        null=True,
        verbose_name='درس'
    )
    field = models.CharField(
        max_length=20,
        choices=FIELD_CHOICES,
        blank=True,
        null=True,
        verbose_name='رشته'
    )
    address = models.CharField(
        max_length=20,
        choices=ADDRESS_CHOICES,
        blank=True,
        null=True,
        verbose_name='آدرس'
    )
    season = models.CharField(
        max_length=20,
        choices=SEASON_CHOICES,
        blank=True,
        null=True,
        verbose_name='فصل'
    )

    def __str__(self):
        return self.title


class Plan(models.Model):
    relation = models.ForeignKey(UserRelationship, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic)
    start = models.DateField()
    days = models.IntegerField()

    def __str__(self):
        return self.relation.student.first_name + " " + self.relation.student.last_name


class Tasks(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField()
    title = models.CharField(max_length=200)
    time = models.IntegerField(default=0)
    is_done = models.BooleanField(default=False)
