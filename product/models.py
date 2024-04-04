"""Doctype"""
from io import BytesIO
from PIL import Image
from django.db import models
from django.core.files import File

# pylint: disable=too-few-public-methods
class Category(models.Model):
    """
    Represents a category for products.
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        """
        Metadata options for the Category model.
        """
        ordering = ('name',)

    def __str__(self):
        """
        Returns the string representation of the category.
        """
        return self.name


class Product(models.Model):
    """
    Represents a product.
    """
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Metadata options for the Product model.
        """
        ordering = ('-created_at',)

    def __str__(self):
        """
        Returns a string representation of the product.
        """
        return self.name

    def get_display_price(self):
        """
        Returns the price of the product formatted as a display price.
        """
        return f"$ {self.price / 100}"

    def get_thumbnail(self):
        """
        Returns the URL of the product's thumbnail image.
        If no thumbnail exists, it creates one from the main image.
        """
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x240x.jpg'

    def make_thumbnail(self, image, size=(300, 300)):
        """
        Creates a thumbnail image from the given image.
        """
        img = Image.open(image)
        img = img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumb_io.seek(0)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
