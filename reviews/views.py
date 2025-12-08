from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from accounts.models import CustomUser
from orders.models import Order
from .models import Review
from .forms import ReviewForm, ExecutorResponseForm
from core.utils import create_notification


class ReviewListView(ListView):
    """Список отзывов исполнителя"""
    model = Review
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'
    
    def get_queryset(self):
        executor = get_object_or_404(CustomUser, pk=self.kwargs['executor_id'])
        return Review.objects.filter(executor=executor).select_related('customer', 'order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['executor'] = get_object_or_404(CustomUser, pk=self.kwargs['executor_id'])
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """Создание отзыва"""
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'
    
    def form_valid(self, form):
        order = get_object_or_404(Order, pk=self.kwargs['order_id'])
        
        if order.customer != self.request.user:
            messages.error(self.request, 'Вы не можете оставить отзыв на этот заказ')
            return redirect('orders:order_detail', pk=order.pk)
        
        form.instance.order = order
        form.instance.customer = self.request.user
        form.instance.executor = order.responses.filter(status='accepted').first().executor
        
        # Создаем уведомление для исполнителя
        create_notification(
            user=form.instance.executor,
            notification_type='review',
            title='Новый отзыв',
            message=f'{self.request.user.username} оставил отзыв о вашей работе',
            related_object_id=order.id
        )
        
        messages.success(self.request, 'Отзыв успешно добавлен!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('reviews:review_list', kwargs={'executor_id': self.object.executor.id})


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование отзыва"""
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Отзыв обновлен!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('reviews:review_list', kwargs={'executor_id': self.object.executor.id})


@login_required
def executor_respond(request, pk):
    """Ответ исполнителя на отзыв"""
    review = get_object_or_404(Review, pk=pk)
    
    if request.user != review.executor:
        messages.error(request, 'У вас нет прав для этого действия')
        return redirect('reviews:review_list', executor_id=review.executor.id)
    
    if request.method == 'POST':
        form = ExecutorResponseForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ответ добавлен!')
            return redirect('reviews:review_list', executor_id=review.executor.id)
    else:
        form = ExecutorResponseForm(instance=review)
    
    return render(request, 'reviews/executor_response_form.html', {'form': form, 'review': review})
