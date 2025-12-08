from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """Форма создания/редактирования отзыва"""
    
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} звезд') for i in range(1, 6)],
                attrs={'class': 'form-control'}
            ),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Ваш отзыв'}),
        }


class ExecutorResponseForm(forms.ModelForm):
    """Форма ответа исполнителя на отзыв"""
    
    class Meta:
        model = Review
        fields = ('executor_response',)
        widgets = {
            'executor_response': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ваш ответ'}),
        }
