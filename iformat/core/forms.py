from django import forms


class Contact_form(forms.Form):
    contact_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control form-control-plain', 'placeholder': 'Nome Completo'}))
    contact_email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control form-control-plain', 'placeholder': 'email@exemplo.com'}))
    subject = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control form-control-plain', 'placeholder': 'Assunto'}))
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control form-control-plain', 'placeholder': 'Coloque sua mensagem aqui...', 'rows': 8}))
