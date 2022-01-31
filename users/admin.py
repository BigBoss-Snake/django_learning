from django.contrib import admin
from users.models import User
from book.models import Books

# Register your models here.
class BooksAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'author_book')
    list_filter = ('author', 'title', 'author_book')

admin.site.register(Books, BooksAdmin)
admin.site.register(User)
