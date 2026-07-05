from django.db import models
from users.models import UserRelationship


class Topic(models.Model):

    LESSON_CHOICES = [
        ('general', 'زیست'),
        ('experimental', 'فیزیک'),
        ('mathematical', 'ریاضی'),
        ('humanities', 'شیمی'),
    ]
    FIELD_CHOICES = [
        ('general', 'نهم'),
        ('experimental', 'تجربی'),
        ('mathematical', 'ریاضی'),
        ('humanities', 'انسانی'),
    ]

    title = models.CharField(max_length=200, default='', verbose_name='نام مبحث')
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

