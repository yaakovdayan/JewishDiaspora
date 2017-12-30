from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.utils.translation import ugettext as _
from jewishdiaspora.base_views import JewishDiasporaUIMixin
from users.forms import ContactForm, UserForm
from users.models import ArtifactContact
from django.contrib.auth.models import User
from django import forms

class UserFormView(View):
    form_class = UserForm
    template_name = 'users/registration.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit = False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()

            user = authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return  redirect('jewishdiaspora:home')

        return render(request, self.template_name, {'form': form})



class ContactView(JewishDiasporaUIMixin, SuccessMessageMixin, CreateView):
    template_name = 'users/contact_form.html'
    model = ArtifactContact
    success_url = reverse_lazy('contact')
    page_title = _('Contact us')
    page_name = 'contact_us'
    form_class = ContactForm
    success_message = _('Thank you, we will contact you shortly')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)
