from django.contrib import admin
from .models import Book, Review
from .models import UpcomingBook, Cart, CartItem
from .models import Cart, CartItem 

# Register your models here.

admin.site.register(Book)
admin.site.register(Review)

@admin.register(UpcomingBook)
class UpcomingBookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'release_date')
    search_fields = ('title', 'author')
    list_filter = ('release_date',)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'is_popular', 'is_upcoming')
    search_fields = ('title', 'author')
    list_filter = ('is_popular', 'is_upcoming')
