from django import forms
from .models import Comment, Reply


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_content"]
        widgets = {'comment_content': forms.TextInput(
            attrs={'class': 'form-control'})}


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["reply_content"]
        widgets = {'reply_content': forms.TextInput(
            attrs={'class': 'form-control'})}


class UpdateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_content"]
        widgets = {'comment_content': forms.TextInput(
            attrs={'class': 'form-control'})}


class UpdateReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["reply_content"]
        widgets = {'reply_content': forms.TextInput(
            attrs={'class': 'form-control'})}
