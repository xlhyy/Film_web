from django.contrib import admin

# Register your models here.

from Film_App import models


@admin.register(models.FilmInfo)

class FilmInfoAdmin(admin.ModelAdmin):
    ordering = ('m_id',)
    search_fields = ['names','types']
    list_display = ['m_id','names','intros']