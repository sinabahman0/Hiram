from django import forms
from django.contrib.auth import authenticate
from .models import User


class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور را وارد کنید'
        })
    )
    password_confirm = forms.CharField(
        label='تأیید رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور را دوباره وارد کنید'
        })
    )

    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام کاربری'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('رمز‌های عبور مطابقت ندارند!')

        if password and len(password) < 6:
            raise forms.ValidationError('رمز عبور باید حداقل 6 کاراکتر باشد!')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = True
        user.user_type = 'student'
        user.profile_completed = False

        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        label='نام کاربری',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام کاربری'
        })
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                # بررسی کن آیا کاربر وجود دارد ولی غیرفعال است
                try:
                    user = User.objects.get(username=username)
                    if not user.is_active:
                        raise forms.ValidationError('اکانت شما هنوز فعال نشده است!')
                    else:
                        raise forms.ValidationError('نام کاربری یا رمز عبور نادرست است!')
                except User.DoesNotExist:
                    raise forms.ValidationError('نام کاربری یا رمز عبور نادرست است!')

        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)


class CompleteProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'grade', 'field']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خانوادگی',
                'required': True
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '09xxxxxxxxx',
                'pattern': '[0-9]{11}',
                'required': True
            }),
            'grade': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'field': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name or first_name.strip() == '':
            raise forms.ValidationError('نام الزامی است!')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name or last_name.strip() == '':
            raise forms.ValidationError('نام خانوادگی الزامی است!')
        return last_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number or phone_number.strip() == '':
            raise forms.ValidationError('شماره همراه الزامی است!')
        if len(phone_number) != 11 or not phone_number.isdigit():
            raise forms.ValidationError('شماره همراه باید 11 رقم باشد!')
        if not phone_number.startswith('09'):
            raise forms.ValidationError('شماره همراه باید با 09 شروع شود!')
        return phone_number

    def clean_grade(self):
        grade = self.cleaned_data.get('grade')
        if not grade:
            raise forms.ValidationError('پایه الزامی است!')
        return grade

    def clean_field(self):
        field = self.cleaned_data.get('field')
        if not field:
            raise forms.ValidationError('رشته الزامی است!')
        return field

    def save(self, commit=True):
        user = super().save(commit=False)
        user.profile_completed = True
        if commit:
            user.save()
        return user
