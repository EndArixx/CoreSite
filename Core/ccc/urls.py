from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	path('', views.cccindex, name='cccindex'),
	url(r'^login/$', auth_views.LoginView.as_view(template_name='/login.html'), name='login'),
	url(r'^logout/$', auth_views.LogoutView.as_view(next_page ='/'), name='logout'),
	path('comic', views.ComicHome, name = 'ComicHome'),
	path('comic/<int:inComic>', views.ComicSplash, name = 'ComicSplash'),
	path('comic/<int:inComic>/page/<int:inPage>', views.ComicPage, name = 'ComicPage'),
	#Hidden----------------------------------------------------------------
	path('PanelHelper',views.PanelHelper, name = 'PanelHelper'),
]