from django import forms
from .models import PortfolioItem


class PortfolioItemForm(forms.ModelForm):
    """Форма добавления/редактирования работы в портфолио"""
    
    class Meta:
        model = PortfolioItem
        fields = ('title', 'description', 'category')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название работы'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Описание работы'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
