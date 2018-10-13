from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('player/<int:PID>', views.player, name='player'),
	path('CharacterSheet/<int:CIDin>', views.Character_Sheet, name='CharacterSheet'),
	path('group/<int:GIDin>', views.group, name = 'group'),
	path('group/<int:GIDin>/npcs', views.NPClist,name = 'NPClist'),
	path('group/<int:GIDin>/npc/<int:NIDin>', views.NPCpage, name = 'NPCpage'),
	path('PlayerHandbook',views.PlayerHandbook, name = 'PlayerHandbook'),
	#login stuff
	url(r'^login/$', auth_views.LoginView.as_view(template_name='stats/login.html'), name='login'),
	url(r'^logout/$', auth_views.LogoutView.as_view(next_page ='/'), name='logout'),
]