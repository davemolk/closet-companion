# Generated by Django 3.2.3 on 2021-07-31 02:30

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('wardrobe', '0009_alter_outfit_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format='JPEG', keep_meta=True, quality=75, size=[500, 300], upload_to='images'),
        ),
    ]
