from .models import SchoolInfo


def school_info(request):
    school = SchoolInfo.objects.first() or SchoolInfo(name='Your School')
    return {'school': school}