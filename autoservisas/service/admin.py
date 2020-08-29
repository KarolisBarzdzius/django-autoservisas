from django.contrib import admin

from .models import Service,Car,Car_model,Service_price,Order,\
    Order_line,OrderReview,Profile


class Service_priceAdmin(admin.ModelAdmin):
    list_display = ('service_id','display_car_models','price')

class CarAdmin(admin.ModelAdmin):
    list_display = ('client','car_model_id','plates','VIN_code')
    search_fields = ('plates', 'VIN_code')
    list_filter = ('client','car_model_id')

class Car_modelAdmin(admin.ModelAdmin):
    list_display = ('years','brand','model','engine')


class OrderInline(admin.TabularInline):
    model = Order_line

class OrderAdmin(admin.ModelAdmin):
    list_display = ('car_id','client_id','return_time')
    inlines = [OrderInline]


class Order_lineAdmin(admin.ModelAdmin):
    list_display = ('order_id','service_id','quantity','price','status')


class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ('order','reviewer', 'date_created','comment')




admin.site.register(Service)
admin.site.register(Service_price,Service_priceAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Order_line,Order_lineAdmin)
admin.site.register(Car,CarAdmin)
admin.site.register(Car_model,Car_modelAdmin)
admin.site.register(OrderReview,OrderReviewAdmin)
admin.site.register(Profile)