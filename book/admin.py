from django.contrib import admin
from book.models import Books, Category, Value


class BooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'author_book', 'value', 'price')
    list_filter = ('author', 'title', 'author_book', 'category')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category')


admin.site.register(Books, BooksAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Value)
