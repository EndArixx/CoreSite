from django.contrib import admin
from .models import  *
from django.forms.models import BaseInlineFormSet, ModelForm

admin.site.register(Page)

class Page_Comic_Inline(admin.StackedInline):
    ordering = ('PagID__Number',)
    model = Page_Comic
    extra = 0
	
class ComicAdmin(admin.ModelAdmin):
	ordering = ('Name',)
	inlines = [Page_Comic_Inline]

admin.site.register(Comic,ComicAdmin)