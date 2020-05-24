from django.conf import settings
from django.db import models
from datetime import datetime  

'''
IMPORTANT Identifiers/ForeignKeys:
    --Comic--
    ComId = Comic Id
    SerId = Series Id
    SeaId = Season Id
    IssId = Issue Id
    ChaId = Chapter Id
    PagId = Page Id
    PanId = Panel Id

    TagId = Tag Id
    AutId = Author Id
    GenId = Genre Id
'''

'''
---Heirarchy:---
    Comic 
    Series
    Season
    Issue
    Chapter
    Page
    Panel
'''

'''
---Search info---
Tag
Auther
Genre
Date
'''

#########################################################
#                  Hierarchy of tables                  #
#########################################################
class Comic(models.Model):
    ComId = models.AutoField(primary_key=True)
    Name =  models.CharField(max_length=200)
    Date = models.DateField()
    Description =  models.CharField(max_length=8000,blank=True, null=True)
    Summary = models.CharField(max_length=8000,blank=True, null=True)
    class Meta:
        verbose_name = 'Comic'
        verbose_name_plural = '1) Comics' 
    def __str__(self):
        return self.Name

class Series(models.Model):
    SerId = models.AutoField(primary_key=True)
    Name =  models.CharField(max_length=200)
    Description =  models.CharField(max_length=8000,blank=True, null=True)
    Summary = models.CharField(max_length=8000,blank=True, null=True)
    Start = models.DateField(null=True)
    End = models.DateField(null=True)
    class Meta:
        verbose_name = 'Series'
        verbose_name_plural = '2) Serieses' 
    def __str__(self):
        return self.Name

class Season(models.Model):
    SeaId = models.AutoField(primary_key=True)
    Name =  models.CharField(max_length=200)
    Description =  models.CharField(max_length=8000,blank=True, null=True)
    Summary = models.CharField(max_length=8000,blank=True, null=True)
    Start = models.DateField(null=True)
    End = models.DateField(null=True)
    class Meta:
        verbose_name = 'Season'
        verbose_name_plural = '3) Seasons' 
    def __str__(self):
        return self.Name

class Issue(models.Model):
    IssId = models.AutoField(primary_key=True)
    Name =  models.CharField(max_length=200)
    Date = models.DateField(null=True)
    Description =  models.CharField(max_length=8000,blank=True, null=True)
    Summary = models.CharField(max_length=8000,blank=True, null=True)
    class Meta:
        verbose_name = 'Issue'
        verbose_name_plural = '4) Issues' 
    def __str__(self):
        return self.Name

class Chapter(models.Model):
    ChaId = models.AutoField(primary_key=True)
    Name =  models.CharField(max_length=200)
    Description =  models.CharField(max_length=8000,blank=True, null=True)
    Summary = models.CharField(max_length=8000,blank=True, null=True)
    class Meta:
        verbose_name = 'Chapter'
        verbose_name_plural = '5) Chapters' 
    def __str__(self):
        return self.Name

class Page(models.Model):
    PagId = models.AutoField(primary_key=True)
    Name =  models.CharField(max_length=200)
    Number = models.IntegerField(default=0)
    Image = models.ImageField()
    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = '6) Pages' 
        unique_together = ('Name', 'Number')
    def __str__(self):
        return self.Name + ' - '+ str(self.Number)


class Panel(models.Model):
    PanId = models.AutoField(primary_key=True)
    PagId =  models.ForeignKey(Page, on_delete=models.CASCADE) 
    Number = models.IntegerField(default=0)
    Image = models.ImageField()
    class Meta:
        verbose_name = 'Panel'
        verbose_name_plural = '7) Panels' 
        unique_together = ('PagId', 'Number')
    def __str__(self):
        return PagId.Name + ' - ' + str(PagId.Number) + ' (' + str(self.Number) + ')'


#########################################################
#                     Relationships                     #
#########################################################

class Comic_Series(models.Model):
    ComId = models.ForeignKey(Comic, on_delete=models.CASCADE) 
    SerId =  models.ForeignKey(Series, on_delete=models.CASCADE) 
    class Meta:
        unique_together = ('ComId', 'SerId')
    def __str__(self):
        return self.ComId.Name + ' - '+ str(self.SerId.Number)

class Series_Season(models.Model):
    SerId =  models.ForeignKey(Series, on_delete=models.CASCADE) 
    SeaId = models.ForeignKey(Season, on_delete=models.CASCADE) 
    class Meta:
        unique_together = ('SerId', 'SeaId')
    def __str__(self):
        return self.SerId.Name + ' - '+ str(self.SeaId.Number)

class Season_Issue(models.Model):
    SeaId =  models.ForeignKey(Season, on_delete=models.CASCADE) 
    IssId = models.ForeignKey(Issue, on_delete=models.CASCADE) 
    class Meta:
        unique_together = ('SeaId', 'IssId')
    def __str__(self):
        return self.SeaId.Name + ' - '+ str(self.IssId.Number)

class Issue_Chapter(models.Model):
    IssId =  models.ForeignKey(Issue, on_delete=models.CASCADE)
    ChaId = models.ForeignKey(Chapter, on_delete=models.CASCADE) 
    class Meta:
        unique_together = ('IssId', 'ChaId')
    def __str__(self):
        return self.IssId.Name + ' - '+ str(self.ChaId.Number)

class Chapter_Page(models.Model):
    ChaId = models.ForeignKey(Chapter, on_delete=models.CASCADE) 
    PagId =  models.ForeignKey(Page, on_delete=models.CASCADE) 
    class Meta:
        unique_together = ('ChaId', 'PagId')
    def __str__(self):
        return self.ChaId.Name + ' - '+ str(self.PagId.Number)

#########################################################
#                     Search Tables                     #
#########################################################
