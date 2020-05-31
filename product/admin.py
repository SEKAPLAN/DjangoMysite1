from django.contrib import admin

# Register your models here.
from product.models import Category,Produce,Images,Comment


from mptt.admin import MPTTModelAdmin
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin

class ProduceImageInline(admin.TabularInline):
    model = Images
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    list_display =  ['title', 'status']
    list_filter = ['status']


class ProduceAdmin(admin.ModelAdmin):
    list_display =  ['title','category','price','amount','status','image_tag']
    readonly_fields = ('image_tag','catimg_tag')
    list_filter = ['status','category']
    inlines = [ProduceImageInline]
    prepopulated_fields = {'slug': ('title',)}


class ImagesAdmin(admin.ModelAdmin):
        list_display = ['title', 'produce','image_tag']
        readonly_fields = ('image_tag',)



class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_produces_count', 'related_produces_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Produce,
                'category',
                'produces_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Produce,
                 'category',
                 'produces_count',
                 cumulative=False)
        return qs

    def related_produces_count(self, instance):
        return instance.produces_count
    related_produces_count.short_description = 'Related products (for this specific category)'

    def related_produces_cumulative_count(self, instance):
        return instance.produces_cumulative_count
    related_produces_cumulative_count.short_description = 'Related products (in tree)'




class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'produce', 'user', 'status']
    list_filter = ['status']


admin.site.register(Category, CategoryAdmin2)
admin.site.register(Produce, ProduceAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Comment, CommentAdmin)




