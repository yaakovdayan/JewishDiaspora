from django.contrib import admin
from django.utils.translation import ugettext as _
from . import models


class ArtifactImageInline(admin.TabularInline):
    model = models.ArtifactImage
    extra = 1


class ArtifactAdmin(admin.ModelAdmin):
    inlines = [
        ArtifactImageInline,
    ]


class PageBannerAdmin(admin.ModelAdmin):
    list_display = ('page', 'main_text_he', 'main_text_en', 'credit_he', 'credit_en', 'active')
    list_display_links = ('page', 'main_text_he', 'main_text_en', 'credit_he', 'credit_en', 'active')


class OriginAreaAdmin(admin.ModelAdmin):
    list_display = ('title_he', 'title_en', 'countries_list')
    list_display_links = ('title_he', 'title_en', 'countries_list')

    def countries_list(self, obj):
        return ",".join([x.name for x in obj.countries])

    countries_list.short_description = _('Countries')


admin.site.register(models.Artifact, ArtifactAdmin)
admin.site.register(models.ArtifactType)
admin.site.register(models.ArtifactMaterial)
admin.site.register(models.PageBanner, PageBannerAdmin)
admin.site.register(models.OriginArea, OriginAreaAdmin)
