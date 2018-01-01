from django.conf import settings
from django.utils.translation import ugettext as _
from django.db import models
from django_countries.fields import CountryField


class ArtifactStatus(object):
    PENDING = 1
    MISSING = 2
    APPROVED = 3
    REJECTED = 4

    choices = (
        (PENDING, _('Pending approval')),
        (MISSING, _('Missing info')),
        (APPROVED, _('Approved')),
        (REJECTED, _('Rejected')),
    )


class Pages(object):
    MUSEUM_COLLECTIONS = 'museum_collections'
    USERS_COLLECTIONS = 'users_collections'
    ALL_COLLECTIONS = 'all_collections'
    ABOUT = 'about'
    CONTACT = 'contact'
    ACCOUNT = 'account'
    LOGIN = 'login'
    UPLOAD_STEP_1 = 'upload_step_1'
    UPLOAD_STEP_2 = 'upload_step_2'
    UPLOAD_STEP_3 = 'upload_step_3'

    choices = (
        (MUSEUM_COLLECTIONS, _('Museum collections')),
        (USERS_COLLECTIONS, _('Users collections')),
        (ALL_COLLECTIONS, _('All collections')),
        (ABOUT, _('About')),
        (CONTACT, _('Contact')),
        (ACCOUNT, _('Account')),
        (LOGIN, _('Login')),
        (UPLOAD_STEP_1, _('Upload step 1')),
        (UPLOAD_STEP_2, _('Upload step 2')),
        (UPLOAD_STEP_3, _('Upload step 3')),
    )


class ArtifactType(models.Model):
    title_he = models.CharField(_('Title hebrew'), max_length=250)
    title_en = models.CharField(_('Title english'), max_length=250)

    def __str__(self):
        return self.title_he if self.title_he else self.title_en


class ArtifactMaterial(models.Model):
    title_he = models.CharField(_('Title hebrew'), max_length=250)
    title_en = models.CharField(_('Title english'), max_length=250)

    def __str__(self):
        return self.title_he if self.title_he else self.title_en


class OriginArea(models.Model):
    title_he = models.CharField(_('Title hebrew'), max_length=250)
    title_en = models.CharField(_('Title english'), max_length=250)
    countries = CountryField(_('Country'), multiple=True, blank=True)

    def __str__(self):
        return self.title_he if self.title_he else self.title_en

    def get_countries_list(self):
        return [
            {
                'name': x.name,
                'code': x.code,
                'flag': x.flag
            } for x in self.countries
        ]


class Artifact(models.Model):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                    related_name='uploaded_artifacts', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    acceptance_date = models.DateTimeField(blank=True, null=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                    related_name='approved_artifacts', null=True, blank=True)
    artifact_type = models.ForeignKey(ArtifactType, verbose_name=_('Artifact type'), on_delete=models.SET_NULL,
                                      related_name='artifacts', null=True, blank=True)
    artifact_materials = models.ManyToManyField(ArtifactMaterial, verbose_name=_('Artifact material'),
                                                related_name='artifacts', blank=True)
    status = models.PositiveSmallIntegerField(_('Status'), choices=ArtifactStatus.choices,
                                              default=ArtifactStatus.PENDING)
    is_private = models.BooleanField(_('Privately owned artifact'), default=False)
    name_he = models.CharField(_('Name hebrew'), max_length=250)
    name_en = models.CharField(_('Name english'), max_length=250)
    slug = models.SlugField(_('Slug'), max_length=250, allow_unicode=True, blank=True, null=True)
    year_from = models.CharField(_('Year from'), max_length=200, blank=True, null=True)
    year_to = models.CharField(_('Year to'), max_length=200, blank=True, null=True)
    technical_data_he = models.TextField(_('Technical data hebrew'))
    technical_data_en = models.TextField(_('Technical data english'))
    description_he = models.TextField(_('Description hebrew'))
    description_en = models.TextField(_('Description english'))
    origin_city_he = models.CharField(_('City hebrew'), max_length=100, blank=True, null=True)
    origin_city_en = models.CharField(_('City english'), max_length=100, blank=True, null=True)
    origin_country = CountryField(_('Country'), blank=True, null=True)
    origin_area = models.ForeignKey(OriginArea, verbose_name=_('Area'), on_delete=models.SET_NULL, blank=True,
                                    null=True, related_name='artifacts')
    is_displayed = models.BooleanField(_('Displayed in museum?'), default=False)
    displayed_at = models.CharField(_('Artifact location in museum'), max_length=250, blank=True, null=True)
    donor_name_he = models.CharField(_('Donor name hebrew'), max_length=250, blank=True, null=True)
    donor_name_en = models.CharField(_('Donor name english'), max_length=250, blank=True, null=True)
    display_donor_name = models.BooleanField(_('Display donor name?'), default=False)

    def __str__(self):
        return self.name_he if self.name_he else self.name_en

    def get_years(self):
        if self.year_from:
            if self.year_to:
                if self.year_from == self.year_to:
                    return '{}-{}'.format(self.year_from, self.year_to)
            return self.year_from
        elif self.year_to:
            return self.year_to
        return None

    def get_all_tags(self):
        artifact_type = [self.artifact_type.title_he] if self.artifact_type else []
        artifact_materials = [x.title_he for x in self.artifact_materials.all()]
        return artifact_materials + artifact_type

    def get_cover_image(self):
        image = self.images.filter(is_cover=True).first()
        if image:
            return image.image
        # Fallback to not cover image
        image = self.images.filter(is_cover=False).first()
        if image:
            return image.image

        # return some default image instead
        return None

    def get_images(self):
        return self.images.all()

    def get_first_image(self):
        return self.get_images()[0]

    def get_rest_images(self):
        return self.get_images()[1:]

class ArtifactImage(models.Model):
    artifact = models.ForeignKey(Artifact, verbose_name=_('Artifact'), on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(_('Image'), upload_to='artifacts/')
    description = models.CharField(_('Description'), max_length=400, blank=True, null=True)
    credit_he = models.CharField(_('Credit hebrew'), max_length=200, blank=True, null=True)
    credit_en = models.CharField(_('Credit english'), max_length=200, blank=True, null=True)
    year_era = models.CharField(_('Year/Era'), max_length=200, blank=True, null=True)
    location = models.CharField(_('Image location'), max_length=200, blank=True, null=True)
    is_cover = models.BooleanField(_('Cover image?'), default=False)

    def __str__(self):
        return f'[{self.id}] {self.artifact.name}'


class ArtifactImageCoord(models.Model):
    image = models.ForeignKey(ArtifactImage, verbose_name=_('Image'), on_delete=models.CASCADE, related_name='coords')
    x = models.CharField(_('X'), max_length=10)
    y = models.CharField(_('Y'), max_length=10)
    width = models.CharField(_('Width'), max_length=10, blank=True, null=True)
    height = models.CharField(_('Height'), max_length=10, blank=True, null=True)
    info = models.CharField(_('Info'), max_length=400, blank=True, null=True)

    def __str__(self):
        return f'[{self.x},{self.y}] {self.image.artifact.name}'


class PageBanner(models.Model):
    page = models.CharField(_('Page'), max_length=250, choices=Pages.choices, blank=True, null=True)
    image = models.ImageField(_('Image'), upload_to='banners/')
    main_text_he = models.CharField(_('Main text hebrew'), max_length=400, blank=True, null=True)
    main_text_en = models.CharField(_('Main text english'), max_length=400, blank=True, null=True)
    description_he = models.CharField(_('Description hebrew'), max_length=400, blank=True, null=True)
    description_en = models.CharField(_('Description english'), max_length=400, blank=True, null=True)
    credit_he = models.CharField(_('Credit hebrew'), max_length=200, blank=True, null=True)
    credit_en = models.CharField(_('Credit english'), max_length=200, blank=True, null=True)
    active = models.BooleanField(_('Active?'), default=True)

    def __str__(self):
        return f'[{self.id}] {self.get_page_display()}'
