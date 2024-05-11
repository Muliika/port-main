from django import forms
from .models import Comment
from mptt.forms import TreeNodeChoiceField


class NewCommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = Comment
        fields = ('name', 'parent', 'email', 'content')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'u-fullwidth h-remove-bottom'}),
            'email': forms.TextInput(attrs={'class': 'u-fullwidth h-remove-bottom'}),
            'content': forms.Textarea(attrs={'class': 'u-fullwidth'}),
        }

    def save(self, *args, **kwargs):
        Comment.objects.rebuild()
        return super(NewCommentForm, self).save(*args, **kwargs)