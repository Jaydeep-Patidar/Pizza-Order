from django.shortcuts import redirect, render
from home.models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate 
# Create your views here.
def home(request):
    pizzas = Pizza.objects.all()
    context = {'pizzas': pizzas}
    return render(request, 'home.html', context)


def login_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
        
            user_obj = User.objects.filter(username=username)
            if not user_obj.exists():
                messages.warning(request, "User not found.")
                return redirect('/login/')
        
            user_obj = authenticate(username = username, password=password)
            
            if user_obj:
                login(request, user_obj)
                return redirect('/')

            messages.error(request, "wrong password.")
            return redirect('/login/')
        
        except Exception as e:
            messages.error(request, "something went wrong.")
            return redirect('/register/')

    return render(request, 'login.html')



def register_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
        
            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request, "Username is taken.")
                return redirect('/register/')
        
            user_obj = User.objects.create(username = username)
            user_obj.set_password(password)
            user_obj.save() 
            
            messages.success(request, "Account created.")
            return redirect('/login/')
        
        except Exception as e:
            messages.error(request, "something went wrong.")
            return redirect('/register/')

    return render(request, 'register.html')

    



def add_cart(request, pizza_uid):
    user = request.user
    pizza_obj = Pizza.objects.get(uid = pizza_uid)
    cart , _ = Cart.objects.get_or_create(user = user, is_paid = False)
    cart_items = CartItems.objects.create(
        cart = cart,
        pizza = pizza_obj
    )

    return redirect('/')


def cart(request):
    return render(request, 'cart.html')