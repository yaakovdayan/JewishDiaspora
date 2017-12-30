from django import forms
from django.forms import inlineformset_factory
from django_countries.widgets import CountrySelectWidget, LazySelectMultiple
from django.contrib.auth.models import User
from django import forms
from .models import Artifact, ArtifactImage, OriginArea, ArtifactMaterial


class ArtifactForm(forms.ModelForm):
    class Meta:
        model = Artifact
        exclude = ['uploaded_at', 'uploaded_by', 'approved_by', 'status']
        widgets = {
            'acceptance_date': forms.TextInput(attrs={'class': 'form-control'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'year_from': forms.TextInput(attrs={'class': 'form-control'}),
            'year_to': forms.TextInput(attrs={'class': 'form-control'}),
            'technical_data': forms.Textarea(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'origin_city': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'origin_country': CountrySelectWidget(attrs={'class': 'form-control'}),
            'origin_area': forms.Select(attrs={'class': 'form-control'}),
            'is_displayed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'displayed_at': forms.TextInput(attrs={'class': 'form-control'}),
            'donor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'display_donor_name': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'artifact_type': forms.Select(attrs={'class': 'form-control'}),
            'artifact_materials': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ArtifactForm, self).__init__(*args, **kwargs)
        if self.errors:
            for field in self.fields:
                if field in self.errors:
                    classes = self.fields[field].widget.attrs.get('class', '')
                    classes += ' is-invalid'
                    self.fields[field].widget.attrs['class'] = classes


class UserArtifactForm(ArtifactForm):
    class Meta(ArtifactForm.Meta):
        exclude = ArtifactForm.Meta.exclude + ['is_displayed', 'displayed_at', 'donor_name', 'is_private',
                                               'acceptance_date', 'slug']


class ArtifactImageForm(forms.ModelForm):
    class Meta:
        model = ArtifactImage
        exclude = ['artifact']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'credit': forms.TextInput(attrs={'class': 'form-control'}),
            'year_era': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'is_cover': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(ArtifactImageForm, self).__init__(*args, **kwargs)
        if self.errors:
            for field in self.fields:
                if field in self.errors:
                    classes = self.fields[field].widget.attrs.get('class', '')
                    classes += ' is-invalid'
                    self.fields[field].widget.attrs['class'] = classes


ArtifactImageFormSet = inlineformset_factory(
    Artifact,
    ArtifactImage,
    form=ArtifactImageForm,
    extra=1,
    can_delete=False
)


class OriginAreaForm(forms.ModelForm):
    class Meta:
        model = OriginArea
        fields = [
            'title',
            'countries'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'countries': LazySelectMultiple(attrs={'class': 'form-control'}),
        }


class ArtifactMaterialForm(forms.ModelForm):
    class Meta:
        model = ArtifactMaterial
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

