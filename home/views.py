import json
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from home.models import ContactFormMessage,ContactFormu
from home.models import Setting
# Create your views here.
from product.models import Produce
from product.models import Category

from product.models import Images

from product.models import Comment

from home.forms import SearchForm

from home.forms import SignUpForm

from order.models import ShopCart

from home.models import UserProfile


def index(request):
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    siliderdata=Produce.objects.all()[:1]
    category=Category.objects.all()
    dayproduces=Produce.objects.all()[:4]
    lastproduces=Produce.objects.all().order_by('-id')[:4]
    randomproduces = Produce.objects.all().order_by('?')[:4]
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    context = {'setting': setting,'category':category,'page':'home',
               'siliderdata':siliderdata,
               'dayproduces': dayproduces,
               'lastproduces': lastproduces,
               'randomproduces':randomproduces}
    return render(request, 'index.html', context)

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,'page':'hakkimizda'}
    return render(request,'hakkimizda.html', context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,'page':'referanslar'}
    return render(request,'referanslar.html', context)

def iletisim(request):
    if request.method=='POST':
       form =ContactFormu(request.POST)
       if form.is_valid():
           data =ContactFormMessage()
           data.name = form.cleaned_data['name']
           data.email = form.cleaned_data['email']
           data.subject = form.cleaned_data['subject']
           data.message = form.cleaned_data['message']
           data.ip=request.META.get('REMOTE_ADDR')
           data.save()
           messages.success(request , "Mesajınız Başarı ile Gönderilmiştir.Teşekkür Ederiz.")
           return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=1)
    form=ContactFormu()
    context = {'setting': setting,'page':'iletisim','form': form,}
    return render(request,'iletisim.html', context)


def category_produces(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    produces=Produce.objects.filter(category_id=id)
    context ={'produces':produces,'category':category,'categorydata':categorydata}
    return render(request,'produces.html',context)


def produces_detail(request,id,slug):
    category = Category.objects.all()
    produce = Produce.objects.get(pk=id)
    images = Images.objects.filter(produce_id=id)
    comments = Comment.objects.filter(produce_id=id,status='True')
    context = {'produce': produce, 'category': category,'images': images,'comments': comments}
    return render(request, 'produces_detail.html', context)

def produce_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                    produces = Produce.objects.filter(title__icontains=query)

            else:
                    produces = Produce.objects.filter(title__icontains=query, category_id=catid)

            context = {'produces': produces, 'category': category}
            return render(request, 'produce_search.html', context)

    return HttpResponseRedirect('/')

def produce_search_auto(request):
  if request.is_ajax():
    q = request.GET.get('term','')
    produce = Produce.objects.filter(title__icontains=q)
    results = []
    for rs in produce:
      produce_json = {}
      produce_json = rs.title
      results.append(produce_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/')

        else:
            messages.error(request, "Login hatası! Kulanıcı bilgileri yanlış")
            return HttpResponseRedirect('/login')


    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.jpg"
            data.save()
            messages.success(request, "Hoş geldiniz.Sitemize başarılı bir şelde üye oldunuz ")
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,'form': form}
    return render(request, 'signup.html', context)

