from django.contrib import admin
#imports
from .models import  *



#Status-----------------------------------------------------------------------------------
admin.site.register(Status)

#Player-----------------------------------------------------------------------------------
admin.site.register(Player)
admin.site.register(Faction)

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

#group------------------------------------------------------------------------------------
class Group_ItemInline(admin.StackedInline):
	model = Group_Item	
	extra = 0
class Group_VehicleInline(admin.StackedInline):
	model = Group_Vehicle
	extra = 0
class War_CrimeInline(admin.StackedInline):
	model = War_Crime
	extra = 0	
	
class public_GroupInline(admin.StackedInline):
	model = public_Group
	extra = 0	
	
class GroupAdmin(admin.ModelAdmin):
	inlines = [Group_ItemInline,Group_VehicleInline,War_CrimeInline,public_GroupInline]	
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
	model = Character_Weapon
	extra = 0
class Character_ItemInline(admin.StackedInline):
	model = Character_Item
	extra = 0
class Character_VehicleInline(admin.StackedInline):
	model = Character_Vehicle
	extra = 0
	
class CharacterAdmin(admin.ModelAdmin):
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
	Character_VehicleInline]

admin.site.register(Character,CharacterAdmin)

#NPC-------------------------------------------------------------------------------------
class NPC_DispositionInline(admin.StackedInline):
	model = NPC_Disposition
	extra = 0
	
class Character_NPC_NoteInline(admin.StackedInline):
	model = Character_NPC_Note
	extra = 0
	
class NPCAdmin(admin.ModelAdmin):
	inlines = [NPC_DispositionInline, Character_NPC_NoteInline]
admin.site.register(NPC,NPCAdmin)

#Administration---------------------------------------------------------------------------
admin.site.register(character_Access)
admin.site.register(Group_Access)