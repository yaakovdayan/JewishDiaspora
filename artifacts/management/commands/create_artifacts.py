import random
import silly
import os
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django_countries.data import COUNTRIES

from artifacts.models import Artifact, ArtifactImage
from users.models import User


class Command(BaseCommand):
    help = "Create new artifacts."

    def add_arguments(self, parser):
        parser.add_argument('n', type=int)

    def handle(self, n, **options):
        for i in range(n):
            user = User.objects.first()

            # Create random artifact
            o = Artifact()
            o.uploaded_by = user
            o.uploaded_at = silly.datetime().date()
            o.acceptance_date = silly.datetime().date()
            o.status = random.randint(1, 4)
            o.is_private = random.choice([True, False])
            o.name_he = silly.name()
            o.name_en = silly.name()
            o.slug = silly.name(slugify=True)
            o.year_from = random.randint(1700, 2000)
            o.year_to = random.randint(1700, 2000)
            o.origin_country = list(COUNTRIES)[random.randint(0, 200)]
            o.origin_city_he = silly.city()
            o.origin_city_en = silly.city()
            o.donor_name_he = silly.name()
            o.donor_name_en = silly.name()
            o.technical_data_he = silly.thing()
            o.technical_data_en = silly.thing()
            o.description_he = silly.thing()
            o.description_en = silly.thing()
            o.save()

            # Add 4 random images to artifact
            for i in range(4):
                image = ArtifactImage()
                image.artifact = o
                filename = os.path.join(
                    settings.BASE_DIR, f'artifact_images/{random.randint(1, 16)}.jpg'
                )
                image.image = UploadedFile(open(filename, "br"))
                image.is_cover = random.choice([True, False])
                image.year_era = silly.name()
                image.location = silly.name()
                image.full_clean()
                image.save()
