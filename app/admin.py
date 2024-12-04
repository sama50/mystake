from django.contrib import admin
from app.models import PattiGame
# Register your models here.


@admin.register(PattiGame)
class PattiGameAdmin(admin.ModelAdmin):
    list_display = ("id",)
