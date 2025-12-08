from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from accounts.models import CustomUser
from .models import PortfolioItem
from .forms import PortfolioItemForm
from core.mixins import ExecutorRequiredMixin


class PortfolioListView(ListView):
    """Список работ в портфолио исполнителя"""
    model = PortfolioItem
    template_name = 'portfolio/portfolio_list.html'
    context_object_name = 'portfolio_items'
    
    def get_queryset(self):
        user = get_object_or_404(CustomUser, pk=self.kwargs['user_id'])
        return PortfolioItem.objects.filter(executor=user).prefetch_related('images')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['executor'] = get_object_or_404(CustomUser, pk=self.kwargs['user_id'])
        return context


class PortfolioCreateView(LoginRequiredMixin, ExecutorRequiredMixin, CreateView):
    """Добавление работы в портфолио"""
    model = PortfolioItem
    form_class = PortfolioItemForm
    template_name = 'portfolio/portfolio_form.html'
    
    def form_valid(self, form):
        form.instance.executor = self.request.user
        messages.success(self.request, 'Работа добавлена в портфолио!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('portfolio:portfolio_list', kwargs={'user_id': self.request.user.id})


class PortfolioUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование работы в портфолио"""
    model = PortfolioItem
    form_class = PortfolioItemForm
    template_name = 'portfolio/portfolio_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Работа обновлена!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('portfolio:portfolio_list', kwargs={'user_id': self.request.user.id})


class PortfolioDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление работы из портфолио"""
    model = PortfolioItem
    
    def get_success_url(self):
        return reverse_lazy('portfolio:portfolio_list', kwargs={'user_id': self.request.user.id})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Работа удалена из портфолио')
        return super().delete(request, *args, **kwargs)
