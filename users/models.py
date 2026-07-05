from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('advisor', 'مشاور'),
        ('admin', 'ادمین'),
        ('student', 'دانش‌اموز'),
    ]

    GRADE_CHOICES = [
        ('9', 'نهم'),
        ('10', 'دهم'),
        ('11', 'یازدهم'),
        ('12', 'دوازدهم'),
    ]

    FIELD_CHOICES = [
        ('general', 'نهم'),
        ('experimental', 'تجربی'),
        ('mathematical', 'ریاضی'),
        ('humanities', 'انسانی'),
    ]

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='student'
    )

    is_active = models.BooleanField(default=True)

    # فیلدهای پروفایل
    phone_number = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        verbose_name='شماره همراه'
    )

    grade = models.CharField(
        max_length=2,
        choices=GRADE_CHOICES,
        blank=True,
        null=True,
        verbose_name='پایه'
    )

    field = models.CharField(
        max_length=20,
        choices=FIELD_CHOICES,
        blank=True,
        null=True,
        verbose_name='رشته'
    )

    profile_completed = models.BooleanField(
        default=False,
        verbose_name='پروفایل تکمیل شده'
    )
    if user_type == 'student' :
        def __str__(self):
            return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'


class UserRelationship(models.Model):
    student = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='as_student',
        limit_choices_to={'user_type': 'student'}
    )
    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='students_under_admin',
        limit_choices_to={'user_type': 'admin'}
    )
    advisor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='students_under_advisor',
        limit_choices_to={'user_type': 'advisor'}
    )

    num_test = {}
    term = {}

    def __str__(self):
        return (self.student.first_name + " " + self.student.last_name)

    class Meta:
        unique_together = ['student', 'admin', 'advisor']