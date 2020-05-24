from django.contrib import admin
from .models import  *
from django.forms.models import BaseInlineFormSet, ModelForm

admin.site.register(Page)

class Comic_Series_Inline(admin.StackedInline):
    ordering = ('SerId__Name',)
    model = Comic_Series
    extra = 0
    
class ComicAdmin(admin.ModelAdmin):
    ordering = ('Name',)
    inlines = [Comic_Series_Inline]
    
admin.site.register(Comic,ComicAdmin)

class Series_Season_Inline(admin.StackedInline):
    ordering = ('SeaId__Name',)
    model = Series_Season
    extra = 0

class SeriesAdmin(admin.ModelAdmin):
    ordering = ('Name',)
    inlines = [Series_Season_Inline]

admin.site.register(Series,SeriesAdmin)

class Season_Issue_Inline(admin.StackedInline):
    ordering = ('IssId__Name',)
    model = Season_Issue
    extra = 0
    
class SeasonAdmin(admin.ModelAdmin):
    ordering = ('Name',)
    inlines = [Season_Issue_Inline]

admin.site.register(Season,SeasonAdmin)

class Issue_Chapter_Inline(admin.StackedInline):
    ordering = ('ChaId__Name',)
    model = Issue_Chapter
    extra = 0
    
class IssueAdmin(admin.ModelAdmin):
    ordering = ('Name',)
    inlines = [Issue_Chapter_Inline]

admin.site.register(Issue,IssueAdmin)

class Chapter_Page_Inline(admin.StackedInline):
    ordering = ('PagId__Name',)
    model = Chapter_Page
    extra = 0
    
class ChapterAdmin(admin.ModelAdmin):
    ordering = ('Name',)
    inlines = [Chapter_Page_Inline]

admin.site.register(Chapter,ChapterAdmin)

