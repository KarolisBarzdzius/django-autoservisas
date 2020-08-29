from django.shortcuts import render, get_object_or_404
from .models import Service,Car,Car_model,Service_price,Order,Order_line
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm


from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,CreateView,DeleteView,UpdateView


def index(request):

    num_services = Service.objects.all().count()
    num_orders = Order_line.objects.all().filter(status__exact ='v').count()
    num_cars=Car.objects.all().count()
    completed_orders = Order_line.objects.filter(status__exact='a').count()

    context = {
        'num_services': num_services,
        'num_orders': num_orders,
        'num_cars': num_cars,
        'completed_orders':completed_orders,
    }

    return render(request, 'index.html', context=context)



def cars(request):
    paginator=Paginator(Car.objects.all(),5)
    page_number=request.GET.get('page')
    paged_cars=paginator.get_page(page_number)
    # single=Car.objects.all()

    context={
        # 'single':single,
        'cars':paged_cars,
    }
    return render(request,'cars.html',context=context)

def car(request, car_id):
    single_car= get_object_or_404(Car, pk=car_id)
    return render(request, 'car.html', {'car': single_car})

# def orders(request):
#     orders=Order_line.objects.all()
#     context={
#         'orders':orders.filter(status__exact ='v')
#     }
#     return render(request,'orders.html',context=context)
#
# def order(request, order_id):
#     single_order= get_object_or_404(Order_line, pk=order_id)
#     return render(request, 'order.html', {'order': single_order})

def search(request):
    query = request.GET.get('query')
    search_results = Car.objects.filter(Q(client__icontains=query) | Q(plates__icontains=query) | Q(VIN_code__icontains=query) | Q(car_model_id__brand__icontains=query) | Q(car_model_id__model__icontains=query))
    return render(request, 'search.html', {'cars': search_results, 'query': query})


class OrdersListView(generic.ListView):
    model=Order
    context_object_name = 'orders'
    paginate_by = 5
    template_name = 'orders.html'

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order.html'


class OrdersByUserListView(LoginRequiredMixin,ListView):
    model=Order
    template_name = 'user_orders.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(client_id=self.request.user)

class OrdersByUserCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ['car_id','return_time']
    success_url = "/service/myorders/"
    template_name = 'user_order_form.html'

    def form_valid(self, form):
        form.instance.client_id = self.request.user
        return super().form_valid(form)



class OrdersByUserDeleteView(LoginRequiredMixin,UserPassesTestMixin , generic.DeleteView):
    model = Order
    success_url = "/service/myorders/"
    template_name = 'user_order_delete.html'

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.client_id



class OrdersByUserUpdateView(LoginRequiredMixin,UserPassesTestMixin , generic.UpdateView):
    model = Order
    success_url = "/service/myorders/"
    fields = ['car_id', 'return_time']
    template_name = 'user_order_form.html'

    def form_valid(self, form):
        form.instance.client_id = self.request.user
        return super().form_valid(form)

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.client_id







@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')



@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)

