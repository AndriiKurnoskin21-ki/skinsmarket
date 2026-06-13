"""
Запуск: python manage.py shell < seed.py
Або: python manage.py runscript seed  (потрібен django-extensions)
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skinsmarket.settings')

from django.contrib.auth.models import User
from skins.models import Game, Skin

# Games
dota, _ = Game.objects.get_or_create(name='Dota 2', slug='dota2', defaults={'icon': '🏆', 'color': '#FF6B35'})
cs, _   = Game.objects.get_or_create(name='CS2', slug='cs2', defaults={'icon': '🔫', 'color': '#FFD700'})
rust, _ = Game.objects.get_or_create(name='Rust', slug='rust', defaults={'icon': '🪓', 'color': '#CD4B2C'})

# Demo seller
if not User.objects.filter(username='demo_seller').exists():
    seller = User.objects.create_user('demo_seller', 'seller@example.com', 'demo1234')
else:
    seller = User.objects.get(username='demo_seller')

# Sample skins
skins_data = [
    # Dota 2
    {'game': dota, 'name': 'Phantom Cloak', 'price': '45.50', 'rarity': 'classified',
     'image_url': 'https://cdn.dota2.com/apps/dota2/images/items/bkb_lg.png',
     'description': 'Легендарний плащ примари. Рідкісний предмет.'},
    {'game': dota, 'name': 'Dragon Lance', 'price': '12.00', 'rarity': 'restricted',
     'image_url': 'https://cdn.dota2.com/apps/dota2/images/items/dragon_lance_lg.png'},
    {'game': dota, 'name': 'Arcane Boots', 'price': '5.99', 'rarity': 'mil_spec',
     'image_url': 'https://cdn.dota2.com/apps/dota2/images/items/boots_of_elven_light_lg.png'},
    # CS2
    {'game': cs, 'name': 'AK-47 | Redline', 'price': '28.00', 'rarity': 'classified',
     'condition': 'ft', 'float_value': 0.25,
     'image_url': 'https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I4lAN/360fx360f',
     'description': 'Класична шкіра з червоними лініями.'},
    {'game': cs, 'name': 'AWP | Dragon Lore', 'price': '1850.00', 'rarity': 'covert',
     'condition': 'fn', 'float_value': 0.01,
     'description': 'Найдорожча та бажана шкіра в CS2.'},
    {'game': cs, 'name': 'M4A4 | Howl', 'price': '560.00', 'rarity': 'covert',
     'condition': 'mw', 'float_value': 0.09},
    # Rust
    {'game': rust, 'name': 'Tempered AK47', 'price': '18.50', 'rarity': 'restricted',
     'description': 'Загартований AK47 — популярний скін у Rust.'},
    {'game': rust, 'name': 'Whiteout Jacket', 'price': '7.25', 'rarity': 'mil_spec'},
    {'game': rust, 'name': 'Banana Crossbow', 'price': '3.50', 'rarity': 'consumer'},
]

for data in skins_data:
    Skin.objects.get_or_create(
        name=data['name'], game=data['game'],
        defaults={'seller': seller, **{k: v for k, v in data.items() if k not in ('name', 'game')}}
    )

print(f"✅ Створено: {Game.objects.count()} ігор, {Skin.objects.count()} скінів")
print(f"   Продавець: demo_seller / demo1234")
