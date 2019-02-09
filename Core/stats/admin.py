from django.contrib import admin
#imports
from .models import  *
from django.forms.models import BaseInlineFormSet, ModelForm

#Utilities-------------------------------------------------------------------------------
class AlwaysChangedModelForm(ModelForm):
	def has_changed(self):
		return True

#Status-----------------------------------------------------------------------------------
admin.site.register(Status)

#Player-----------------------------------------------------------------------------------
#Administration---------------------------------------------------------------------------
class Character_AccessInLine(admin.StackedInline):
	model = character_Access
	extra = 0
class Group_AccessInLine(admin.StackedInline):
	model = Group_Access
	extra = 0
class PlayerAdmin(admin.ModelAdmin):
	inlines = [Character_AccessInLine,Group_AccessInLine]

admin.site.register(Player,PlayerAdmin)
# admin.site.register(character_Access)
# admin.site.register(Group_Access)

#Faction-----------------------------------------------------------------------------
class Faction_ChainInline(admin.StackedInline):
	model = Faction_Chain
	fk_name = "FID"
	extra = 0
class Faction_Admin(admin.ModelAdmin):
	inlines = [Faction_ChainInline]
	
admin.site.register(Faction,Faction_Admin)

#Armor-----------------------------------------------------------------------------------
admin.site.register(Armor)
admin.site.register(Character_Equipped_Armor_Value)

#Weapon-----------------------------------------------------------------------------------
admin.site.register(Weapon_Range)
admin.site.register(Weapon_Ammo)
admin.site.register(Weapon)

#Stat & Skill-----------------------------------------------------------------------------

admin.site.register(Stat)
admin.site.register(Skill)

#Item-------------------------------------------------------------------------------------
class Character_Vehicle_FeatureInline(admin.StackedInline):
	model = Character_Vehicle_Feature
	extra = 0
class Group_Vehicle_FeatureInline(admin.StackedInline):
	model = Group_Vehicle_Feature
	extra = 0
class Character_Vehicle_StatusInline(admin.StackedInline):
	model = Character_Vehicle_Status
	extra = 0
class Group_Vehicle_StatusInline(admin.StackedInline):
	model = Group_Vehicle_Status
	extra = 0
	
class Group_VehicleAdmin(admin.ModelAdmin):
	inlines = [Group_Vehicle_FeatureInline,Group_Vehicle_StatusInline]
class Character_VehicleAdmin(admin.ModelAdmin):
	inlines = [Character_Vehicle_FeatureInline,Character_Vehicle_StatusInline]

admin.site.register(Vehicle)
admin.site.register(Character_Vehicle,Character_VehicleAdmin)
admin.site.register(Group_Vehicle,Group_VehicleAdmin)


#Currency---------------------------------------------------------------------------------
class Character_CurrencyInline(admin.StackedInline):
	model = Character_Currency
	extra = 0
class Currency_Admin(admin.ModelAdmin):
	ordering = ('Name',)
	inlines = [Character_CurrencyInline]
	
admin.site.register(Currency,Currency_Admin)

#group------------------------------------------------------------------------------------
class Group_ItemInline(admin.StackedInline):
	model = Group_Item	
	extra = 0
class Group_VehicleInline(admin.StackedInline):
	model = Group_Vehicle
	extra = 0
class Group_War_CrimeInline(admin.StackedInline):
	model = Group_War_Crime
	extra = 0	
class public_GroupInline(admin.StackedInline):
	model = public_Group
	extra = 0	
class Group_EventInline(admin.StackedInline):
	ordering = ('GC_DisplayOrder','EID')
	model = Group_Event
	extra = 0	
	
class GroupAdmin(admin.ModelAdmin):
	ordering = ('Name','GID')
	inlines = [Group_ItemInline,
	Group_VehicleInline,
	public_GroupInline,
	Group_EventInline,
	Group_War_CrimeInline,
	Group_AccessInLine]	
admin.site.register(Group,GroupAdmin)

#Character--------------------------------------------------------------------------------
class Character_StatusInline(admin.StackedInline):
	model = Character_Status
	extra = 0
class Character_DetailsInline(admin.StackedInline):
	model = Character_Details
	extra = 0
class Character_HPInline(admin.StackedInline):
	model = Character_HP
	form = AlwaysChangedModelForm
	
class Character_StatInline(admin.StackedInline):
	model = Character_Stat
	extra = 0
class Character_SkillInline(admin.StackedInline):
	model = Character_Skill	
	extra = 0
class Character_PowerInline(admin.StackedInline):
	model = Character_Power	
	extra = 0
class Character_Equipped_ArmorInline(admin.StackedInline):
	model = Character_Equipped_Armor
class Character_WeaponInline(admin.StackedInline):
	ordering = ('WID__Name',)
	model = Character_Weapon
	extra = 0
class Character_ItemInline(admin.StackedInline):
	ordering = ('Name',)
	model = Character_Item
	extra = 0
class Character_VehicleInline(admin.StackedInline):
	model = Character_Vehicle
	extra = 0
	
class Character_War_CrimeInline(admin.StackedInline):
	model = Character_War_Crime
	extra = 0	
	
	
class CharacterAdmin(admin.ModelAdmin):
	ordering = ('GID','Name')
	inlines = [
	Character_StatusInline,
	Character_DetailsInline,
	Character_HPInline,
	Character_StatInline,
	Character_SkillInline,
	Character_PowerInline,
	Character_WeaponInline,
	Character_Equipped_ArmorInline,
	Character_ItemInline,
	Character_CurrencyInline,
	Character_VehicleInline,
	Character_War_CrimeInline,
	Character_AccessInLine,
	Character_CurrencyInline]

admin.site.register(Character,CharacterAdmin)

#NPC-------------------------------------------------------------------------------------
class NPC_DispositionInline(admin.StackedInline):
	model = NPC_Disposition
	extra = 0
	
class Character_NPC_NoteInline(admin.StackedInline):
	model = Character_NPC_Note
	extra = 0
	
class NPCAdmin(admin.ModelAdmin):
	ordering = ('FID__Name','Name')
	inlines = [NPC_DispositionInline, Character_NPC_NoteInline]
admin.site.register(NPC,NPCAdmin)


#Time line-------------------------------------------------------------------------------
class NPC_EventInline(admin.StackedInline):
	model = NPC_Event
	extra = 0
	
class Faction_EventInline(admin.StackedInline):
	model = Faction_Event
	extra = 0
	
class EventAdmin(admin.ModelAdmin):
	inlines = [Group_EventInline, NPC_EventInline,Faction_EventInline]

admin.site.register(Event,EventAdmin)

#warCrimes--------------------------------------------------------------------------------

class War_CrimeAdmin(admin.ModelAdmin):
	inlines = [Character_War_CrimeInline,Group_War_CrimeInline]
admin.site.register(War_Crime,War_CrimeAdmin)

