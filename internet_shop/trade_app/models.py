from datetime import date

from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings


def upload_location(instance, filename):
    return '{0}/{1}'.format(date.today(), filename)


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)
    logo = models.ImageField(upload_to=upload_location, default=settings.DEFAULT_LOGO)
    preview = models.ImageField(blank=True)
    description = models.TextField()
    min_price = models.DecimalField(max_digits=14, decimal_places=2)
    rating = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-rating', 'name']

    # def get_absolute_url(self):
    #     return reverse('product_details', kwargs={'pk': self.id})

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.CharField(max_length=64)
    text = models.TextField()
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
        (4, 'four-speed'),
        (5, 'five-speed'),
        (6, 'six-speed'),
    )
    gearbox = models.PositiveSmallIntegerField(choices=GEARBOX)
    TYPE_OF_TRANSMISSION = (
        ('MT', 'manual transmission'),
        ('AT', 'automatic transmission')
    )
    transmission = models.CharField(max_length=2, choices=TYPE_OF_TRANSMISSION)
    product = models.ForeignKey(Product)

    class Meta:
        ordering = ['name']
        unique_together = (('mark', 'model'),)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Comment)
def calculate_rating(sender, **kwargs):
    product = Product.objects.get(id=kwargs.get('instance').product.id)
    product.rating = len(product.comments.all())
    product.save()


@receiver(post_delete, sender=Product)
def delete_media_file(sender, **kwargs):
    instance = kwargs.get("instance")
    instance.logo.delete(save=False)
    instance.preview.delete(save=False)
