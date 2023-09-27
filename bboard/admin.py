from django.contrib import admin
from bboard.models import Bb, Rubric


class BbAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'published', 'rubric')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content')
    readonly_fields = ['published']
    list_editable = ['rubric']


admin.site.register(Rubric)
admin.site.register(Bb, BbAdmin)
