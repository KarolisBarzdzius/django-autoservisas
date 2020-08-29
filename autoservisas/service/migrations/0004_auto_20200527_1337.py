# Generated by Django 3.0.6 on 2020-05-27 10:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0003_auto_20200520_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='description',
            field=tinymce.models.HTMLField(null=True, verbose_name='Aprasymas'),
        ),
        migrations.AddField(
            model_name='car',
            name='photo',
            field=models.ImageField(null=True, upload_to='autos', verbose_name='Nuotrauka'),
        ),
        migrations.AddField(
            model_name='order',
            name='client_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='return_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Gražinimo terminas'),
        ),
    ]