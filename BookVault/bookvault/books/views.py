from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q
from .forms import UpcomingBookForm
from .models import UpcomingBook
from django.views.decorators.http import require_http_methods
from .models import Book, Review, Cart, CartItem, UpcomingBook


def home(request):
    """Render the homepage showing book reviews, upcoming books, and popular books."""
    upcoming_books = UpcomingBook.objects.all().order_by('release_date')[:5]
    print("Upcoming books:", upcoming_books)  # Debug line to check data in terminal
    popular_books = Book.objects.filter(is_popular=True)[:5]
    recent_reviews = Review.objects.select_related('book', 'user').order_by('-created_at')[:5]

    context = {
        'upcoming_books': upcoming_books,
        'popular_books': popular_books,
        'recent_reviews': recent_reviews,
    }
    return render(request, 'books/home.html', context)


def book_list(request):
    """Display all books with a search bar to filter by title or author."""
    query = request.GET.get('q')
    books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query)) if query else Book.objects.all()
    context = {'books': books, 'query': query}
    return render(request, 'books/book_list.html', context)


def book_detail(request, pk):
    """Show details of a single book and its reviews."""
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all().order_by('-created_at')
    context = {'book': book, 'reviews': reviews}
    return render(request, 'books/book_detail.html', context)


@login_required
def add_review(request, pk):
    """Allow logged-in users to add a review for a book."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Review.objects.create(book=book, user=request.user, content=content)
            return redirect('book_detail', pk=book.pk)
    return render(request, 'books/add_review.html', {'book': book})


def signup(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@require_http_methods(["GET", "POST"])
@login_required
def add_to_cart(request, book_id):
    """Add a book to the user's cart."""
    book = get_object_or_404(Book, pk=book_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('cart_detail')


@login_required
def cart_detail(request):
    """Display the contents of the user's cart."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'books/cart_detail.html', {'cart': cart})


@login_required
def remove_from_cart(request, item_id):
    """Remove an item from the cart."""
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_detail')


@login_required
def upload_upcoming_book(request):
    """Allow staff users to upload details of an upcoming book."""
    if request.method == 'POST':
        form = UpcomingBookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UpcomingBookForm()
    return render(request, 'books/upload_upcoming_book.html', {'form': form})


def upcoming_book_detail(request, pk):
   '''Display details of an upcoming book.'''
   book = get_object_or_404(UpcomingBook, pk=pk)
   return render(request, 'books/upcoming_book_detail.html', {'book': book})


from .models import UpcomingBook

def upcoming_books(request):
    '''Display a list of all upcoming books.'''
    upcoming_books = UpcomingBook.objects.all()
    return render(request, 'books/upcoming_books.html', {'upcoming_books': upcoming_books})

