import factory

from . import models


class ShortenURLFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ShortenURL
