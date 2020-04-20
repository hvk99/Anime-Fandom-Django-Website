from django.contrib import admin
from .models import Character, Anime, Genre
from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.

class CharacterAdmin(admin.ModelAdmin):

	fieldsets = [
		("Introduction", {"fields" : ["name", "anime"]}),
		("slug", {"fields" : ["slug"]}),
		("Characteristics and Story", {"fields" : ["skill", "power", "description"]}),
	]

	formfield_overrides = {
		models.TextField: {'widget': TinyMCE()}
	}


admin.site.register(Genre)
admin.site.register(Anime)
admin.site.register(Character, CharacterAdmin)