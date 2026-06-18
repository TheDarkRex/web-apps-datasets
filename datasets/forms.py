from django import forms
from .models import Dataset, Query, Answer


class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['name', 'author', 'topic', 'size_class', 'table_count', 'link', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'size_class': forms.Select(attrs={'class': 'form-select'}),
            'table_count': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'link': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Masz pytanie do tego zbioru danych? Napisz je tutaj...'
            }),
        }
        labels = {'content': ''}

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control form-control-sm',
                'rows': 2,
                'placeholder': 'Napisz odpowiedź...'
            }),
        }
        labels = {'content': ''}