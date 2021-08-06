from django.db import models
from user.models import Profile
import uuid
from django_resized import ResizedImageField


# Create your models here.

class Item(models.Model):
    top = 'top'
    bottom = 'bottom'
    dress = 'dress'
    shoe = 'shoe'
    outerwear = 'outerwear'
    handbag = 'handbag'
    other = 'other'

    item_type = [
        (top, 'top'),
        (bottom, 'bottom'),
        (dress, 'dress'),
        (shoe, 'shoe'),
        (outerwear, 'outerwear'),
        (handbag, 'handbag'),
        (other, 'other'),
    ]

    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True, null=True)
    type = models.CharField(max_length=100, choices = item_type, default=shoe)
    image = ResizedImageField(size=[961, 1140], blank=True, null=True, upload_to="images", default="images/itemdefault.jpg")
    url = models.URLField(max_length=200, blank=True, null=True)
    sell = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
        
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Tag(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Outfit(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    items= models.ManyToManyField(Item)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.name
