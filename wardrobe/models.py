from django.db import models
from user.models import Profile
import uuid

# Create your models here.

class Item(models.Model):
    top = 'top'
    bottom = 'bottom'
    dress = 'dress'
    shoe = 'shoe'
    coat = 'coat'
    handbag = 'handbag'

    item_type = [
        (top, 'top'),
        (bottom, 'bottom'),
        (dress, 'dress'),
        (shoe, 'shoe'),
        (coat, 'coat'),
        (handbag, 'handbag'),
    ]

    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True, null=True)
    type = models.CharField(max_length=100, choices = item_type, default=shoe)
    image = models.ImageField(upload_to="images", default='itemdefault.jpg')
    sell = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Outfit(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    item = models.ManyToManyField(Item)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True, null=True)
    
    def __str__(self):
        return self.namecd