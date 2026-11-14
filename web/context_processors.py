from .models import SchoolInfo


def school_info(request):
    return {'school': SchoolInfo.objects.first()}