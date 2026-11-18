from django.contrib import admin
from .models import (
    SchoolInfo, Staff, SchoolClass, News, Event, Achievement,
    GalleryImage, Application, ContactMessage, Sponsor
)

admin.site.site_header = 'School Admin'
admin.site.site_title = 'School Admin'


@admin.register(SchoolInfo)
class SchoolInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # only one record allowed
        return not SchoolInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order')
    list_editable = ('order',)

class AchievementInline(admin.StackedInline):  # Or use admin.StackedInline for a vertical layout
    model = Achievement
    extra = 1  # Number of empty achievement rows displayed by default
    # Optional: specify which fields appear in the inline table
    # fields = ('category', 'title', 'description') 

@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    inlines = [AchievementInline]

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'created')
    list_filter = ('published',)
    search_fields = ('title',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')
    list_filter = ('date',)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'uploaded')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('child_name', 'class_applying_for', 'parent_name',
                    'phone', 'status', 'submitted')
    list_filter = ('status', 'class_applying_for')
    list_editable = ('status',)
    search_fields = ('child_name', 'parent_name', 'phone')
    date_hierarchy = 'submitted'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created', 'handled')
    list_filter = ('handled',)
    list_editable = ('handled',)

admin.site.register(Sponsor)
admin.site.register(Achievement)

