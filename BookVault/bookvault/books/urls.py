from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<int:pk>/', views.book_detail, name='book_detail'),
    path('<int:pk>/add_review/', views.add_review, name='add_review'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('upcoming/<int:pk>/', views.upcoming_book_detail, name='upcoming_book_detail'),
    path('upcoming/', views.upcoming_books, name='upcoming_books'),
] 

#     """Display popular books based on the number of reviews."""
#     popular_books = Book.objects.annotate(review_count=Count('reviews')).order_by('-review_count')[:5]    
#     return render(request, 'books/popular_books.html', {'popular_books': popular_books})

#     """Display upcoming books based on their release date."""
#     upcoming_books = Book.objects.filter(release_date__gte=timezone.now()).order_by('release_date')   
#     return render(request, 'books/upcoming_books.html', {'upcoming_books': upcoming_books})
#     return render(request, 'books/search_results.html', {'books': books, 'query': query})