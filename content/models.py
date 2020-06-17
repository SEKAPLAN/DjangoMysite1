from ckeditor.widgets import CKEditorWidget
from django.db import models
from ckeditor_uploader.fields import  RichTextUploadingField

# Create your models here.
from django.forms import ModelForm,FileInput,TextInput,Select
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.urls import reverse
from mptt.models import MPTTModel
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

class Menu(MPTTModel):
    STATUS=(
        ('True','Evet'),
        ('False','Hayır'),
    )
    parent = TreeForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    title = models.CharField(max_length=100,unique=True)
    link = models.CharField(max_length=100,blank=True)
    status = models.CharField(max_length=10,choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by=['title']

    def __str__(self):
        full_path =[self.title]
        k=self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '/'.join(full_path[::-1])
TYPE = (
        ('Sıfır','Sıfır'),
        ('İkinciEl','İkinciEl'),
    )
STATUS=(
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )

class Content(models.Model):
    TYPE = (
        ('menu','menu'),
        ('haber','haber'),
        ('duyuru','duyuru'),
        ('etkinlik','etkinlik'),
    )
    STATUS=(
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    menu = models.OneToOneField(Menu,null=True,blank=True,on_delete=models.CASCADE)
    type = models.CharField(max_length=10,choices=TYPE)
    title = models.CharField(max_length=158)
    price = models.CharField(max_length=15)
    keywords = models.CharField(blank=True,max_length=255)
    description = models.CharField(blank=True, max_length=255)
    image = models.ImageField(blank=True,upload_to='images/')
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False,unique=True)
    status = models.CharField(max_length=18,choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height ="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('content_detail',kwargs={'slug':self.slug})

class CImages(models.Model):
    content = models.ForeignKey(Content,on_delete=models.CASCADE)
    title=models.CharField(max_length=50,blank=True)
    image= models.ImageField(blank=True,upload_to='images/')
    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields=['type','price','title','slug','keywords','description','image','detail']
        widgets = {
            'title' : TextInput(attrs={'class':'input','placeholder':'title'}),
            'price': TextInput(attrs={'class': 'input', 'placeholder': 'price'}),
            'slug': TextInput(attrs={'class':'input','placeholder':'slug'}),
            'keywords': TextInput(attrs={'class': 'input', 'placeholder': 'keywords'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'description'}),
            'type': Select(attrs={'class': 'input', 'placeholder': 'city'}),
            'image':FileInput(attrs={'class':'input','placeholder':'image',}),
            'detail' : CKEditorWidget(),
        }
class ContenImageForm(ModelForm):
    class Meta:
        model = CImages
        fields = ['title','image']
