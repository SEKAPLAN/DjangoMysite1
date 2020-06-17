from django.contrib import admin

# Register your models here.
from content.models import Menu,Content
from content.models import CImages
from mptt.admin import DraggableMPTTAdmin
from product.models import Images

class ContentImageInline(admin.TabularInline):
    model = CImages
    extra = 3

class ContentAdmin(admin.ModelAdmin):
    list_display = ['title','type','image_tag','status','create_at']
    list_filter = ['status','type']
    inlines = [ContentImageInline]
    prepopulated_fields = {'slug':('title',)}


class MenuAdmin(DraggableMPTTAdmin):
    mptt_intent_field = "title"
    list_display = ('tree_actions','indented_title','status')
    list_filter = ['status']


admin.site.register(Menu,MenuAdmin)
admin.site.register(Content,ContentAdmin)



