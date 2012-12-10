from django.contrib import admin
from models import Category, WMSServer, Layer


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'order')
    list_display_links = ('id',)
    list_editable = ('title', 'slug', 'order')
    prepopulated_fields = {'slug': ('title',)}



class LayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'visible', 'category_order', 'map_order')
    list_display_links = ('id',)
    list_editable = ('title', 'visible', 'category_order', 'map_order')


admin.site.register(Category, CategoryAdmin)
admin.site.register(WMSServer, admin.ModelAdmin)
admin.site.register(Layer, LayerAdmin)