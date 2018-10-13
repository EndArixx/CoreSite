from django.db import models

'''
IMPORTANT Identifiers/ForeignKeys:
	--character--
	PID = Player ID 
	CID = Character ID
	GID = Group ID
	SID = Skill ID
	STID = Stat ID
	SUID = Status ID
	--Items--
	WID = Weapon ID
	RIP = Range ID 
	AMID = Ammo ID
	AID = Armor ID
	IIP = Item ID
	BID = Ammo ID
	VID = Vehicle ID
	CVID = Character Vehicle ID
	GID = Group Vehicle ID
	--NPS--
	NID = NPC ID 
	FID = Faction ID
	WCID = War Crime ID
'''


'''
GC_notes is used by the Game Commander.
This should never show up on any pages that normal players can see. 
Every table should have this so the GC can add a note on anything.
'''

#JOHN LOOK INTO IMPORTING USER FOR PLAYER TABLE


#------------------------------------------------------------------------------	
#----------------------------- Player------------------------------------------
#------------------------------------------------------------------------------	

class Player(models.Model):
	PID = models.AutoField(primary_key=True)
	Name = models.CharField(max_length=200)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def __str__(self):
		return self.Name

		
class Faction(models.Model):
	FID = models.AutoField(primary_key=True)
	Name =  models.CharField(max_length=200)
	Image  =  models.CharField(max_length=200, blank=True, null=True)
	Details =  models.CharField(max_length=2000,blank=True, null=True)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def __str__(self):
		return self.Name
				
		
class Group(models.Model):
	GID = models.AutoField(primary_key=True)
	FID = models.ForeignKey(Faction, on_delete=models.CASCADE) 
	Name = models.CharField(max_length=200)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def __str__(self):
		return self.Name

#------------------------------------------------------------------------------	
#---------------------------- Character ---------------------------------------
#------------------------------------------------------------------------------	

class Character(models.Model):
	#names_And FKs
	CID = models.AutoField(primary_key=True)
	PID = models.ForeignKey(Player, on_delete=models.CASCADE) 
	GID = models.ForeignKey(Group, on_delete=models.CASCADE) 
	Name =  models.CharField(max_length=200)
	Image  =  models.CharField(max_length=200, blank=True, null=True)
	#Details
	Appearance  =  models.CharField(max_length=2000)
	Gender  =  models.CharField(max_length=200)
	Age = models.IntegerField(default=20)
	#Hidden data
	Max_ActionSurges_stat = models.IntegerField(default=5)
	Total_ActionSurges_stat = models.IntegerField(default=0)
	ActionSurges_stat = models.IntegerField(default=0)
	Total_MomentofStrength_stat = models.IntegerField(default=0)
	Max_MomentofStrength_stat = models.IntegerField(default=10)
	Momentofstrength_stat = models.IntegerField(default=0)
	MomentofWeakness_failed_stat = models.IntegerField(default=0)
	MomentofWeakness_passed_stat = models.IntegerField(default=0)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def __str__(self):
		return self.Name

class Character_Details(models.Model):	
	CID = models.ForeignKey(Character, on_delete=models.CASCADE)
	Details =  models.CharField(max_length=2000,blank=True, null=True)
	Hidden = models.BooleanField(default = False)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def __str__(self):
		return str(self.id) +"-" + self.CID.Name
	
class Character_HP(models.Model):
	#Character ID
	CID = models.OneToOneField(Character, on_delete=models.CASCADE, primary_key = True) 
		#Max allowed HP per slot
	Max_Head_HP = models.IntegerField(default=25)
	Max_Core_HP = models.IntegerField(default=50)
	Max_Right_Arm_HP = models.IntegerField(default=30)
	Max_Left_Arm_HP = models.IntegerField(default=30)
	Max_Right_Leg_HP = models.IntegerField(default=30)
	Max_Left_Leg_HP = models.IntegerField(default=30)
		#Current HP per slot
	Head_HP = models.IntegerField(default=Max_Head_HP.default)
	Core_HP = models.IntegerField(default=Max_Core_HP.default)
	Right_Arm_HP = models.IntegerField(default=Max_Right_Arm_HP.default)
	Left_Arm_HP = models.IntegerField(default=Max_Left_Arm_HP.default)
	Right_Leg_HP = models.IntegerField(default=Max_Right_Leg_HP.default)
	Left_Leg_HP = models.IntegerField(default=Max_Left_Leg_HP.default)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def __str__(self):
		return self.CID.Name

#------------------------------------------------------------------------------			
#----------------------------- Armor ------------------------------------------
#------------------------------------------------------------------------------	
class Armor(models.Model):
	AID = models.AutoField(primary_key=True)
	Name =  models.CharField(max_length=200)
	Value = models.IntegerField(default=10)
	Details =  models.CharField(max_length=2000,blank=True, null=True)
	Allow_Head = models.BooleanField(default = True)
	Allow_Core = models.BooleanField(default = True)
	Allow_Right_Arm = models.BooleanField(default = True)
	Allow_Left_Arm = models.BooleanField(default = True)
	Allow_Right_Leg = models.BooleanField(default = True)
	Allow_Left_Leg = models.BooleanField(default = True)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def __str__(self):
		return self.Name

class Character_Equipped_Armor(models.Model):
	CID = models.OneToOneField(Character, on_delete=models.CASCADE, primary_key = True) 
	#AID = models.ForeignKey(Armor, on_delete=models.CASCADE)
	Equiped_Head = models.ForeignKey(Armor, related_name='Head_Armor', on_delete=models.CASCADE)
	Equiped_Core = models.ForeignKey(Armor, related_name='Core_Armor', on_delete=models.CASCADE)
	Equiped_Right_Arm  = models.ForeignKey(Armor, related_name='Right_Arm_Armor', on_delete=models.CASCADE)
	Equiped_Left_Arm = models.ForeignKey(Armor, related_name='Left_Arm_Armor', on_delete=models.CASCADE)
	Equiped_Right_Leg  = models.ForeignKey(Armor, related_name='Right_Leg_Armor', on_delete=models.CASCADE)
	Equiped_Left_Leg  = models.ForeignKey(Armor, related_name='Left_Leg_Armor', on_delete=models.CASCADE)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def save(self, *args, **kwargs):
		if not self.Equiped_Head.Allow_Head:
			raise Exception('Armor ' + self.Equiped_Head.Name + ' cannot be equiped to: Head')
		if not self.Equiped_Core.Allow_Core:
			raise Exception('Armor ' + self.Equiped_Core.Name + '  cannot be equiped to: Core')
		if not self.Equiped_Right_Arm.Allow_Right_Arm:
			raise Exception('Armor ' + self.Equiped_Right_Arm.Name + '  cannot be equiped to: Right Arm')
		if not self.Equiped_Left_Arm.Allow_Left_Arm:
			raise Exception('Armor ' + self.Equiped_Left_Arm.Name + '  cannot be equiped to: Left Arm')
		if not self.Equiped_Right_Leg.Allow_Right_Leg:
			raise Exception('Armor ' + self.Equiped_Right_Leg.Name + '  cannot be equiped to: Right Leg')
		if not self.Equiped_Left_Leg.Allow_Left_Leg:
			raise Exception('Armor ' + self.Equiped_Left_Leg.Name + '  cannot be equiped to: Left Leg')
		super(Character_Equipped_Armor, self).save(*args, **kwargs)
	def __str__(self):
		return self.CID.Name
		
class Character_Equipped_Armor_Value(models.Model):
		#Charater ID
	CID = models.OneToOneField(Character, on_delete=models.CASCADE, primary_key = True) 
		#Max allowed HP per slot
	Max_Head_Armor = models.IntegerField(default=15)
	Max_Core_Armor = models.IntegerField(default=15)
	Max_Right_Arm_Armor = models.IntegerField(default=15)
	Max_Left_Arm_Armor = models.IntegerField(default=15)
	Max_Right_Leg_Armor = models.IntegerField(default=15)
	Max_Left_Leg_Armor = models.IntegerField(default=15)
		#Current HP per slot
	Head_Armor = models.IntegerField(default=Max_Head_Armor.default)
	Core_Armor = models.IntegerField(default=Max_Core_Armor.default)
	Right_Arm_Armor = models.IntegerField(default=Max_Right_Arm_Armor.default)
	Left_Arm_Armor = models.IntegerField(default=Max_Left_Arm_Armor.default)
	Right_Leg_Armor = models.IntegerField(default=Max_Right_Leg_Armor.default)
	Left_Leg_Armor = models.IntegerField(default=Max_Left_Leg_Armor.default)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def __str__(self):
		return self.CID.Name

#------------------------------------------------------------------------------			
#------------------------------ Weapon ----------------------------------------
#------------------------------------------------------------------------------		

class Weapon_Range(models.Model):
	RID = models.AutoField(primary_key=True)
	Name =  models.CharField(max_length=200)
	Distance = models.IntegerField(default=0)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def __str__(self):
		return self.Name

class Weapon_Ammo(models.Model):
	AAID = models.AutoField(primary_key=True)
	Name =  models.CharField(max_length=200)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def __str__(self):
		return self.Name
		
class Weapon(models.Model):
	WID = models.AutoField(primary_key=True)
	RID = models.ForeignKey(Weapon_Range, on_delete=models.CASCADE) 
	AAID  = models.ForeignKey(Weapon_Ammo, on_delete=models.CASCADE) 
	Name =  models.CharField(max_length=200)
	Details =  models.CharField(max_length=2000,blank=True, null=True)
	Capacity = models.IntegerField(default=1)
	Rarity  = models.IntegerField(default=1)
	Details =  models.CharField(max_length=2000,blank=True, null=True)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def __str__(self):
		return self.Name
		
class Character_Weapon(models.Model):
	CID = models.ForeignKey(Character, on_delete=models.CASCADE) 
	WID = models.ForeignKey(Weapon, on_delete=models.CASCADE) 
	Count = models.IntegerField(default=1)
	Equiped = models.BooleanField(default = False)
	Hidden = models.BooleanField(default = False)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	class Meta:
		unique_together = ('CID', 'WID')
	def __str__(self):
		return self.CID.Name + ' - '+ self.WID.Name
	

#------------------------------------------------------------------------------	
#-------------------------- Stats & Skills ------------------------------------
#------------------------------------------------------------------------------	

class Stat(models.Model):
	STID = models.AutoField(primary_key=True)
	Name =  models.CharField(max_length=200,blank=True, null=True)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def __str__(self):
		return self.Name
		
class Character_Stat(models.Model):
	CID = models.ForeignKey(Character, on_delete=models.CASCADE) 
	STID =  models.ForeignKey(Stat, on_delete=models.CASCADE) 
	Value = models.IntegerField(default=0)
	class Meta:
		unique_together = ('CID', 'STID')
		
	def __str__(self):
		return self.CID.Name + ' - '+ self.STID.Name
	
class Skill(models.Model):
	SID = models.AutoField(primary_key=True)
	STID =  models.ForeignKey(Stat, on_delete=models.CASCADE) 
	Name =  models.CharField(max_length=200,blank=True, null=True)
	Cost = models.IntegerField(default=2)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def __str__(self):
		return self.Name
		
class Character_Skill(models.Model):
	CID = models.ForeignKey(Character, on_delete=models.CASCADE) 
	SID = models.ForeignKey(Skill, on_delete=models.CASCADE) 
	Mod = models.IntegerField(default=4)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	class Meta:
		unique_together = ('CID', 'SID')
	def __str__(self):
		return self.CID.Name + ' - '+ self.SID.Name

class Character_Power(models.Model):
	CID = models.ForeignKey(Character, on_delete=models.CASCADE) 
	Name =  models.CharField(max_length=200,blank=True, null=True)
	Power_stat =  models.IntegerField(default=0)
	Details =  models.CharField(max_length=2000,blank=True, null=True)
	Hidden = models.BooleanField(default = False)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def __str__(self):
		return self.CID.Name + ' - '+ self.Name
		
#------------------------------------------------------------------------------			
#-------------------------------- Item ----------------------------------------
#------------------------------------------------------------------------------

class Character_Item(models.Model):
	IID = models.AutoField(primary_key=True)
	CID = models.ForeignKey(Character, on_delete=models.CASCADE) 
	Name =  models.CharField(max_length=200)
	Count = models.IntegerField(default=1)
	Details =  models.CharField(max_length=2000,blank=True, null=True)
	Equipable = models.BooleanField(default = False)
	Equiped = models.BooleanField(default = False)
	Hidden = models.BooleanField(default = False)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def __str__(self):
		return self.CID.Name + ' - '+ self.Name
		
class Group_Item(models.Model):
	IID = models.AutoField(primary_key=True)
	GID = models.ForeignKey(Group, on_delete=models.CASCADE) 
	Name =  models.CharField(max_length=200)
	Count = models.IntegerField(default=1)
	Details =  models.CharField(max_length=2000,blank=True, null=True)
	Equipable = models.BooleanField(default = False)
	Equiped = models.BooleanField(default = False)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def __str__(self):
		return self.GID.Name + ' - '+ self.Name


class Vehicle(models.Model):
	VID = models.AutoField(primary_key=True)
	Name =  models.CharField(max_length=200)
	Details =  models.CharField(max_length=2000,blank=True, null=True)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def __str__(self):
		return self.Name
		
class Character_Vehicle(models.Model):
	CVID = models.AutoField(primary_key=True)
	VID = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
	CID = models.ForeignKey(Character, on_delete=models.CASCADE)
	functional = models.BooleanField(default = False)
	HP = models.IntegerField(default=100)
	Max_HP = models.IntegerField(default=100)
	Hidden = models.BooleanField(default = False)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	class Meta:
		unique_together = ('VID', 'CID')
	def __str__(self):
		return self.CID.Name + ' - '+ self.VID.Name
		
class Group_Vehicle(models.Model):
	GVID = models.AutoField(primary_key=True)
	VID = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
	GID = models.ForeignKey(Group, on_delete=models.CASCADE)
	functional = models.BooleanField(default = False)
	HP = models.IntegerField(default=100)
	Max_HP = models.IntegerField(default=100)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	class Meta:
		unique_together = ('VID', 'GID')
	def __str__(self):
		return self.GID.Name + ' - '+ self.VID.Name
		
class Character_Vehicle_Feature(models.Model):
	CVID = models.ForeignKey(Character_Vehicle, on_delete=models.CASCADE)
	Name =  models.CharField(max_length=200)
	Count = models.IntegerField(default=1)
	Equiped = models.BooleanField(default = False)
	Details =  models.CharField(max_length=2000,blank=True, null=True)
	Hidden = models.BooleanField(default = False)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def __str__(self):
		return self.Name

class Group_Vehicle_Feature(models.Model):
	GVID = models.ForeignKey(Group_Vehicle, on_delete=models.CASCADE)
	Name =  models.CharField(max_length=200)
	Count = models.IntegerField(default=1)
	Equiped = models.BooleanField(default = False)
	Details =  models.CharField(max_length=2000,blank=True, null=True)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def __str__(self):
		return self.Name
	
#------------------------------------------------------------------------------			
#------------------------------ Status ----------------------------------------
#------------------------------------------------------------------------------
		
class Status(models.Model):
	SUID = models.AutoField(primary_key=True)
	Name =  models.CharField(max_length=200)
	Details =  models.CharField(max_length=2000,blank=True, null=True)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	class Meta:
		verbose_name = 'Status'
		verbose_name_plural = 'Statuses'
	def __str__(self):
		return self.Name
		
class Character_Status(models.Model):
	SUID = models.ForeignKey(Status, on_delete=models.CASCADE) 
	CID = models.ForeignKey(Character, on_delete=models.CASCADE)
	Hidden = models.BooleanField(default = False)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	class Meta:
		unique_together = ('CID', 'SUID')
	def __str__(self):
		return self.CID.Name + ' - '+ self.SUID.Name

class Character_Vehicle_Status(models.Model):
	CVID = models.ForeignKey(Character_Vehicle, on_delete=models.CASCADE)
	SUID = models.ForeignKey(Status, on_delete=models.CASCADE) 
	Hidden = models.BooleanField(default = False)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	class Meta:
		unique_together = ('CVID', 'SUID')
		verbose_name_plural = 'Character_Vehicle_statuses'
	def __str__(self):
		return self.CVID.VID.Name + ' - '+ self.SUID.Name
		
class Group_Vehicle_Status(models.Model):
	GVID = models.ForeignKey(Group_Vehicle, on_delete=models.CASCADE)
	SUID = models.ForeignKey(Status, on_delete=models.CASCADE) 
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	class Meta:
		unique_together = ('GVID', 'SUID')
		verbose_name_plural = 'Group_Vehicle_statuses'
	def __str__(self):
		return self.GVID.VID.Name + ' - '+ self.SUID.Name
#------------------------------------------------------------------------------			
#-------------------------------- NPC -----------------------------------------
#------------------------------------------------------------------------------	
		
class NPC(models.Model):
	NID = models.AutoField(primary_key=True)
	Name =  models.CharField(max_length=200)
	Image  =  models.CharField(max_length=200, blank=True, null=True)
	Alive = models.BooleanField(default = True)
	Status = models.ForeignKey(Status, on_delete=models.CASCADE)
	FID = models.ForeignKey(Faction, on_delete=models.CASCADE) 
	Details =  models.CharField(max_length=2000,blank=True, null=True)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	class Meta:
		verbose_name = 'NPC'
		verbose_name_plural = 'NPCs'
	def __str__(self):
		return self.Name
	
class NPC_Disposition(models.Model):
		#This shows if the NPC likes the player group
	NID = models.ForeignKey(NPC, on_delete=models.CASCADE)
	GID = models.ForeignKey(Group, on_delete=models.CASCADE)
	Disposition = models.IntegerField(default=0)
	Details = models.CharField(max_length=2000,blank=True, null=True)
	EmogiOverride = models.CharField(max_length=5,blank=True, null=True)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	class Meta:
		unique_together = ('NID', 'GID')
		verbose_name = 'NPC_Disposition'
		verbose_name_plural = 'NPC_Dispositions'
	def __str__(self):
		return self.NID.Name + ' - '+ self.GID.Name
	
class Character_NPC_Note(models.Model):
		#player notes about the NPC
	NID = models.ForeignKey(NPC, on_delete=models.CASCADE)
	CID = models.ForeignKey(Character, on_delete=models.CASCADE)
	Note  = models.CharField(max_length=2000)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	class Meta:
		unique_together = ('NID', 'CID')
	def __str__(self):
		return self.NID.Name + ' - '+ self.CID.Name
		
	
#------------------------------------------------------------------------------	
#----------------------------- MISC -------------------------------------------
#------------------------------------------------------------------------------
	
class War_Crime(models.Model):
	WCID =  models.AutoField(primary_key=True)
	Name =  models.CharField(max_length=200)
	GID = models.ForeignKey(Group, on_delete=models.CASCADE)
	Details =  models.CharField(max_length=2000,blank=True, null=True)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def __str__(self):
		return self.Name		
		
#------------------------------------------------------------------------------	
#----------------------- Administration ---------------------------------------
#------------------------------------------------------------------------------			
'''
This table is used to indicate what players can see what characters.
'''
class character_Access(models.Model):
	PID = models.ForeignKey(Player, on_delete=models.CASCADE) 
	CID = models.ForeignKey(Character, on_delete=models.CASCADE) 
	HasAccess = models.BooleanField(default = True)
	HasEdit = models.BooleanField(default = False)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	class Meta:
		unique_together = (('PID', 'CID'),)
	def __str__(self):
		return self.PID.Name +' - '+ self.CID.Name
		
class Group_Access(models.Model):
	PID = models.ForeignKey(Player, on_delete=models.CASCADE) 
	GID = models.ForeignKey(Group, on_delete=models.CASCADE) 
	IsPlayer = models.BooleanField(default = True)
	IsGC = models.BooleanField(default = False)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	class Meta:
		unique_together = (('PID', 'GID'),)
	def __str__(self):
		return self.PID.Name +' - '+ self.GID.Name
		
class public_Group(models.Model):
	GID = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key = True) 
	IsPublic = models.BooleanField(default = False)
	GC_notes = models.CharField(max_length=2000,blank=True, null=True)
	def __str__(self):
		return self.GID.Name
		