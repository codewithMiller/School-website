from django.db import models
from django.utils.text import slugify


class SchoolInfo(models.Model):
    """One record per school. Edit this in admin to re-skin the site."""
    name = models.CharField(max_length=150)
    tagline = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to='school/', blank=True)
    hero_image = models.ImageField(upload_to='school/', blank=True)
    primary_color = models.CharField(max_length=7, default='#1e40af')
    secondary_color = models.CharField(max_length=7, default='#f59e0b')

    font_family = models.CharField(
    max_length=80, default='Arial, sans-serif',
    help_text='Example: Georgia, serif')
    custom_css = models.TextField(
        blank=True, 
        help_text='Extra CSS for this school only'
        )

    about = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    head_message = models.TextField(blank=True)
    head_name = models.CharField(max_length=100, blank=True)
    head_photo = models.ImageField(upload_to='school/', blank=True)

    phone = models.CharField(max_length=30, blank=True)
    whatsapp = models.CharField(
        max_length=20, blank=True,
        help_text='International format, no plus sign. Example: 2348012345678')
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    map_embed_url = models.URLField(blank=True)

    admission_requirements = models.TextField(blank=True)
    fees_info = models.TextField(blank=True)

    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = 'School info'

    def save(self, *args, **kwargs):
        self.pk = 1  # keeps it to a single record
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Staff(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='staff/', blank=True)
    bio = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    online_profile = models.URLField(max_length=225,blank=True,null=True)
    qualifications = models.TextField(blank=True, help_text='One per line, e.g. B.Ed English, University of Abuja')
    subjects = models.CharField(max_length=200, blank=True, help_text='e.g. English, Igbo')
    experience_years = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Staff'

    def __str__(self):
        return f'{self.name} ({self.role})'


class SchoolClass(models.Model):
    """Used for the Academics page and the admission form dropdown."""
    class_teacher = models.OneToOneField(Staff,on_delete=models.SET_NULL,null=True,blank=True)
    #class captain
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='classes/', blank=True)
    order = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=90, unique=True, blank=True, null=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Classes'

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or 'class'
            slug, n = base, 2
            while SchoolClass.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)    

    def __str__(self):
        return self.name
class Achievement(models.Model):
    class Category(models.TextChoices):
        ACADEMIC = 'ACAD','Academic Excellence'
        COMPETITION = 'COMP','Competition & Contest'
        LEADERSHIP = 'LEAD', 'Leadership & CITIZENSHIP'
        SPORTS = 'SPRT','Sports & Extracurricular'
        MILESTONE = 'MILE','Class Milestone'

    school_class = models.ForeignKey(SchoolClass,on_delete=models.CASCADE,related_name='achievements')
    title = models.CharField(max_length=225)
    category = models.CharField( max_length=50,choices=Category.choices,default=Category.ACADEMIC)
    description = models.TextField(blank=True)
    date_awarded = models.DateField()
    awarded_by = models.CharField(max_length=50,blank=True)

    class Meta:
        ordering = ['-date_awarded']

    def __str__(self):
        return f"{self.title} - {self.school_class.name}"
    
class News(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True)
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    location = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'{self.title} ({self.date})'


class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=150, blank=True)
    uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded']

    def __str__(self):
        return self.caption or f'Image {self.pk}'


class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('reviewing', 'Reviewing'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]

    child_name = models.CharField(max_length=120)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    class_applying_for = models.ForeignKey(
        SchoolClass, on_delete=models.PROTECT, related_name='applications')
    previous_school = models.CharField(max_length=150, blank=True)

    parent_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    message = models.TextField(blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted']

    def __str__(self):
        return f'{self.child_name} ({self.class_applying_for})'


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.name} on {self.created:%d %b %Y}'


class Sponsor(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='sponsors/', blank=True)