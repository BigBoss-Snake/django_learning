from django.contrib import admin
from users.models import User
from book.models import Books, Category

# Register your models here.
class BooksAdmin(admin.ModelAdmin):
    list_display = ('title','author','author_book')
    list_filter = ('author', 'title', 'author_book')

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'last_name', 'is_active')
    list_filter = ('email', 'last_name', 'is_active')

# class CategoryAdmin(admin.ModelAdmin):


admin.site.register(Books, BooksAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Category)
