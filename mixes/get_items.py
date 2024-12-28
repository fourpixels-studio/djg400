from .models import Album, Genre, Mix


def get_genres():
    if Genre.objects.exists():
        return Genre.objects.all()
    return "All"


def get_albums():
    if Album.objects.exists():
        return Album.objects.all()
    return "All"


def get_all_mixes():
    if Mix.objects.exists():
        return Mix.objects.all()
    return "All"


def get_latest_mix():
    if Mix.objects.exists():
        return Mix.objects.latest("release_date")
    return "All"
