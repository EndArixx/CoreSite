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
	path('ForestHandbook',views.ForestHandbook, name = 'ForestHandbook'),
	path('group/<int:GIDin>/timeline', views.EventTimeline,name = 'EventTimeline'),
	path('group/<int:GIDin>/event/<int:EIDin>', views.EventPage, name = 'Eventpage'),
	#path('group/<int:GIDin>/factions', views.FactionList,name = 'FactionList'),
	path('group/<int:GIDin>/faction/<int:FIDin>', views.FactionPage, name = 'FactionPage'),
	path('group/<int:GIDin>/health/', views.HealthPage, name = 'HealthPage'),
	#Character HP/ARMOR
	path('CharacterSheet/<int:CIDin>/HPSetMax', views.CharacterHPFullHeal, name='CharacterHPFullHeal'),
	path('CharacterSheet/<int:CIDin>/ArmorReset', views.CharacterArmorReset, name='CharacterArmorReset'),
	path('CharacterSheet/<int:CIDin>/HPSetAll', views.CharacterHPHealALL, name='CharacterHPHealALL'),
	path('CharacterSheet/<int:CIDin>/ArmorAll', views.CharacterArmorALL, name='CharacterArmorALL'),
	path('CharacterSheet/<int:CIDin>/HurtHead', views.CharacterDamageHead, name='CharacterDamageHead'),
	path('CharacterSheet/<int:CIDin>/HurtCore', views.CharacterDamageCore, name='CharacterDamageCore'),
	path('CharacterSheet/<int:CIDin>/HurtRArm', views.CharacterDamageRightArm, name='CharacterDamageRightArm'),
	path('CharacterSheet/<int:CIDin>/HurtLArm', views.CharacterDamageLeftArm, name='CharacterDamageLeftArm'),
	path('CharacterSheet/<int:CIDin>/HurtRLeg', views.CharacterDamageRightLeg, name='CharacterDamageRightLeg'),
	path('CharacterSheet/<int:CIDin>/HurtLLeg', views.CharacterDamageLeftLeg, name='CharacterDamageLeftLeg'),
	path('CharacterSheet/<int:CIDin>/HealHead', views.CharacterHealHead, name='CharacterHealHead'),
	path('CharacterSheet/<int:CIDin>/HealCore', views.CharacterHealCore, name='CharacterHealCore'),
	path('CharacterSheet/<int:CIDin>/HealRArm', views.CharacterHealRightArm, name='CharacterHealRightArm'),
	path('CharacterSheet/<int:CIDin>/HealLArm', views.CharacterHealLeftArm, name='CharacterHealLeftArm'),
	path('CharacterSheet/<int:CIDin>/HealRLeg', views.CharacterHealRightLeg, name='CharacterHealRightLeg'),
	path('CharacterSheet/<int:CIDin>/HealLLeg', views.CharacterHealLeftLeg, name='CharacterHealLeftLeg'),
	
	#surgeControl Things
	path('group/<int:GIDin>/SurgeControl', views.SurgePage, name = 'SurgePage'),
	path('group/<int:GIDin>/SurgeControl/<int:CIDin>/Save', views.SurgePageCharacterSave, name = 'SurgePageCharacterSave'),
	path('group/<int:GIDin>/SurgeControl/<int:CIDin>/incAc', views.SurgePageIncrementAction, name = 'SurgePageIncrementAction'),
	path('group/<int:GIDin>/SurgeControl/<int:CIDin>/spenAc', views.SurgePageSpendAction, name = 'SurgePageSpendAction'),
	path('group/<int:GIDin>/SurgeControl/<int:CIDin>/spenAcT', views.SurgePageSpendActionTwenty, name = 'SurgePageSpendActionTwenty'),
	path('group/<int:GIDin>/SurgeControl/<int:CIDin>/incWP', views.SurgePageIncrementWeaknessPassed, name = 'SurgePageIncrementWeaknessPassed'),
	path('group/<int:GIDin>/SurgeControl/<int:CIDin>/incWF', views.SurgePageIncrementWeaknessFailed, name = 'SurgePageIncrementWeaknessFailed'),
	path('group/<int:GIDin>/SurgeControl/<int:CIDin>/spenSt', views.SurgePageSpendStrength, name = 'SurgePageSpendStrength'),
	#login stuff
	url(r'^login/$', auth_views.LoginView.as_view(template_name='stats/login.html'), name='login'),
	url(r'^logout/$', auth_views.LogoutView.as_view(next_page ='/'), name='logout'),
]