from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from home.models import ContactFormMessage,ContactFormu
from home.models import Setting
# Create your views here.
from product.models import Produce
from product.models import Category

from product.models import Images

from product.models import Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    siliderdata=Produce.objects.all()[:1]
    category=Category.objects.all()
    dayproduces=Produce.objects.all()[:4]
    lastproduces=Produce.objects.all().order_by('-id')[:4]
    randomproduces = Produce.objects.all().order_by('?')[:4]

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
