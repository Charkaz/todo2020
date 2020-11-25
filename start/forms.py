from django import forms

class registerForm(forms.Form):
    Adi             = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    Soyadi          = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    Istifadeciadi   = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    email           = forms.EmailField(max_length=150,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    password        = forms.CharField(max_length=150,required=True,widget=forms.PasswordInput(attrs={'class':'form-control'}))


class loginForm(forms.Form):
    istifadeci_adi  = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class':'form-control','style':'border-radius:10px'}))
    sifre           = forms.CharField(max_length=150,required=True,widget=forms.PasswordInput(attrs={'class':'form-control','style':'border-radius:10px'}))

class ActivationForm(forms.Form):
    code            = forms.CharField(max_length=10,required=True,widget=forms.TextInput(attrs={'class':'form-control','style':'border-radius:20px'}))