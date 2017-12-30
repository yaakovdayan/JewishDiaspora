from django import forms
from django.core.mail import send_mail
from django.utils.translation import ugettext as _

from .models import ArtifactContact
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        module = User
        fields = ['username', 'email', 'password']



class ContactForm(forms.ModelForm):
    class Meta:
        model = ArtifactContact
        exclude = ['submitted_at', ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'artifact_info': forms.Textarea(attrs={'class': 'form-control'}),
            'intend_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def send_email(self):
        data = self.cleaned_data

        return send_mail(
            _('Artifact contact form'),
            f'Name: {data["name"]}\n'
            f'Email: {data["email"]}\n'
            f'Phone: {data["phone"]}\n'
            f'Artifact info: {data["artifact_info"]}\n'
            f'Intend to: {data["intend_type"]}',
            data['email'],
            ['yanivmirel@gmail.com'],
            fail_silently=False,
        )
