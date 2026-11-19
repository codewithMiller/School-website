
from .models import SchoolInfo, Sponsor


def school_info(request):
    school = SchoolInfo.objects.first() or SchoolInfo(name='Your School')
    sponsors = Sponsor.objects.all()

    return {
        'school': school,
        'sponsors': sponsors,
    }
