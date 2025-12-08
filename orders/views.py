from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Order, Response, Category
from .forms import OrderForm, ResponseForm
from core.mixins import CustomerRequiredMixin, ExecutorRequiredMixin
from core.utils import create_notification


class OrderListView(ListView):
    """Список всех заказов с фильтрацией"""
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Order.objects.filter(status='active').select_related('customer', 'category')
        
        # Поиск по ключевым словам
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        
        # Фильтр по категории
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Фильтр по бюджету
        budget_min = self.request.GET.get('budget_min')
        budget_max = self.request.GET.get('budget_max')
        if budget_min:
            queryset = queryset.filter(budget_max__gte=budget_min)
        if budget_max:
            queryset = queryset.filter(budget_min__lte=budget_max)
        
        # Сортировка
        sort = self.request.GET.get('sort', '-created_at')
        queryset = queryset.order_by(sort)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class MyOrdersView(LoginRequiredMixin, CustomerRequiredMixin, ListView):
    """Список заказов текущего пользователя"""
    model = Order
    template_name = 'orders/my_orders.html'
    context_object_name = 'orders'
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).exclude(status='deleted')


class OrderDetailView(DetailView):
    """Детальная информация о заказе"""
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responses'] = self.object.responses.select_related('executor').all()
        return context


class OrderCreateView(LoginRequiredMixin, CustomerRequiredMixin, CreateView):
    """Создание нового заказа"""
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('orders:my_orders')
    
    def form_valid(self, form):
        form.instance.customer = self.request.user
        messages.success(self.request, 'Заказ успешно создан!')
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование заказа"""
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    
    def get_success_url(self):
        return reverse_lazy('orders:order_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Заказ успешно обновлен!')
        return super().form_valid(form)


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление заказа (мягкое удаление)"""
    model = Order
    success_url = reverse_lazy('orders:my_orders')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.status = 'deleted'
        self.object.save()
        messages.success(request, 'Заказ удален')
        return redirect(self.success_url)


class ResponseCreateView(LoginRequiredMixin, ExecutorRequiredMixin, CreateView):
    """Создание отклика на заказ"""
    model = Response
    form_class = ResponseForm
    template_name = 'orders/response_form.html'
    
    def form_valid(self, form):
        order = get_object_or_404(Order, pk=self.kwargs['pk'])
        form.instance.order = order
        form.instance.executor = self.request.user
        
        # Создаем уведомление для заказчика
        create_notification(
            user=order.customer,
            notification_type='response',
            title='Новый отклик на ваш заказ',
            message=f'{self.request.user.username} откликнулся на заказ "{order.title}"',
            related_object_id=order.id
        )
        
        messages.success(self.request, 'Отклик отправлен!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('orders:order_detail', kwargs={'pk': self.kwargs['pk']})


@login_required
def response_accept(request, pk):
    """Принятие отклика"""
    response = get_object_or_404(Response, pk=pk)
    
    if request.user != response.order.customer:
        messages.error(request, 'У вас нет прав для этого действия')
        return redirect('orders:order_detail', pk=response.order.pk)
    
    response.status = 'accepted'
    response.save()
    
    response.order.status = 'in_progress'
    response.order.save()
    
    # Уведомление исполнителю
    create_notification(
        user=response.executor,
        notification_type='response_accepted',
        title='Ваш отклик принят',
        message=f'Заказчик принял ваш отклик на заказ "{response.order.title}"',
        related_object_id=response.order.id
    )
    
    messages.success(request, 'Отклик принят')
    return redirect('orders:order_detail', pk=response.order.pk)


@login_required
def response_reject(request, pk):
    """Отклонение отклика"""
    response = get_object_or_404(Response, pk=pk)
    
    if request.user != response.order.customer:
        messages.error(request, 'У вас нет прав для этого действия')
        return redirect('orders:order_detail', pk=response.order.pk)
    
    response.status = 'rejected'
    response.save()
    
    # Уведомление исполнителю
    create_notification(
        user=response.executor,
        notification_type='response_rejected',
        title='Ваш отклик отклонен',
        message=f'Заказчик отклонил ваш отклик на заказ "{response.order.title}"',
        related_object_id=response.order.id
    )
    
    messages.info(request, 'Отклик отклонен')
    return redirect('orders:order_detail', pk=response.order.pk)
