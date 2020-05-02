from django.conf import settings
from django.db import models
from datetime import datetime  

'''
IMPORTANT Identifiers/ForeignKeys:
	--Comic--
    SerId = Series Id
    SeaId = Season Id
    ComID = Comic Id
    ChaID = Chapter Id
    PagId = Page Id
'''

'''
---Heirarchy:---
    Series
    Season
    Comic
    Chapter
    Page
'''

class Comic(models.Model):
    ComID = models.AutoField(primary_key=True)
    Name =  models.CharField(max_length=200)
    #should this be its own table?
    Description =  models.CharField(max_length=4000,blank=True, null=True)
    #should this be its own table?
    Summary = models.CharField(max_length=4000,blank=True, null=True)
    #Tag:                       one to many tables
    #Auther/Artist/Creator:     one to many tables
    #Genre:                     one to many tables
    def __str__(self):
        return self.Name

class Page(models.Model):
    PagID = models.AutoField(primary_key=True)
    Name =  models.CharField(max_length=200)
    Number = models.IntegerField(default=0)
    Image = models.ImageField()
    class Meta:
        unique_together = ('Name', 'Number')
    def __str__(self):
        return self.Name + ' - '+ str(self.Number)

class Page_Comic(models.Model):
	ComID = models.ForeignKey(Comic, on_delete=models.CASCADE) 
	PagID =  models.ForeignKey(Page, on_delete=models.CASCADE) 
	class Meta:
		unique_together = ('ComID', 'PagID')
	def __str__(self):
		return self.ComID.Name + ' - '+ str(self.PagID.Number)
