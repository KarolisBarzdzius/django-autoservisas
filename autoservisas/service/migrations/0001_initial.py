# Generated by Django 3.0.6 on 2020-05-19 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.CharField(help_text='Vardas Pavarde??', max_length=200, verbose_name='Klientas')),
                ('plates', models.CharField(max_length=200, verbose_name='Valstybinis numeris')),
                ('VIN_code', models.CharField(max_length=200, verbose_name='VIN kodas')),
            ],
        ),
        migrations.CreateModel(
            name='Car_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('years', models.IntegerField(help_text='Iveskite Automobilio Metus', verbose_name='Metai')),
                ('brand', models.CharField(help_text='Iveskite Automobilio Marke', max_length=200, verbose_name='Marke')),
                ('model', models.CharField(help_text='Iveskite Automobilio Modeli', max_length=200, verbose_name='Modelis')),
                ('engine', models.CharField(help_text='Iveskite Automobilio Varikli', max_length=200, verbose_name='Variklis')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.FloatField(verbose_name='Suma')),
                ('car_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.Car')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Pavadinimas')),
            ],
        ),
        migrations.CreateModel(
            name='Service_price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(verbose_name='Kaina')),
                ('car_id', models.ManyToManyField(to='service.Car_model')),
                ('service_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.Service')),
            ],
        ),
        migrations.CreateModel(
            name='Order_line',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='Kiekis')),
                ('price', models.FloatField(verbose_name='Kaina')),
                ('order_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.Order')),
                ('service_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.Service')),
            ],
        ),
        migrations.AddField(
            model_name='car',
            name='car_model_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.Car_model'),
        ),
    ]