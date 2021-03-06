from bokeh.models import TextInput
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.forms import ModelForm,TextInput,Textarea
from django.utils.safestring import mark_safe


class Setting(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=200)
    keywords = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    company = models.CharField(max_length=50)
    address = models.CharField(blank=True,max_length=200)
    phone = models.CharField(blank=True,max_length=15)
    fax = models.CharField(blank=True,max_length=15)
    email = models.CharField(blank=True,max_length=50)
    smtpserver = models.CharField(max_length=20)
    smtpemail = models.CharField(max_length=50 )
    smtppasword = models.CharField(max_length=10)
    smtpport = models.CharField(blank=True,max_length=5)
    icon = models.ImageField(blank=True,upload_to='images/')
    facebook = models.CharField(blank=True,max_length=50)
    instagram = models.CharField(blank=True,max_length=50)
    twitter = models.CharField(blank=True,max_length=50)
    aboutus = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class ContactFormMessage(models.Model):
        STATUS = (
            ('New', 'New'),
            ('Read', 'Read'),
            ('Closed', 'Closed'),
        )
        name = models.CharField(blank=True,max_length=200)
        email = models.CharField(blank=True, max_length=50)
        subject = models.CharField(blank=True,max_length=200)
        message = models.CharField(blank=True,max_length=200)
        status = models.CharField(max_length=10, choices=STATUS,default='New')
        ip = models.CharField(blank=True,max_length=50)
        note = models.CharField(blank=True, max_length=200)
        create_at = models.DateTimeField(auto_now_add=True)
        update_at = models.DateTimeField(auto_now=True)


def __str__(self):
    return self.name

class ContactFormu(ModelForm):
    class Meta:
        model =ContactFormMessage
        fields=['name','email','subject','message']
        widgets ={
            'name' : TextInput(attrs={'class ':'input-xlarge','placeholder':'Name & Surname'}),
            'subject': TextInput(attrs={'class ': 'input-xlarge', 'placeholder': 'Subject'}),
            'email': TextInput(attrs={'class ': 'input-xlarge', 'placeholder': 'E-mail'}),
            'message': Textarea(attrs={'class ': 'input-xlarge', 'placeholder': 'Your Message' }),
        }


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    image = models.ImageField(blank=True, upload_to='images/users')
    def __str__(self):
        return self.user.username

    def user_name(self):
        return '['+ self.user.username + '] ' +self.user.username

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'



class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'country', 'image']