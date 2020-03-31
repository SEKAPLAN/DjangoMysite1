from django.contrib import admin

# Register your models here.
from product.models import Category,Produce,Images

class ProduceImageInline(admin.TabularInline):
    model = Images
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    list_display =  ['title', 'status']
    list_filter = ['status']

class ProduceAdmin(admin.ModelAdmin):
    list_display =  ['title','category','price','amount','status','image_tag']
    readonly_fields = ('image_tag',)
    list_filter = ['status','category']
    inlines = [ProduceImageInline]


class ImagesAdmin(admin.ModelAdmin):
        list_display = ['title', 'produce','image_tag']
        readonly_fields = ('image_tag',)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Produce,ProduceAdmin)
admin.site.register(Images,ImagesAdmin)


