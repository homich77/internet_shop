from datetime import date
from os import remove

from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.conf import settings
from PIL import Image


def logo_upload_location(instance, filename):
    return 'logo/{0}/{1}'.format(date.today(), filename)


def preview_upload_location(instance, filename):
    return 'preview/{0}/{1}'.format(date.today(), filename)


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)
    logo = models.ImageField(upload_to=logo_upload_location, default=settings.DEFAULT_LOGO)
    preview = models.ImageField(upload_to=preview_upload_location, blank=True)
    description = models.TextField()
    min_price = models.PositiveIntegerField()
    rating = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-rating', 'name']

    def get_absolute_url(self):
        return reverse('cars:product_details', kwargs={'pk': self.id})

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.CharField(max_length=64)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.text


class Specification(models.Model):
    name = models.CharField(max_length=64)
    mark = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    engine_type = models.CharField(max_length=64)
    fuel_consumption = models.DecimalField(max_digits=5, decimal_places=2)
    horsepower = models.PositiveSmallIntegerField()
    max_speed = models.DecimalField(max_digits=5, decimal_places=2)
    GEARBOX = (
        (None, 'chose gearbox'),
        (4, 'four-speed'),
        (5, 'five-speed'),
        (6, 'six-speed'),
    )
    gearbox = models.PositiveSmallIntegerField(choices=GEARBOX)
    TYPE_OF_TRANSMISSION = (
        (None, 'chose type of transmission'),
        ('MT', 'manual transmission'),
        ('AT', 'automatic transmission')
    )
    transmission = models.CharField(max_length=2, choices=TYPE_OF_TRANSMISSION)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')

    class Meta:
        ordering = ['name']
        unique_together = (('name', 'mark', 'model'),)

    def get_absolute_url(self):
        return reverse('cars:spec_details', kwargs={'pk': self.id})

    def __str__(self):
        return self.name


@receiver(post_save, sender=Comment)
def calculate_rating(sender, **kwargs):
    product = Product.objects.get(id=kwargs.get('instance').product.id)
    product.rating = len(product.comments.all())
    product.save()


# @receiver(pre_save, sender=Product)
# def update_media_file(sender, **kwargs):
#     SIZE = (256, 256)
#     product = kwargs.get('instance')
#     old_logo = sender.objects.get(id=product.id).logo
#     logo = Image.open(old_logo.path).copy()
#     logo.thumbnail(SIZE)
#     logo.save('', 'JPEG')
#     product.preview = location
#     try:
#         remove(old_logo.path)
#     except:
#         pass


@receiver(post_delete, sender=Product)
def delete_media_file(sender, **kwargs):
    instance = kwargs.get("instance")
    instance.logo.delete(save=False)
    instance.preview.delete(save=False)
