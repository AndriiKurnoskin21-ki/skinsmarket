from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Game(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=10, default='🎮')
    color = models.CharField(max_length=7, default='#FF6B35')
    image = models.ImageField(upload_to='games/', blank=True, null=True)

    class Meta:
        verbose_name = 'Гра'
        verbose_name_plural = 'Ігри'

    def __str__(self):
        return self.name


class Skin(models.Model):
    RARITY_CHOICES = [
        ('consumer', 'Consumer Grade'),
        ('industrial', 'Industrial Grade'),
        ('mil_spec', 'Mil-Spec'),
        ('restricted', 'Restricted'),
        ('classified', 'Classified'),
        ('covert', 'Covert'),
        ('extraordinary', 'Extraordinary'),
    ]

    CONDITION_CHOICES = [
        ('fn', 'Factory New'),
        ('mw', 'Minimal Wear'),
        ('ft', 'Field-Tested'),
        ('ww', 'Well-Worn'),
        ('bs', 'Battle-Scarred'),
    ]

    STATUS_CHOICES = [
        ('available', 'Доступний'),
        ('sold', 'Продано'),
        ('reserved', 'Зарезервовано'),
    ]

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='skins')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skins')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='skins/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES, default='consumer')
    condition = models.CharField(max_length=5, choices=CONDITION_CHOICES, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    float_value = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Скін'
        verbose_name_plural = 'Скіни'

    def __str__(self):
        return f'{self.name} ({self.game.name})'

    def get_absolute_url(self):
        return reverse('skin_detail', args=[self.pk])

    @property
    def rarity_color(self):
        colors = {
            'consumer': '#b0c3d9',
            'industrial': '#5e98d9',
            'mil_spec': '#4b69ff',
            'restricted': '#8847ff',
            'classified': '#d32ce6',
            'covert': '#eb4b4b',
            'extraordinary': '#e4ae39',
        }
        return colors.get(self.rarity, '#ffffff')


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Кошик {self.user.username}'

    @property
    def total(self):
        return sum(item.skin.price for item in self.items.filter(skin__status='available'))


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    skin = models.ForeignKey(Skin, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['cart', 'skin']


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує'),
        ('paid', 'Оплачено'),
        ('completed', 'Завершено'),
        ('cancelled', 'Скасовано'),
    ]

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'

    def __str__(self):
        return f'Замовлення #{self.pk} — {self.buyer.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    skin = models.ForeignKey(Skin, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Review(models.Model):
    skin = models.ForeignKey(Skin, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['skin', 'author']
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'
