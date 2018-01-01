from django.contrib.auth import login
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.utils.translation import ugettext as _
from artifacts.forms import ArtifactForm, UserArtifactForm, ArtifactImageFormSet, OriginAreaForm, ArtifactMaterialForm, \
    UserForm, ArtifactImagesForm
from artifacts.models import Artifact, ArtifactStatus, ArtifactImage, PageBanner, OriginArea, ArtifactMaterial
from jewishdiaspora.base_views import JewishDiasporaUIMixin
from users.models import User


class PersonalInformationRegistrationPage(JewishDiasporaUIMixin, TemplateView):
    template_name = 'artifacts/sign_in_first_page.html'


class ArtifactInformationRegistrationPage(JewishDiasporaUIMixin, TemplateView):
    template_name = 'artifacts/sign_in_second_page.html'


class ArtifactsImagesRegistrationPage(JewishDiasporaUIMixin, TemplateView):
    template_name = 'artifacts/sign_in_third_page.html'


class UserArtifactInformationPage(JewishDiasporaUIMixin, DetailView):
    template_name = 'artifacts/user_artifact_information.html'
    model = Artifact
    context_object_name = 'artifact'
    page_title = _('Artifact detail')
    page_name = 'artifact_detail'


class TheNewForm(JewishDiasporaUIMixin, TemplateView):
    template_name = 'artifacts/artifacts_donor_registration.html'


class HomeView(JewishDiasporaUIMixin, ListView):
    template_name = 'artifacts/home.html'
    page_title = _('Home')
    page_name = 'home'
    model = Artifact
    context_object_name = 'artifacts'

    def get_queryset(self):
        return super(HomeView, self).get_queryset().filter(status=ArtifactStatus.APPROVED, is_private=False)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['bigs'] = [1, 6, 7, 12, 13, 18, 19, 24, 25, 30, 31, 36, 37, 42, 43, 48, 49]
        context['page_banner'] = PageBanner.objects.filter(active=True, page='museum_collections').order_by('?').first()
        return context


class AboutView(JewishDiasporaUIMixin, TemplateView):
    template_name = 'artifacts/about.html'
    page_title = _('About')
    page_name = 'about'


class ArtifactUsersListView(JewishDiasporaUIMixin, ListView):
    template_name = 'artifacts/users_artifact_list.html'
    model = Artifact
    context_object_name = 'artifacts'
    page_title = _('Users artifacts list')
    page_name = 'users_artifact_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return super(ArtifactUsersListView, self).get_queryset().filter(is_private=True)

        return super(ArtifactUsersListView, self).get_queryset().filter(status=ArtifactStatus.APPROVED, is_private=True)


class ArtifactFullListView(JewishDiasporaUIMixin, ListView):
    template_name = 'artifacts/artifact_full_list.html'
    model = Artifact
    context_object_name = 'artifacts'
    page_title = _('All artifacts list')
    page_name = 'all_artifact_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return super(ArtifactFullListView, self).get_queryset()

        return super(ArtifactFullListView, self).get_queryset().filter(status=ArtifactStatus.APPROVED)


class ArtifactDetailView(JewishDiasporaUIMixin, DetailView):
    model = Artifact
    context_object_name = 'artifact'
    page_title = _('Artifact detail')
    page_name = 'artifact_detail'

    def get_template_names(self):
        if self.object.is_private:
            return 'artifacts/user_artifact_detail.html'
        return 'artifacts/artifact_detail.html'


class ArtifactCreateStepOneView(JewishDiasporaUIMixin, FormView):
    template_name = 'artifacts/artifact_create_step_one.html'
    form_class = UserForm
    success_url = reverse_lazy('artifacts:create_step_two')
    page_title = _('Artifact create')
    page_name = 'artifact_create'

    def get_initial(self):
        if self.request.user.is_authenticated:
            return {
                'name': self.request.user.full_name,
                'email': self.request.user.email,
                'phone_number': self.request.user.phone,
            }

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        phone = form.cleaned_data.get('phone_number')

        if not self.request.user.is_authenticated:
            password = User.objects.make_random_password()
            user = User.objects.create_user(
                email=email,
                password=password,
                full_name=name,
                phone=phone
            )
            # Send email
            user.send_registration_email(password)
            # Login user into session
            login(self.request, user)

        return super().form_valid(form)


class ArtifactCreateStepTwoView(JewishDiasporaUIMixin, CreateView):
    template_name = 'artifacts/artifact_create_step_two.html'
    model = Artifact
    page_title = _('Artifact detail')
    page_name = 'artifact_detail'
    form_description = _('Some Artifact Description')

    def get_initial(self):
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            return {
                'donor_name_he': self.request.user.full_name,
                'donor_name_en': self.request.user.full_name,
            }

    def get_form_class(self):
        if self.request.user.is_superuser:
            return ArtifactForm

        return UserArtifactForm

    def get_success_url(self):
        return reverse('artifacts:create_step_three', args=[self.object.id])

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.is_private = True
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)


class ArtifactCreateStepThreeView(JewishDiasporaUIMixin, FormView):
    template_name = 'artifacts/artifact_create_step_three.html'
    form_class = ArtifactImagesForm
    page_title = _('Artifact Images')
    page_name = 'artifact_images'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        context = self.get_context_data()
        artifact_image_formset = context['artifact_image_formset']

        if artifact_image_formset.is_valid():
            artifact = Artifact.objects.get(pk=self.kwargs['pk'])
            artifact_image_formset.instance = artifact
            artifact_image_formset.save()
            return super().form_valid(form)

        return self.render_to_response(
            self.get_context_data(
                form=form,
                artifact_image_formset=artifact_image_formset
            )
        )
        # return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['artifact_image_formset'] = ArtifactImageFormSet(self.request.POST, self.request.FILES,
                                                                     prefix='artifact_image_formset')
        else:
            context['artifact_image_formset'] = ArtifactImageFormSet(prefix='artifact_image_formset')
        return context


class OriginAreaCreateView(JewishDiasporaUIMixin, CreateView):
    template_name = 'artifacts/origin_area_create.html'
    model = OriginArea
    form_class = OriginAreaForm
    success_url = reverse_lazy('artifacts:origin_area_list')
    page_title = _('Origin area create')
    page_name = 'origin_area_create'


class OriginAreaUpdateView(JewishDiasporaUIMixin, UpdateView):
    template_name = 'artifacts/origin_area_create.html'
    model = OriginArea
    form_class = OriginAreaForm
    success_url = reverse_lazy('artifacts:origin_area_list')
    page_title = _('Origin area update')
    page_name = 'origin_area_update'


class OriginAreaListView(JewishDiasporaUIMixin, ListView):
    template_name = 'artifacts/origin_area_list.html'
    model = OriginArea
    context_object_name = 'areas'
    page_title = _('Origin area list')
    page_name = 'origin_area_list'


class ArtifactMaterialCreateView(JewishDiasporaUIMixin, CreateView):
    template_name = 'artifacts/artifact_material.html'
    model = ArtifactMaterial
    form_class = ArtifactMaterialForm
    success_url = reverse_lazy('artifacts:material_list')
    page_title = _('Artifact material create')
    page_name = 'artifact_material_create'


class ArtifactMaterialUpdateView(JewishDiasporaUIMixin, UpdateView):
    template_name = 'artifacts/artifact_material.html'
    model = ArtifactMaterial
    form_class = ArtifactMaterialForm
    success_url = reverse_lazy('artifacts:material_list')
    page_title = _('Artifact material update')
    page_name = 'artifact_material_update'


class ArtifactMaterialDeleteView(JewishDiasporaUIMixin, DeleteView):
    template_name = 'artifacts/artifact_material_delete.html'
    model = ArtifactMaterial
    form_class = ArtifactMaterialForm
    success_url = reverse_lazy('artifacts:material_list')
    page_title = _('Origin area update')
    page_name = 'origin_area_update'


class ArtifactMaterialListView(JewishDiasporaUIMixin, ListView):
    template_name = 'artifacts/artifact_material_list.html'
    model = ArtifactMaterial
    context_object_name = 'materials'


class ArtifactImageCreateView(JewishDiasporaUIMixin, CreateView):
    template_name = 'artifacts/artifact_create_step_one.html'
    model = ArtifactImage
    success_url = reverse_lazy('artifacts:list')
    page_title = _('Artifact image create')
    page_name = 'artifact_image_create'
    fields = '__all__'




