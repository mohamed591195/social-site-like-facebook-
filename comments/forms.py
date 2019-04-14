from django import forms
from .models import Comment

class CommentForm(forms.Form):
    comment = forms.CharField()
    
    