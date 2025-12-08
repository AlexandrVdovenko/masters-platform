from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Profile, ExecutorProfile


class RegistrationForm(UserCreationForm):
    """
    Форма регистрации нового пользователя
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    user_type = forms.ChoiceField(
        choices=CustomUser.USER_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Подтверждение пароля'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return email


class LoginForm(AuthenticationForm):
    """
    Форма входа в систему
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )


class ProfileForm(forms.ModelForm):
    """
    Форма редактирования профиля
    """
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio', 'city')
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Расскажите о себе'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Москва'}),
        }
    
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError('Размер файла не должен превышать 5MB')
            if avatar.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
                raise ValidationError('Допустимые форматы: JPEG, PNG, GIF')
        return avatar


class ExecutorProfileForm(forms.ModelForm):
    """
    Форма редактирования профиля исполнителя
    """
    class Meta:
        model = ExecutorProfile
        fields = ('experience_years', 'hourly_rate')
        widgets = {
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.01'}),
        }
