from django.contrib import admin

# Register your models here.
from django.urls import reverse

from product.models import Product, Comment


class ProductAdmin(admin.ModelAdmin):
    exclude = ('user_id', 'like_count')

    def view_on_site(self, obj):
        return reverse('product_slug', args=[obj.slug])


class CommentAdmin(admin.ModelAdmin):
    def view_on_site(self, obj):
        return reverse('product_slug', args=[obj.product_id.slug])


admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
