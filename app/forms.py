from django import forms
from .models import todo

class TodoForm(forms.Form):
    basliq        = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    aciqlama      = forms.CharField(max_length=150,required=True,widget=forms.Textarea(attrs={'class':'form-control'}))
    son_tarix     = forms.DateTimeField(required=True,widget=forms.TextInput(attrs={'type':'datetime-local','class':'form-control'}))


class serhupdateForm(forms.Form):
    metin         = forms.CharField(max_length=300,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
