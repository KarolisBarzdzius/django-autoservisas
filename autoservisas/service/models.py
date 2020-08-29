

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import pytz
from tinymce.models import HTMLField

from PIL import Image

utc=pytz.UTC


# Create your models here.
class Car(models.Model):
    client=models.CharField('Klientas',max_length=200,help_text='Vardas Pavarde??')
    car_model_id=models.ForeignKey('Car_model',on_delete=models.SET_NULL,null=True)
    plates=models.CharField('Valstybinis numeris',max_length=200)
    VIN_code=models.CharField('VIN kodas',max_length=200)
    photo=models.ImageField('Nuotrauka',upload_to='autos',null=True)
    description = HTMLField('Aprasymas',null=True)

    def __str__(self):
        return f"{self.client}:{self.car_model_id},{self.plates},{self.VIN_code}"

    class Meta:
        verbose_name = 'Automobilis'
        verbose_name_plural = 'Automobiliai'


class Car_model(models.Model):
    years = models.IntegerField('Metai', help_text='Iveskite Automobilio Metus')
    brand = models.CharField('Marke',max_length=200,help_text='Iveskite Automobilio Marke')
    model = models.CharField('Modelis',max_length=200, help_text='Iveskite Automobilio Modeli')
    engine = models.CharField('Variklis',max_length=200, help_text='Iveskite Automobilio Varikli')

    def __str__(self):
        return f"{self.years},{self.brand},{self.model},{self.engine}"

    class Meta:
        verbose_name = 'Automobilio Modelis'
        verbose_name_plural = 'Automobiliu Modeliai'

class Order(models.Model):
    car_id=models.ForeignKey('Car',on_delete=models.SET_NULL,null=True)
    client_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    return_time = models.DateTimeField('Gražinimo terminas', null=True, blank=True)

    def __str__(self):
        return f"{self.car_id}"

    class Meta:
        verbose_name = 'Uzsakymas'
        verbose_name_plural = 'Uzsakymai'

    @property
    def praejes_terminas(self):
        if self.return_time and datetime.today().replace(tzinfo=utc) > self.return_time.replace(tzinfo=utc):
            return True
        return False

    @property
    def total_price(self):
        order_line=Order_line.objects.filter(order_id=self.id)
        total=0
        for line in order_line:
            total+=line.quantity * line.price
        return total

class Order_line(models.Model):
    order_id=models.ForeignKey('Order',on_delete=models.SET_NULL,null=True)
    service_id=models.ForeignKey('Service',on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField('Kiekis')
    price=models.FloatField('Kaina')

    @property
    def Sum(self):
        order_total_price=self.quantity * self.price
        return order_total_price

    # @property
    # def total(self):
    #     orders=Order.objects
    #     total=0
    #     for o in orders:
    #         total+=o.price * o.quantity
    #     return total

    def __str__(self):
        return f"{self.service_id} - {self.quantity} : {self.price}"

    class Meta:
        verbose_name = 'Uzsakymo Linija'
        verbose_name_plural = 'Uzsakymu Linijos'

    STATUS = (
        ('p', 'Patvirtinta'),
        ('v', 'Vykdoma'),
        ('a', 'Atlikta'),
        ('t', 'Atšaukta'),
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS,
        blank=True,
        default='a',
        help_text='Statusas',
    )


class Service(models.Model):
    name=models.CharField('Pavadinimas',max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Paslauga'
        verbose_name_plural = 'Paslaugos'


class Service_price(models.Model):
    service_id=models.ForeignKey('Service',on_delete=models.SET_NULL,null=True)
    car_id=models.ManyToManyField(Car_model)
    price=models.FloatField('Kaina')

    def __str__(self):
        return f"{self.service_id}: {self.price}"

    class Meta:
        verbose_name = 'Paslaugos Kaina'
        verbose_name_plural = 'Paslaugu Kainos'

    def display_car_models(self):
        return ','.join(f"{car.brand}/{car.model}/{car.years}/{car.engine}" for car in self.car_id.all())

class OrderReview(models.Model):
    order=models.ForeignKey('Order',on_delete=models.SET_NULL,null=True,blank=True)
    reviewer=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    date_created=models.DateTimeField(auto_now=True)
    comment=models.TextField('Komentaras',max_length=1000)


class Profile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    photo=models.ImageField(default="default.png",upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self):
        super().save()
        img = Image.open(self.photo.path)
        if img.height > 200 or img.width > 200:
            output_size = (150, 150)
            img.thumbnail(output_size)
            img.save(self.photo.path)