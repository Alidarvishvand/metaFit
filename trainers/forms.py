from django import forms
from .models import TrainerComment, TrainerRating


class TrainerCommentForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(str(i), f'{i} ستاره') for i in range(1, 6)],
        widget=forms.RadioSelect(),
        label="امتیاز",
        required=True
    )
    
    class Meta:
        model = TrainerComment
        fields = ['name', 'email', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'نام شما'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'ایمیل (اختیاری)'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'نظر خود را بنویسید...',
                'rows': 5
            }),
        }
        labels = {
            'name': 'نام',
            'email': 'ایمیل',
            'comment': 'نظر',
        }


