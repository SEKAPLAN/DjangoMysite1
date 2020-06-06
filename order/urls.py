from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    # ex: /home/
    path('', views.index, name='index'),
    path('addtocart/<int:id>',views.addtocart, name='addtocart'),
    path('deletefromcart/<int:id>',views.deletefromcart, name='deletefromcart'),
    path('orderproduce/',views.orderproduce, name='orderproduce')
    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail')

]