from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import CustomUser, Profile, ExecutorProfile
from .forms import RegistrationForm, LoginForm, ProfileForm, ExecutorProfileForm


class RegisterView(CreateView):
    """
    Представление для регистрации нового пользователя
    """
    model = CustomUser
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Регистрация прошла успешно! Теперь вы можете войти.')
        # TODO: Отправка email подтверждения
        return response


def login_view(request):
    """
    Представление для входа в систему
    """
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    Представление для выхода из системы
    """
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('home')


class ProfileView(LoginRequiredMixin, DetailView):
    """
    Представление для просмотра профиля
    """
    model = CustomUser
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования профиля
    """
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user.profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.user_type == 'executor':
            if self.request.POST:
                context['executor_form'] = ExecutorProfileForm(
                    self.request.POST,
                    instance=self.request.user.executor_profile
                )
            else:
                context['executor_form'] = ExecutorProfileForm(
                    instance=self.request.user.executor_profile
                )
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.user_type == 'executor':
            executor_form = ExecutorProfileForm(
                self.request.POST,
                instance=self.request.user.executor_profile
            )
            if executor_form.is_valid():
                executor_form.save()
        messages.success(self.request, 'Профиль успешно обновлен!')
        return response
