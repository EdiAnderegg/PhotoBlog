from .models import Photographer


def photographer(request):
    return {"photographer": Photographer.objects.first()}
