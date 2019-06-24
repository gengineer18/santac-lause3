from .models import Present


def common(request):
    content = {
        "side_presents": Present.objects.order_by('-favorite'),
    }
    return content
