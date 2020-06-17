from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.crypto import get_random_string


from order.models import ShopCartForm,ShopCart
from product.models import Category


# Create your views here.
from order.models import OrderForm,Order

from order.models import OrderProduce
from product.models import Produce

from home.models import UserProfile

from content.models import Content


def index(request):
    return HttpResponse('order app')

@login_required(login_url='/login')
def addtocart(request,id):
    url = request.META.get('HTTP_REFERER')
    checkproduce = ShopCart.objects.filter(produce_id=id)
    if request.method == 'POST':
        form = ShopCartForm(request.POST)
        if form.is_valid():
            current_user = request.user
            data = ShopCart()
            data.user_id = current_user.id
            data.produce_id = id
            data.quantity = form.cleaned_data['quantity']
            data.save()

        request.session['cart_items']=ShopCart.objects.filter(user_id=current_user.id).count()
        messages.success(request, "Ürün başarı ile sepete eklendi.Teşekkür ederiz")
        return HttpResponseRedirect(url)

    else:
         current_user = request.user
         data = ShopCart()
         data.user_id = current_user.id
         data.produce_id = id
         data.quantity = 1
         data.save()
         request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
         messages.success(request, "Ürün başarı ile sepete eklendi.Teşekkür ederiz")
         return HttpResponseRedirect(url)


    messages.warning(request, "Ürün sepete eklemede hata oluştu.Lütfen kontrol ediniz")
    return HttpResponseRedirect(url)

@login_required(login_url='/login')
def shopcart(request):
    category =Category.objects.all()
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    total=0
    for rs in schopcart:
        total +=rs.produce.price * rs.quantity

    context ={'schopcart': schopcart,'category': category,'total': total}
    return render(request,'shoopcart_produce.html',context)


@login_required(login_url='/login')
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    current_user =request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    messages.success(request, "Ürün sepetten silinmiştir.")
    return HttpResponseRedirect("/shopcart")

@login_required(login_url='/login')
def orderproduce(request):
    category =Category.objects.all()
    current_user =request.user
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    total =0
    for rs in schopcart:
        total += rs.produce.price * rs.quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper
            data.code = ordercode
            data.save()
            schopcart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in schopcart:
                detail = OrderProduce()
                detail.order_id = data.id
                detail.produce_id =rs.produce_id
                detail.user_id = current_user.id
                detail.quantity =rs.quantity
                produce = Produce.objects.get(id=rs.produce_id)
                produce.amount -= rs.quantity
                produce.save()
                detail.price =rs.produce.price
                detail.amount = rs.amount
                detail.save()
            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items']=0
            messages.success(request,"Your order has been  completed.Thank you")
            return render(request,'Order_Completed.html',{'ordercode':ordercode,'category':category})
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect("/order/orderproduce")
    form =OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'schopcart':schopcart,'category':category,'total':total,'form':form,'profile':profile,
               }
    return render(request,'Order_Form.html',context)













