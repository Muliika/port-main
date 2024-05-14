from django import forms
from .models import Comment


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'content')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'u-fullwidth'}),
            'email': forms.TextInput(attrs={'class': 'u-fullwidth'}),
            'content': forms.Textarea(attrs={'class': 'u-fullwidth'}),
        }