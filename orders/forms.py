from django import forms
from .models import Order, Response


class OrderForm(forms.ModelForm):
    """Форма создания/редактирования заказа"""
    
    class Meta:
        model = Order
        fields = ('category', 'title', 'description', 'budget_min', 'budget_max')
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название заказа'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Подробное описание'}),
            'budget_min': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.01'}),
            'budget_max': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.01'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        budget_min = cleaned_data.get('budget_min')
        budget_max = cleaned_data.get('budget_max')
        
        if budget_min and budget_max and budget_min > budget_max:
            raise forms.ValidationError('Минимальный бюджет не может быть больше максимального')
        
        return cleaned_data


class ResponseForm(forms.ModelForm):
    """Форма создания отклика"""
    
    class Meta:
        model = Response
        fields = ('message', 'proposed_price')
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Ваше предложение'}),
            'proposed_price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.01', 'placeholder': 'Предложенная цена'}),
        }
