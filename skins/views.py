from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q, Avg
from django.http import JsonResponse
from .models import Skin, Game, Cart, CartItem, Order, OrderItem, Review
from .forms import SkinForm, UserRegisterForm, ReviewForm


def index(request):
    featured_skins = Skin.objects.filter(status='available').order_by('-views')[:8]
    games = Game.objects.all()
    recent_skins = Skin.objects.filter(status='available').order_by('-created_at')[:4]
    stats = {
        'total_skins': Skin.objects.filter(status='available').count(),
        'total_games': Game.objects.count(),
        'sold_skins': Skin.objects.filter(status='sold').count(),
    }
    return render(request, 'skins/index.html', {
        'featured_skins': featured_skins,
        'games': games,
        'recent_skins': recent_skins,
        'stats': stats,
    })


def skin_list(request):
    skins = Skin.objects.filter(status='available')
    games = Game.objects.all()

    game_slug = request.GET.get('game')
    rarity = request.GET.get('rarity')
    search = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort', '-created_at')

    if game_slug:
        skins = skins.filter(game__slug=game_slug)
    if rarity:
        skins = skins.filter(rarity=rarity)
    if search:
        skins = skins.filter(Q(name__icontains=search) | Q(description__icontains=search))
    if min_price:
        skins = skins.filter(price__gte=min_price)
    if max_price:
        skins = skins.filter(price__lte=max_price)

    valid_sorts = ['-created_at', 'created_at', 'price', '-price', '-views']
    if sort in valid_sorts:
        skins = skins.order_by(sort)

    return render(request, 'skins/skin_list.html', {
        'skins': skins,
        'games': games,
        'selected_game': game_slug,
        'selected_rarity': rarity,
        'search_query': search,
        'sort': sort,
        'rarity_choices': Skin.RARITY_CHOICES,
    })


def skin_detail(request, pk):
    skin = get_object_or_404(Skin, pk=pk)
    skin.views += 1
    skin.save(update_fields=['views'])

    similar_skins = Skin.objects.filter(
        game=skin.game, status='available'
    ).exclude(pk=pk)[:4]

    reviews = skin.reviews.all().order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    review_form = None
    if request.user.is_authenticated and not reviews.filter(author=request.user).exists():
        if request.method == 'POST':
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.skin = skin
                review.author = request.user
                review.save()
                messages.success(request, 'Відгук додано!')
                return redirect('skin_detail', pk=pk)
        else:
            review_form = ReviewForm()

    return render(request, 'skins/skin_detail.html', {
        'skin': skin,
        'similar_skins': similar_skins,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_form': review_form,
    })


@login_required
def sell_skin(request):
    if request.method == 'POST':
        form = SkinForm(request.POST, request.FILES)
        if form.is_valid():
            skin = form.save(commit=False)
            skin.seller = request.user
            skin.save()
            messages.success(request, f'Скін "{skin.name}" виставлено на продаж!')
            return redirect('skin_detail', pk=skin.pk)
    else:
        form = SkinForm()
    return render(request, 'skins/sell_skin.html', {'form': form})


@login_required
def add_to_cart(request, pk):
    skin = get_object_or_404(Skin, pk=pk, status='available')
    if skin.seller == request.user:
        messages.error(request, 'Ви не можете купити власний скін.')
        return redirect('skin_detail', pk=pk)

    cart, _ = Cart.objects.get_or_create(user=request.user)
    _, created = CartItem.objects.get_or_create(cart=cart, skin=skin)
    if created:
        messages.success(request, f'"{skin.name}" додано до кошика!')
    else:
        messages.info(request, 'Цей скін вже є у кошику.')
    return redirect('cart')


@login_required
def remove_from_cart(request, pk):
    cart = get_object_or_404(Cart, user=request.user)
    CartItem.objects.filter(cart=cart, skin_id=pk).delete()
    return redirect('cart')


@login_required
def cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('skin__game').all()
    return render(request, 'skins/cart.html', {
        'cart': cart,
        'items': items,
    })


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.filter(skin__status='available')

    if not items.exists():
        messages.error(request, 'Кошик порожній або скіни вже продані.')
        return redirect('cart')

    if request.method == 'POST':
        total = sum(item.skin.price for item in items)
        order = Order.objects.create(
            buyer=request.user,
            total_price=total,
            status='paid',
        )
        for item in items:
            OrderItem.objects.create(order=order, skin=item.skin, price=item.skin.price)
            item.skin.status = 'sold'
            item.skin.save()

        cart.items.all().delete()
        messages.success(request, f'Замовлення #{order.pk} оформлено! Дякуємо за покупку.')
        return redirect('order_detail', pk=order.pk)

    return render(request, 'skins/checkout.html', {'cart': cart, 'items': items})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, buyer=request.user)
    return render(request, 'skins/order_detail.html', {'order': order})


@login_required
def profile(request):
    my_skins = Skin.objects.filter(seller=request.user).order_by('-created_at')
    if request.user.is_staff:
        my_orders = Order.objects.select_related('buyer').order_by('-created_at')
    else:
        my_orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    return render(request, 'skins/profile.html', {
        'my_skins': my_skins,
        'my_orders': my_orders,
    })


@login_required
def delete_skin(request, pk):
    skin = get_object_or_404(Skin, pk=pk, seller=request.user)
    if request.method == 'POST':
        skin.delete()
        messages.success(request, 'Скін видалено.')
    return redirect('profile')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Ласкаво просимо, {user.username}!')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def newsletter_subscribe(request):
    from .forms import NewsletterForm
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            messages.success(request, f'Дякуємо! {form.cleaned_data["name"]}, ви підписались на розсилку.')
    return redirect(request.META.get('HTTP_REFERER', 'index'))


def game_skins(request, slug):
    game = get_object_or_404(Game, slug=slug)
    skins = Skin.objects.filter(game=game, status='available').order_by('-created_at')
    games = Game.objects.all()
    return render(request, 'skins/game_skins.html', {
        'game': game,
        'skins': skins,
        'games': games,
    })
