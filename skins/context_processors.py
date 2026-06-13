from .models import Game


def nav_games(request):
    return {'nav_games': Game.objects.all()}
