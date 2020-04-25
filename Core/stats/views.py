from django.shortcuts import get_object_or_404,render
from django.contrib.auth.decorators import permission_required
from django.http import Http404, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.staticfiles import finders
from django.db.models import Q
from django.urls import reverse
#models
from .models import  *

#forms
from .forms import *


#utilities-------------------------------------------------------------------
def getPid(request):
	uname = request.user.get_username()
	playA = Player.objects.get(User = request.user)
	PIDin = playA.PID
	return PIDin

def isGameCommander(request,GIDin):
	userIsGC = False
	if request.user.is_authenticated:
			accessstats = Group_Access.objects.filter(PID = getPid(request), GID = GIDin).first()
			if accessstats != None:
				userIsGC = accessstats.IsGC
	return userIsGC

def CanViewGroup(request,GIDin):
	userHasGroup = False
	publicGroups = public_Group.objects.filter(GID = GIDin).first()
	if publicGroups != None:
		userHasGroup = publicGroups.IsPublic
	if not userHasGroup:
		userHasGroup = isGameCommander(request, GIDin)
	if not userHasGroup and request.user.is_authenticated:
			accessstats = Group_Access.objects.filter(PID = getPid(request), GID = GIDin).first()
			if accessstats != None:
				userHasGroup = accessstats.IsPlayer
	return userHasGroup
	
def CanViewCharacter(request,CIDin, GIDin):
	userHasCharacter = False
	character = Character.objects.filter(CID = CIDin).first()
	if character:
		userHasCharacter = CanViewGroup(request, GIDin)
		if not userHasCharacter and request.user.is_authenticated:
			accessstats = character_Access.objects.filter(PID = getPid(request), CID = CIDin).first()
			if accessstats != None:
				userHasCharacter = accessstats.HasAccess
	return userHasCharacter
	
def CanEditCharacter(request,CIDin, GIDin):
	userCanEditCharacter = False
	character = Character.objects.filter(CID = CIDin).first()
	if isGameCommander(request, GIDin):
		userCanEditCharacter = True
	elif character:
		if request.user.is_authenticated:
			accessstats = character_Access.objects.filter(PID = getPid(request), CID = CIDin).first()
			if accessstats != None:
				userCanEditCharacter = accessstats.HasEdit
	return userCanEditCharacter
	
#----------------------------------------------------------------------------------	
#Views-----------------------------------------------------------------------------
#----------------------------------------------------------------------------------

#player handbook, this is static.
#future idea: base handbook based on game?
def ForestHandbook(request):
	return render(request, 'stats/TheForestHandBook.html')

#Index----------------------------------------
#---------------------------------------------
def index(request):
	publicGroups = public_Group.objects.filter(IsPublic = True).order_by('GID__Name')
	if request.user.is_authenticated:
		uname = request.user.get_username()
		try:
			#Get player Name
			playA = Player.objects.get(User = request.user)
			PIDin = playA.PID
			accessstats = Group_Access.objects.filter(Q(PID = PIDin) & (Q(IsPlayer = True) | Q(IsGC = True))).order_by('GID__Name')
				
			context = {'groupAccess': accessstats, 'publicGroups' : publicGroups}
			return render(request, 'stats/index.html', context)
		except Exception as e:
			raise Http404("Error - "+ str(e))
	else:
		context = {'publicGroups' : publicGroups}
		return render(request, 'stats/indexnolog.html',context)

#Groups---------------------------------------
#----------------------------------------------
def group(request, GIDin):
	if CanViewGroup(request, GIDin):
		theGroup = get_object_or_404(Group,GID = GIDin)
		chractersInGroup = Character_Group.objects.filter(GID = GIDin)
		isGC = isGameCommander(request,GIDin)
		return render(request, 'stats/group.html', {'chractersInGroup': chractersInGroup, 'Group':theGroup, 'isGC':isGC})
	else:
		return HttpResponseRedirect(reverse('index'))

#NPC stuff------------------------------------
#---------------------------------------------
def NPClist(request, GIDin):
	if CanViewGroup(request,GIDin):
		theGroup = get_object_or_404(Group,GID = GIDin)
		NPC_dis = NPC_Disposition.objects.filter(GID = GIDin).order_by('NID__FID__Name','NID__Name')
		NPC_fac = Faction.objects.filter(FID__in = set(NPC_dis.values_list('NID__FID', flat=True))).order_by('Name')
		return render(request, 'stats/NPCList.html', {'Group':theGroup,'NPCList':NPC_dis, 'NPCFaction':NPC_fac})
	else:
		return HttpResponseRedirect(reverse('index'))
	
def NPCpage(request, GIDin,NIDin):
	if CanViewGroup(request,GIDin):
		theGroup = get_object_or_404(Group,GID = GIDin)
		NPC_dist = get_object_or_404(NPC_Disposition,GID = GIDin, NID = NIDin)
		
		if NPC_dist.NID.Image:		
			image = finders.find('stats/npc/'+NPC_dist.NID.Image)
			if not image:
				NPC_dist.NID.Image = 'invalid.png'
		
		return render(request, 'stats/NPC.html', {'Group':theGroup,'NPC':NPC_dist})
	else:
		return HttpResponseRedirect(reverse('index'))

#Events----------------------------------------
#----------------------------------------------		
def EventTimeline(request, GIDin):
	if CanViewGroup(request,GIDin):
		try:
			theGroup = get_object_or_404(Group,GID = GIDin)
		except theGroup.DoesNotExist:
			raise Http404("group does not exist")
		Events = Group_Event.objects.filter(GID = GIDin).order_by('GC_DisplayOrder')
		return render(request, 'stats/eventTimeline.html', {'Group':theGroup,'Events':Events})
	else:
		return HttpResponseRedirect(reverse('index'))
	
def EventPage(request, GIDin,EIDin):
	if CanViewGroup(request,GIDin):
		theGroup = get_object_or_404(Group,GID = GIDin)
		Event = get_object_or_404(Group_Event,GID = GIDin, EID = EIDin)
		
		#using a filter so It only shows NPC's the group can see.
		NPCEvent = NPC_Event.objects.filter(EID = EIDin).order_by('NID__Name')
		NPCList = NPC_Disposition.objects.filter(GID = GIDin,NID__in = set(NPCEvent.values_list('NID', flat=True))).order_by('NID__Name')
		
		FactionList = Faction_Event.objects.filter(EID = EIDin).order_by('FID__Name')
		# if NPC_dist.NID.Image:		
			# image = finders.find('stats/npc/'+NPC_dist.NID.Image)
			# if not image:
				# NPC_dist.NID.Image = 'invalid.png'
		
		return render(request, 'stats/event.html', {'Group':theGroup,'event':Event,'NPCList':NPCList,'FactionList':FactionList})
	else:
		return HttpResponseRedirect(reverse('index'))
		
		
#Faction--------------------------------------
#---------------------------------------------
def FactionList(request, GIDin):
	#this isn't ready yet.
	raise Http404()
	
def FactionPage(request, GIDin,FIDin):
	if CanViewGroup(request,GIDin):
		theGroup = get_object_or_404(Group,GID = GIDin)
		theFaction = get_object_or_404(Faction,FID = FIDin)
		superFactions = Faction_Chain.objects.filter(FID = FIDin).order_by('FID__Name')
		subFactions  = Faction_Chain.objects.filter(SuperFID = FIDin).order_by('FID__Name')

		#using a filter so It only shows NPC's the group can see.
		NPCPrefilter = NPC.objects.filter(FID = FIDin).order_by('Name')
		NPCList = NPC_Disposition.objects.filter(GID = GIDin,NID__in = set(NPCPrefilter.values_list('NID', flat=True))).order_by('NID__Name')

		return render(request, 'stats/faction.html', {
		'Group':theGroup,'Faction':theFaction,
		'superFactions':superFactions,
		'subFactions':subFactions,
		'NPCList':NPCList})
	else:
		return HttpResponseRedirect(reverse('index'))

	
		
#Player---------------------------------------
#---------------------------------------------
def player(request, PID):
	#Jaki Validate player.
	return HttpResponse("You're looking at the characters of %s." % PID)
	
#Character------------------------------------
#---------------------------------------------
def Character_Sheet(request, GIDin, CIDin):
	Access = CanViewCharacter(request, CIDin, GIDin)
	htmlpage = 'stats/{0}.html'
	if not Access:
		return HttpResponseRedirect(reverse('index'))

	theGroup = get_object_or_404(Group,GID = GIDin)
	character = get_object_or_404(Character,CID = CIDin)
	isGC = isGameCommander(request, GIDin)
	redirectID = 0
	try:
		#Some Things may be hidden from everyone but the player owner and the DB.
		if CanEditCharacter(request, CIDin, GIDin):
			characterStatus = Character_Status.objects.filter(CID = CIDin).order_by('SUID__Name')
			characterPower = Character_Power.objects.filter(CID = CIDin).order_by('Name')	
			characterWeapon = Character_Weapon.objects.filter(CID = CIDin).order_by('WID__Name')	
			characterGear = Character_Item.objects.filter(CID = CIDin, Equipable = True).order_by('Name')	
			characterItem = Character_Item.objects.filter(CID = CIDin, Equipable = False).order_by('Name')	
			characterDetails = Character_Details.objects.filter(CID = CIDin)	
			characterMoney = Character_Currency.objects.filter(CID = CIDin).order_by('-MID__Value')
			htmlpage  = htmlpage.format('CharacterNewCon')
		else:
			characterStatus = Character_Status.objects.filter(CID = CIDin, Hidden = False).order_by('SUID__Name')
			characterPower = Character_Power.objects.filter(CID = CIDin, Hidden = False).order_by('Name')	
			characterWeapon = Character_Weapon.objects.filter(CID = CIDin, Hidden = False).order_by('WID__Name')	
			characterGear = Character_Item.objects.filter(CID = CIDin, Equipable = True, Hidden = False).order_by('Name')	
			characterItem = Character_Item.objects.filter(CID = CIDin, Equipable = False, Hidden = False).order_by('Name')	
			characterDetails = Character_Details.objects.filter(CID = CIDin, Hidden = False)
			characterMoney = Character_Currency.objects.filter(CID = CIDin, Hidden = False).order_by('-MID__Value')
			htmlpage = htmlpage.format('CharacterNewLim')
			
		#These tables do not have a hidden column. 
		characterHP = get_object_or_404(Character_HP,CID = CIDin)	
			#Jaki this is dirty
		characterArmor = Character_Equipped_Armor_Value.objects.filter(CID = CIDin).first()
		characterArmorName  = Character_Equipped_Armor.objects.filter(CID = CIDin).first()
		groupMembers = Character_Group.objects.filter(GID = GIDin)
		characterStat = Character_Stat.objects.filter(CID = CIDin).order_by('STID__Name')	
		characterSkill = Character_Skill.objects.filter(CID = CIDin).order_by('SID__Name')	
		
		#forms
		hpDamageForm = HPFormDamage()
		hpHealForm = HPFormHeal()
		hpHealAllForm = HPAllForm()
		armorAllForm = ArmorAllForm()
		#redirect
		Redirector  = reverse('character',  kwargs={'GIDin': GIDin,'CIDin': CIDin})
		if not character.Image:		
			character.Image = 'default.png'
		else:
			image = finders.find('stats/character/'+character.Image)
			if not image:
				character.Image = 'invalid.png'
				
			
	except Exception as e:
		print("ERROR: "+str(e))
		raise Http404("Error loading character: " + str(character.Name))

	return render(request, htmlpage, {
	'character': character,
	'characterHP': characterHP,
	'characterArmor': characterArmor,
	'characterArmorName': characterArmorName,
	'theGroup': theGroup,
	'groupMembers': groupMembers,
	'characterStat': characterStat,
	'characterSkill': characterSkill,
	'characterPower': characterPower,
	'characterWeapon': characterWeapon,
	'characterGear': characterGear,
	'characterItem': characterItem,
	'characterDetails': characterDetails,
	'characterMoney': characterMoney,
	'characterStatus': characterStatus,
	'hpDamageForm': hpDamageForm,
	'hpHealForm': hpHealForm,
	'hpHealAllForm': hpHealAllForm,
	'armorAllForm':armorAllForm,
	'Redirector':Redirector,
	'isGC':isGC})		
	

#Character Health------------------------------	
#----------------------------------------------	
def getRedirectOrHome(request):
	redirect = reverse('index')
	if request.method == 'POST':
		redirect = request.POST.get('Redirect', reverse('index'))
	return redirect

def HealthPage(request, GIDin):
	if CanViewGroup(request, GIDin):
		#grab the data
		theGroup = get_object_or_404(Group,GID = GIDin)
		charactersInGroup = Character_Group.objects.filter(GID = GIDin)
		characterHPset = Character_HP.objects.filter(CID__in = set(charactersInGroup.values_list('CID', flat=True)))	
		characterArmorset = Character_Equipped_Armor_Value.objects.filter(CID__in = set(charactersInGroup.values_list('CID', flat=True)))
		characterArmorNameset  = Character_Equipped_Armor.objects.filter(CID__in = set(charactersInGroup.values_list('CID', flat=True)))
		
		#filter them based on if player can edit or not.
		charactersCon = set()
		charactersLim = set()
		for char in charactersInGroup:
			if CanEditCharacter(request, char.CID.CID, GIDin):
				charactersCon.add(char.CID)
			else:
				charactersLim.add(char.CID)
				
		#Sort them for display
		charactersCon = sorted(charactersCon, key=lambda o: o.Name)		
		charactersLim = sorted(charactersLim, key=lambda o: o.Name)	
		
		#forms
		hpDamageForm = HPFormDamage()
		hpHealForm = HPFormHeal()
		hpHealAllForm = HPAllForm()
		armorAllForm = ArmorAllForm()		
		#redirect control
		Redirector  = reverse('HealthPage',  kwargs={'GIDin': GIDin})
		
		context = {'charactersCon': charactersCon,
			'charactersLim':charactersLim,
			'characterHPset':characterHPset,
			'characterArmorset':characterArmorset,
			'characterArmorNameset':characterArmorNameset,
			'hpDamageForm': hpDamageForm,
			'hpHealForm': hpHealForm,
			'hpHealAllForm': hpHealAllForm,
			'armorAllForm':armorAllForm,
			'Redirector':Redirector,
			'theGroup':theGroup}
		return render(request, 'stats/healthControl.html', context)	
	else:
		return HttpResponseRedirect(reverse('index'))

def CharacterHPFullHeal(request, GIDin, CIDin):
	if CanEditCharacter(request,CIDin, GIDin):
		characterhp = get_object_or_404(Character_HP, CID = CIDin)
		if request.method == 'POST':
			characterhp.Head_HP = characterhp.Max_Head_HP
			characterhp.Core_HP  = characterhp.Max_Core_HP 
			characterhp.Right_Arm_HP  = characterhp.Max_Right_Arm_HP 
			characterhp.Left_Arm_HP  = characterhp.Max_Left_Arm_HP 
			characterhp.Right_Leg_HP  = characterhp.Max_Right_Leg_HP 
			characterhp.Left_Leg_HP  = characterhp.Max_Left_Leg_HP 
			
			characterhp.Temp_Head_HP = 0
			characterhp.Temp_Core_HP = 0
			characterhp.Temp_Right_Arm_HP = 0
			characterhp.Temp_Left_Arm_HP = 0
			characterhp.Temp_Right_Leg_HP = 0
			characterhp.Temp_Left_Leg_HP = 0
			
			saveHP(characterhp)
		return HttpResponseRedirect(getRedirectOrHome(request))
	else:
		return HttpResponseRedirect(reverse('index'))
		
def CharacterArmorReset(request, GIDin, CIDin):
	if CanEditCharacter(request,CIDin, GIDin):
		characterArmorValue = Character_Equipped_Armor_Value.objects.get(CID = CIDin)
		characterArmorName  = Character_Equipped_Armor.objects.get(CID = CIDin)
		if request.method == 'POST':
			#set maximum values
			characterArmorValue.Max_Head_Armor 		= characterArmorName.Equiped_Head.Value
			characterArmorValue.Max_Core_Armor 		= characterArmorName.Equiped_Core.Value
			characterArmorValue.Max_Right_Arm_Armor = characterArmorName.Equiped_Right_Arm.Value
			characterArmorValue.Max_Left_Arm_Armor 	= characterArmorName.Equiped_Left_Arm.Value
			characterArmorValue.Max_Right_Leg_Armor = characterArmorName.Equiped_Right_Leg.Value
			characterArmorValue.Max_Left_Leg_Armor 	= characterArmorName.Equiped_Left_Leg.Value
			
			#repair armor
			characterArmorValue.Head_Armor 		= characterArmorValue.Max_Head_Armor
			characterArmorValue.Core_Armor 		= characterArmorValue.Max_Core_Armor
			characterArmorValue.Right_Arm_Armor = characterArmorValue.Max_Right_Arm_Armor
			characterArmorValue.Left_Arm_Armor 	= characterArmorValue.Max_Left_Arm_Armor
			characterArmorValue.Right_Leg_Armor = characterArmorValue.Max_Right_Leg_Armor
			characterArmorValue.Left_Leg_Armor 	= characterArmorValue.Max_Left_Leg_Armor
			
			saveArmor(characterArmorValue)
		return HttpResponseRedirect(getRedirectOrHome(request))
	else:
		return HttpResponseRedirect(reverse('index'))

def checkHP(characterhp):	
	if characterhp.Head_HP > characterhp.Max_Head_HP:
		characterhp.Head_HP = characterhp.Max_Head_HP
	elif characterhp.Head_HP < 0:
		characterhp.Head_HP = 0
	if characterhp.Core_HP  > characterhp.Max_Core_HP:
		characterhp.Core_HP  = characterhp.Max_Core_HP 
	elif characterhp.Core_HP < 0:
		characterhp.Core_HP  = 0
	if characterhp.Right_Arm_HP  > characterhp.Max_Right_Arm_HP:
		characterhp.Right_Arm_HP  = characterhp.Max_Right_Arm_HP 
	elif characterhp.Right_Arm_HP < 0:
		characterhp.Right_Arm_HP = 0
	if characterhp.Left_Arm_HP  > characterhp.Max_Left_Arm_HP:
		characterhp.Left_Arm_HP  = characterhp.Max_Left_Arm_HP 
	elif characterhp.Left_Arm_HP < 0:
		characterhp.Left_Arm_HP = 0
	if characterhp.Right_Leg_HP  > characterhp.Max_Right_Leg_HP:
		characterhp.Right_Leg_HP  = characterhp.Max_Right_Leg_HP 
	elif characterhp.Right_Leg_HP < 0:
		characterhp.Right_Leg_HP = 0
	if characterhp.Left_Leg_HP  > characterhp.Max_Left_Leg_HP:
		characterhp.Left_Leg_HP  = characterhp.Max_Left_Leg_HP
	elif characterhp.Left_Leg_HP < 0:
		characterhp.Left_Leg_HP = 0		
	
	if characterhp.Temp_Head_HP < 0:
		characterhp.Temp_Head_HP = 0
	if characterhp.Temp_Core_HP < 0:
		characterhp.Temp_Core_HP = 0
	if characterhp.Temp_Right_Arm_HP < 0:
		haracterhp.Temp_Right_Arm_HP = 0
	if characterhp.Temp_Left_Arm_HP < 0:
		characterhp.Temp_Left_Arm_HP = 0
	if characterhp.Temp_Right_Leg_HP < 0:
		characterhp.Temp_Right_Leg_HP = 0
	if characterhp.Temp_Left_Leg_HP < 0:
		characterhp.Temp_Left_Leg_HP = 0
	
		
def checkArmor(characterArmorValue):	
	if characterArmorValue.Head_Armor > characterArmorValue.Max_Head_Armor:
		characterArmorValue.Head_Armor = characterArmorValue.Max_Head_Armor
	elif characterArmorValue.Head_Armor < 0:
		characterArmorValue.Head_Armor = 0
	if characterArmorValue.Core_Armor > characterArmorValue.Max_Core_Armor:
		characterArmorValue.Core_Armor = characterArmorValue.Max_Core_Armor
	elif characterArmorValue.Core_Armor < 0:
		characterArmorValue.Core_Armor = 0
	if characterArmorValue.Right_Arm_Armor > characterArmorValue.Max_Right_Arm_Armor:
		characterArmorValue.Right_Arm_Armor = characterArmorValue.Max_Right_Arm_Armor
	elif characterArmorValue.Right_Arm_Armor< 0:
		characterArmorValue.Right_Arm_Armor = 0
	if characterArmorValue.Left_Arm_Armor > characterArmorValue.Max_Left_Arm_Armor:
		characterArmorValue.Left_Arm_Armor = characterArmorValue.Max_Left_Arm_Armor
	elif characterArmorValue.Left_Arm_Armor < 0:
		characterArmorValue.Left_Arm_Armor = 0
	if characterArmorValue.Right_Leg_Armor > characterArmorValue.Max_Right_Leg_Armor:
		characterArmorValue.Right_Leg_Armor = characterArmorValue.Max_Right_Leg_Armor
	elif characterArmorValue.Right_Leg_Armor < 0:
		characterArmorValue.Right_Leg_Armor = 0
	if characterArmorValue.Left_Leg_Armor > characterArmorValue.Max_Left_Leg_Armor:
		characterArmorValue.Left_Leg_Armor = characterArmorValue.Max_Left_Leg_Armor
	elif characterArmorValue.Left_Leg_Armor < 0:
		characterArmorValue.Left_Leg_Armor = 0
		
def saveHP(characterhp):
	checkHP(characterhp)
	characterhp.save()
	
def saveArmor(characterArmorValue):
	checkArmor(characterArmorValue)
	characterArmorValue.save()

def CharacterHPHealALL(request, GIDin, CIDin):	
	if CanEditCharacter(request,CIDin, GIDin):
		characterhp = get_object_or_404(Character_HP, CID = CIDin)
		if request.method == 'POST':
			form = HPAllForm(request.POST)
			if form.is_valid():
				if( form.cleaned_data['OverHeal_f']):
					if(form.cleaned_data['AddorO_f'] == 'Add_f'):
						if form.cleaned_data['HeadHP_f'] != None:
							characterhp.Temp_Head_HP += form.cleaned_data['HeadHP_f']
						if form.cleaned_data['CoreHP_f'] != None:
							characterhp.Temp_Core_HP += form.cleaned_data['CoreHP_f']
						if form.cleaned_data['ArmRightHP_f'] != None:
							characterhp.Temp_Right_Arm_HP += form.cleaned_data['ArmRightHP_f']
						if form.cleaned_data['ArmLeftHP_f'] != None:
							characterhp.Temp_Left_Arm_HP += form.cleaned_data['ArmLeftHP_f']
						if form.cleaned_data['LegRightHP_f'] != None:
							characterhp.Temp_Right_Leg_HP += form.cleaned_data['LegRightHP_f']
						if form.cleaned_data['LegLeftHP_f'] != None:
							characterhp.Temp_Left_Leg_HP += form.cleaned_data['LegLeftHP_f']
					if(form.cleaned_data['AddorO_f'] == 'Override_f'):
						if form.cleaned_data['HeadHP_f'] != None:
							characterhp.Temp_Head_HP = form.cleaned_data['HeadHP_f']
						if form.cleaned_data['CoreHP_f'] != None:
							characterhp.Temp_Core_HP = form.cleaned_data['CoreHP_f']
						if form.cleaned_data['ArmRightHP_f'] != None:
							characterhp.Temp_Right_Arm_HP = form.cleaned_data['ArmRightHP_f']
						if form.cleaned_data['ArmLeftHP_f'] != None:
							characterhp.Temp_Left_Arm_HP = form.cleaned_data['ArmLeftHP_f']
						if form.cleaned_data['LegRightHP_f'] != None:
							characterhp.Temp_Right_Leg_HP = form.cleaned_data['LegRightHP_f']
						if form.cleaned_data['LegLeftHP_f'] != None:
							characterhp.Temp_Left_Leg_HP = form.cleaned_data['LegLeftHP_f']
				else:
					if(form.cleaned_data['AddorO_f'] == 'Add_f'):
						if form.cleaned_data['HeadHP_f'] != None:
							characterhp.Head_HP += form.cleaned_data['HeadHP_f']
						if form.cleaned_data['CoreHP_f'] != None:
							characterhp.Core_HP += form.cleaned_data['CoreHP_f']
						if form.cleaned_data['ArmRightHP_f'] != None:
							characterhp.Right_Arm_HP += form.cleaned_data['ArmRightHP_f']
						if form.cleaned_data['ArmLeftHP_f'] != None:
							characterhp.Left_Arm_HP += form.cleaned_data['ArmLeftHP_f']
						if form.cleaned_data['LegRightHP_f'] != None:
							characterhp.Right_Leg_HP += form.cleaned_data['LegRightHP_f']
						if form.cleaned_data['LegLeftHP_f'] != None:
							characterhp.Left_Leg_HP += form.cleaned_data['LegLeftHP_f']
					if(form.cleaned_data['AddorO_f'] == 'Override_f'):
						if form.cleaned_data['HeadHP_f'] != None:
							characterhp.Head_HP = form.cleaned_data['HeadHP_f']
						if form.cleaned_data['CoreHP_f'] != None:
							characterhp.Core_HP = form.cleaned_data['CoreHP_f']
						if form.cleaned_data['ArmRightHP_f'] != None:
							characterhp.Right_Arm_HP = form.cleaned_data['ArmRightHP_f']
						if form.cleaned_data['ArmLeftHP_f'] != None:
							characterhp.Left_Arm_HP = form.cleaned_data['ArmLeftHP_f']
						if form.cleaned_data['LegRightHP_f'] != None:
							characterhp.Right_Leg_HP = form.cleaned_data['LegRightHP_f']
						if form.cleaned_data['LegLeftHP_f'] != None:
							characterhp.Left_Leg_HP = form.cleaned_data['LegLeftHP_f']	
			saveHP(characterhp)
		return HttpResponseRedirect(getRedirectOrHome(request))
	else:
		return HttpResponseRedirect(reverse('index'))

def CharacterArmorALL(request, GIDin, CIDin):	
	if CanEditCharacter(request,CIDin, GIDin):
		characterArmorValue = Character_Equipped_Armor_Value.objects.get(CID = CIDin)
		characterArmorName  = Character_Equipped_Armor.objects.get(CID = CIDin)
		if request.method == 'POST':
			#set maximum values
			characterArmorValue.Max_Head_Armor 		= characterArmorName.Equiped_Head.Value
			characterArmorValue.Max_Core_Armor 		= characterArmorName.Equiped_Core.Value
			characterArmorValue.Max_Right_Arm_Armor = characterArmorName.Equiped_Right_Arm.Value
			characterArmorValue.Max_Left_Arm_Armor 	= characterArmorName.Equiped_Left_Arm.Value
			characterArmorValue.Max_Right_Leg_Armor = characterArmorName.Equiped_Right_Leg.Value
			characterArmorValue.Max_Left_Leg_Armor 	= characterArmorName.Equiped_Left_Leg.Value
			
			form = ArmorAllForm(request.POST)
			if form.is_valid():
				if(form.cleaned_data['AddorO_f'] == 'Add_f'):
					if form.cleaned_data['HeadArmor_f'] != None:
						characterArmorValue.Head_Armor += form.cleaned_data['HeadArmor_f']
					if form.cleaned_data['CoreArmor_f'] != None:
						characterArmorValue.Core_Armor += form.cleaned_data['CoreArmor_f']
					if form.cleaned_data['ArmRightArmor_f'] != None:
						characterArmorValue.Right_Arm_Armor += form.cleaned_data['ArmRightArmor_f']
					if form.cleaned_data['ArmLeftArmor_f'] != None:
						characterArmorValue.Left_Arm_Armor += form.cleaned_data['ArmLeftArmor_f']
					if form.cleaned_data['LegRightArmor_f'] != None:
						characterArmorValue.Right_Leg_Armor += form.cleaned_data['LegRightArmor_f']
					if form.cleaned_data['LegLeftArmor_f'] != None:
						characterArmorValue.Left_Leg_Armor += form.cleaned_data['LegLeftArmor_f']
				if(form.cleaned_data['AddorO_f'] == 'Override_f'):
					if form.cleaned_data['HeadArmor_f'] != None:
						characterArmorValue.Head_Armor = form.cleaned_data['HeadArmor_f']
					if form.cleaned_data['CoreArmor_f'] != None:
						characterArmorValue.Core_Armor = form.cleaned_data['CoreArmor_f']
					if form.cleaned_data['ArmRightArmor_f'] != None:
						characterArmorValue.Right_Arm_Armor = form.cleaned_data['ArmRightArmor_f']
					if form.cleaned_data['ArmLeftArmor_f'] != None:
						characterArmorValue.Left_Arm_Armor = form.cleaned_data['ArmLeftArmor_f']
					if form.cleaned_data['LegRightArmor_f'] != None:
						characterArmorValue.Right_Leg_Armor = form.cleaned_data['LegRightArmor_f']
					if form.cleaned_data['LegLeftArmor_f'] != None:
						characterArmorValue.Left_Leg_Armor = form.cleaned_data['LegLeftArmor_f']		
			saveArmor(characterArmorValue)
		return HttpResponseRedirect(getRedirectOrHome(request))
	else:
		return HttpResponseRedirect(reverse('index'))		
		
def CharacterDamageHead(request, GIDin, CIDin):
	if CanEditCharacter(request,CIDin, GIDin):
		characterhp = get_object_or_404(Character_HP, CID = CIDin)
		characterArmorValue = Character_Equipped_Armor_Value.objects.filter(CID = CIDin).first()
		if request.method == 'POST':
			form = HPFormDamage(request.POST)
			if form.is_valid():
				rem = form.cleaned_data['Value_f']
				if not form.cleaned_data['skipArmor_f'] and characterArmorValue and characterArmorValue.Head_Armor > 0:
					rem = rem - characterArmorValue.Head_Armor
					characterArmorValue.Head_Armor += -1
				if(characterhp.Temp_Head_HP > 0 and rem > 0):
					rem2 = rem
					rem = rem - characterhp.Temp_Head_HP
					characterhp.Temp_Head_HP += - rem2
					if(characterhp.Temp_Head_HP < 0):
						characterhp.Temp_Head_HP = 0
				if(0 < rem):
					characterhp.Head_HP = characterhp.Head_HP - rem
					if(characterhp.Head_HP < 0):
						characterhp.Head_HP = 0
				
				saveHP(characterhp)
				saveArmor(characterArmorValue)
		return HttpResponseRedirect(getRedirectOrHome(request))
	else:
		return HttpResponseRedirect(reverse('index'))
		
def CharacterHealHead(request, GIDin, CIDin):
	if CanEditCharacter(request,CIDin, GIDin):
		characterhp = get_object_or_404(Character_HP, CID = CIDin)
		if request.method == 'POST':
			form = HPFormHeal(request.POST)
			if form.is_valid():
				if form.cleaned_data['OverHeal_f']:
					characterhp.Temp_Head_HP += form.cleaned_data['Value_f']
				else:
					hp = form.cleaned_data['Value_f'] + characterhp.Head_HP 
					if(hp < characterhp.Max_Head_HP):
						characterhp.Head_HP = hp
					else:
						characterhp.Head_HP = characterhp.Max_Head_HP
			saveHP(characterhp)
		return HttpResponseRedirect(getRedirectOrHome(request))
	else:
		return HttpResponseRedirect(reverse('index'))
		
def CharacterDamageCore(request, GIDin, CIDin):
	if CanEditCharacter(request,CIDin, GIDin):
		characterhp = get_object_or_404(Character_HP, CID = CIDin)
		characterArmorValue = Character_Equipped_Armor_Value.objects.filter(CID = CIDin).first()
		if request.method == 'POST':
			form = HPFormDamage(request.POST)
			if form.is_valid():
				rem = form.cleaned_data['Value_f']
				if not form.cleaned_data['skipArmor_f'] and characterArmorValue and characterArmorValue.Core_Armor > 0:
					rem = rem - characterArmorValue.Core_Armor
					characterArmorValue.Core_Armor += -1
				if(characterhp.Temp_Core_HP > 0 and rem > 0):
					rem2 = rem
					rem = rem - characterhp.Temp_Core_HP
					characterhp.Temp_Core_HP += - rem2
					if(characterhp.Temp_Core_HP < 0):
						characterhp.Temp_Core_HP = 0					
				if(0 < rem):
					characterhp.Core_HP = characterhp.Core_HP - rem
					if(characterhp.Core_HP < 0):
						characterhp.Core_HP = 0
				
				saveHP(characterhp)
				saveArmor(characterArmorValue)
		return HttpResponseRedirect(getRedirectOrHome(request))
	else:
		return HttpResponseRedirect(reverse('index'))
		
def CharacterHealCore(request, GIDin, CIDin):
	if CanEditCharacter(request,CIDin, GIDin):
		characterhp = get_object_or_404(Character_HP, CID = CIDin)
		if request.method == 'POST':
			form = HPFormHeal(request.POST)
			if form.is_valid():
				
				if form.cleaned_data['OverHeal_f']:
					characterhp.Temp_Core_HP += form.cleaned_data['Value_f']
				else:
					hp = form.cleaned_data['Value_f'] + characterhp.Core_HP 
					if(hp < characterhp.Max_Core_HP):
						characterhp.Core_HP = hp
					else:
						characterhp.Core_HP = characterhp.Max_Core_HP
				saveHP(characterhp)
		return HttpResponseRedirect(getRedirectOrHome(request))
	else:
		return HttpResponseRedirect(reverse('index'))		

def CharacterDamageRightArm(request, GIDin, CIDin):
	if CanEditCharacter(request,CIDin, GIDin):
		characterhp = get_object_or_404(Character_HP, CID = CIDin)
		characterArmorValue = Character_Equipped_Armor_Value.objects.filter(CID = CIDin).first()
		if request.method == 'POST':
			form = HPFormDamage(request.POST)
			if form.is_valid():
				rem = form.cleaned_data['Value_f']
				if not form.cleaned_data['skipArmor_f'] and characterArmorValue and characterArmorValue.Right_Arm_Armor > 0:
					rem = rem - characterArmorValue.Right_Arm_Armor
					characterArmorValue.Right_Arm_Armor += -1
				if(characterhp.Temp_Right_Arm_HP > 0 and rem > 0):
					rem2 = rem
					rem = rem - characterhp.Temp_Right_Arm_HP
					characterhp.Temp_Right_Arm_HP += - rem2
					if(characterhp.Temp_Right_Arm_HP < 0):
						characterhp.Temp_Right_Arm_HP = 0
				if(0 < rem):
					characterhp.Right_Arm_HP = characterhp.Right_Arm_HP - rem
					if(characterhp.Right_Arm_HP < 0):
						characterhp.Right_Arm_HP = 0
				
				saveHP(characterhp)
				saveArmor(characterArmorValue)
		return HttpResponseRedirect(getRedirectOrHome(request))
	else:
		return HttpResponseRedirect(reverse('index'))
		
def CharacterHealRightArm(request, GIDin, CIDin):
	if CanEditCharacter(request,CIDin, GIDin):
		characterhp = get_object_or_404(Character_HP, CID = CIDin)
		if request.method == 'POST':
			form = HPFormHeal(request.POST)
			if form.is_valid():
				if form.cleaned_data['OverHeal_f']:
					characterhp.Temp_Right_Arm_HP += form.cleaned_data['Value_f']
				else:
					hp = form.cleaned_data['Value_f'] + characterhp.Right_Arm_HP 
					if(hp < characterhp.Max_Right_Arm_HP):
						characterhp.Right_Arm_HP = hp
					else:
						characterhp.Right_Arm_HP = characterhp.Max_Right_Arm_HP
				saveHP(characterhp)
		return HttpResponseRedirect(getRedirectOrHome(request))
	else:
		return HttpResponseRedirect(reverse('index'))		
		
def CharacterDamageLeftArm(request, GIDin, CIDin):
	if CanEditCharacter(request,CIDin, GIDin):
		characterhp = get_object_or_404(Character_HP, CID = CIDin)
		characterArmorValue = Character_Equipped_Armor_Value.objects.filter(CID = CIDin).first()
		if request.method == 'POST':
			form = HPFormDamage(request.POST)
			if form.is_valid():
				rem = form.cleaned_data['Value_f']
				if not form.cleaned_data['skipArmor_f'] and characterArmorValue and characterArmorValue.Left_Arm_Armor > 0:
					rem = rem - characterArmorValue.Left_Arm_Armor
					characterArmorValue.Left_Arm_Armor += -1
				if(characterhp.Temp_Left_Arm_HP > 0 and rem > 0):
					rem2 = rem
					rem = rem - characterhp.Temp_Left_Arm_HP
					characterhp.Temp_Left_Arm_HP += - rem2
					if(characterhp.Temp_Left_Arm_HP < 0):
						characterhp.Temp_Left_Arm_HP = 0
				if(0 < rem):
					characterhp.Left_Arm_HP = characterhp.Left_Arm_HP - rem
					if(characterhp.Left_Arm_HP < 0 ):
						characterhp.Left_Arm_HP = 0
				
				saveHP(characterhp)
				saveArmor(characterArmorValue)
		return HttpResponseRedirect(getRedirectOrHome(request))
	else:
		return HttpResponseRedirect(reverse('index'))
		
def CharacterHealLeftArm(request, GIDin, CIDin):
	if CanEditCharacter(request,CIDin, GIDin):
		characterhp = get_object_or_404(Character_HP, CID = CIDin)
		if request.method == 'POST':
			form = HPFormHeal(request.POST)
			if form.is_valid():
				if form.cleaned_data['OverHeal_f']:
					characterhp.Temp_Left_Arm_HP += form.cleaned_data['Value_f']
				else:
					hp = form.cleaned_data['Value_f'] + characterhp.Left_Arm_HP 
					if(hp < characterhp.Max_Left_Arm_HP):
						characterhp.Left_Arm_HP = hp
					else:
						characterhp.Left_Arm_HP = characterhp.Max_Left_Arm_HP
				saveHP(characterhp)
		return HttpResponseRedirect(getRedirectOrHome(request))
	else:
		return HttpResponseRedirect(reverse('index'))		
		
def CharacterDamageRightLeg(request, GIDin, CIDin):
	if CanEditCharacter(request,CIDin, GIDin):
		characterhp = get_object_or_404(Character_HP, CID = CIDin)
		characterArmorValue = Character_Equipped_Armor_Value.objects.filter(CID = CIDin).first()
		if request.method == 'POST':
			form = HPFormDamage(request.POST)
			if form.is_valid():
				rem = form.cleaned_data['Value_f']
				if not form.cleaned_data['skipArmor_f'] and characterArmorValue and characterArmorValue.Right_Leg_Armor > 0:
					rem = rem - characterArmorValue.Right_Leg_Armor
					characterArmorValue.Right_Leg_Armor += -1
				if(characterhp.Temp_Right_Leg_HP > 0 and rem > 0):
					rem2 = rem
					rem = rem - characterhp.Temp_Right_Leg_HP
					characterhp.Temp_Right_Leg_HP += - rem2
					if(characterhp.Temp_Right_Leg_HP < 0):
						characterhp.Temp_Right_Leg_HP = 0
				if(0 < rem):
					characterhp.Right_Leg_HP = characterhp.Right_Leg_HP - rem
					if(characterhp.Right_Leg_HP < 0):
						characterhp.Right_Leg_HP = 0
				
				saveHP(characterhp)
				saveArmor(characterArmorValue)
		return HttpResponseRedirect(getRedirectOrHome(request))
	else:
		return HttpResponseRedirect(reverse('index'))
		
def CharacterHealRightLeg(request, GIDin, CIDin):
	if CanEditCharacter(request,CIDin, GIDin):
		characterhp = get_object_or_404(Character_HP, CID = CIDin)
		if request.method == 'POST':
			form = HPFormHeal(request.POST)
			if form.is_valid():
				if form.cleaned_data['OverHeal_f']:
					characterhp.Temp_Right_Leg_HP += form.cleaned_data['Value_f'] 
				else:
					hp = form.cleaned_data['Value_f'] + characterhp.Right_Leg_HP 
					if(hp < characterhp.Max_Right_Leg_HP):
						characterhp.Right_Leg_HP = hp
					else:
						characterhp.Right_Leg_HP = characterhp.Max_Right_Leg_HP
				
				saveHP(characterhp)
		return HttpResponseRedirect(getRedirectOrHome(request))
	else:
		return HttpResponseRedirect(reverse('index'))	
		
def CharacterDamageLeftLeg(request, GIDin, CIDin):
	if CanEditCharacter(request,CIDin, GIDin):
		characterhp = get_object_or_404(Character_HP, CID = CIDin)
		characterArmorValue = Character_Equipped_Armor_Value.objects.filter(CID = CIDin).first()
		if request.method == 'POST':
			form = HPFormDamage(request.POST)
			if form.is_valid():
				rem = form.cleaned_data['Value_f']
				if not form.cleaned_data['skipArmor_f'] and characterArmorValue and characterArmorValue.Left_Leg_Armor > 0:
					rem = rem - characterArmorValue.Left_Leg_Armor
					characterArmorValue.Left_Leg_Armor += -1
				if(characterhp.Temp_Left_Leg_HP > 0 and rem > 0):
					rem2 = rem
					rem = rem - characterhp.Temp_Left_Leg_HP
					characterhp.Temp_Left_Leg_HP += - rem2
					if(characterhp.Temp_Left_Leg_HP < 0):
						characterhp.Temp_Left_Leg_HP = 0
				if(0 < rem < characterhp.Right_Leg_HP ):
					characterhp.Left_Leg_HP = characterhp.Left_Leg_HP - rem
					if(characterhp.Right_Leg_HP < 0):
						characterhp.Left_Leg_HP = 0
				
				saveHP(characterhp)
				saveArmor(characterArmorValue)
		return HttpResponseRedirect(getRedirectOrHome(request))
	else:
		return HttpResponseRedirect(reverse('index'))
		
def CharacterHealLeftLeg(request, GIDin, CIDin):
	if CanEditCharacter(request,CIDin, GIDin):
		characterhp = get_object_or_404(Character_HP, CID = CIDin)
		if request.method == 'POST':
			form = HPFormHeal(request.POST)
			if form.is_valid():
				if form.cleaned_data['OverHeal_f']:
					characterhp.Temp_Left_Leg_HP += form.cleaned_data['Value_f'] 
				else:
					hp = form.cleaned_data['Value_f'] + characterhp.Left_Leg_HP 
					if(hp < characterhp.Max_Left_Leg_HP):
						characterhp.Left_Leg_HP = hp
					else:
						characterhp.Left_Leg_HP = characterhp.Max_Left_Leg_HP
						
				saveHP(characterhp)
		return HttpResponseRedirect(getRedirectOrHome(request))
	else:
		return HttpResponseRedirect(reverse('index'))			
		

#GameCommander Control-------------------------
#----------------------------------------------		
def SurgePage(request, GIDin):
	if isGameCommander(request,GIDin):
		try:
			theGroup = get_object_or_404(Group,GID = GIDin)
			chractersInGroup = charactersInGroup = Character_Group.objects.filter(GID = GIDin)
		except Character.DoesNotExist:
			raise Http404("group does not exist")
		return render(request, 'stats/surgeControl.html', {'chractersInGroup': chractersInGroup, 'theGroup':theGroup})
	else:
		return HttpResponseRedirect(reverse('index'))
		
def SurgePageCharacterSave(request, GIDin, CIDin):
	if isGameCommander(request,GIDin):
		chracter = get_object_or_404(Character, CID = CIDin)
			
		if request.method == 'POST':
			form = SurgeForm(request.POST)
			if form.is_valid():
				if form.cleaned_data['Max_ActionSurges_f'] != None:
					chracter.Max_ActionSurges_stat = form.cleaned_data['Max_ActionSurges_f']
				if form.cleaned_data['Total_ActionSurges_f'] != None:
					chracter.Total_ActionSurges_stat  = form.cleaned_data['Total_ActionSurges_f']
				if form.cleaned_data['ActionSurges_f'] != None:
					chracter.ActionSurges_stat = form.cleaned_data['ActionSurges_f']
				if form.cleaned_data['Max_MomentofStrength_f'] != None:
					chracter.Max_MomentofStrength_stat = form.cleaned_data['Max_MomentofStrength_f']
				if form.cleaned_data['Momentofstrength_f'] != None:
					chracter.Momentofstrength_stat = form.cleaned_data['Momentofstrength_f']
				if form.cleaned_data['MomentofWeakness_passed_f'] != None:
					chracter.MomentofWeakness_passed_stat = form.cleaned_data['MomentofWeakness_passed_f']
				if form.cleaned_data['MomentofWeakness_failed_f'] != None:
					chracter.MomentofWeakness_failed_stat = form.cleaned_data['MomentofWeakness_failed_f']
				chracter.save()
		return HttpResponseRedirect(reverse('SurgePage',  kwargs={'GIDin': GIDin}))
	else:
		return HttpResponseRedirect(reverse('index'))
		
def SurgePageIncrementAction(request, GIDin, CIDin):
	if isGameCommander(request,GIDin):
		chracter = get_object_or_404(Character, CID = CIDin)
			
		if request.method == 'POST':
			form = SurgeForm(request.POST)
			if form.is_valid():
				if chracter.ActionSurges_stat < chracter.Max_ActionSurges_stat:
					chracter.ActionSurges_stat += 1
				chracter.Total_ActionSurges_stat += 1
				chracter.save()
		return HttpResponseRedirect(reverse('SurgePage',  kwargs={'GIDin': GIDin}))
	else:
		return HttpResponseRedirect(reverse('index'))

def SurgePageSpendAction(request, GIDin, CIDin):
	if isGameCommander(request,GIDin):
		chracter = get_object_or_404(Character, CID = CIDin)
			
		if request.method == 'POST':
			form = SurgeForm(request.POST)
			if form.is_valid():
				if chracter.ActionSurges_stat > 0:
					chracter.ActionSurges_stat -= 1
				chracter.save()
		return HttpResponseRedirect(reverse('SurgePage',  kwargs={'GIDin': GIDin}))
	else:
		return HttpResponseRedirect(reverse('index'))
	
def SurgePageSpendActionTwenty(request, GIDin, CIDin):
	if isGameCommander(request,GIDin):
		chracter = get_object_or_404(Character, CID = CIDin)
			
		if request.method == 'POST':
			form = SurgeForm(request.POST)
			if form.is_valid():
				if chracter.ActionSurges_stat > 2:
					chracter.ActionSurges_stat -= 3
				chracter.save()
		return HttpResponseRedirect(reverse('SurgePage',  kwargs={'GIDin': GIDin}))
	else:
		return HttpResponseRedirect(reverse('index'))
	
def SurgePageIncrementWeaknessPassed(request, GIDin, CIDin):
	if isGameCommander(request,GIDin):
		chracter = get_object_or_404(Character, CID = CIDin)
			
		if request.method == 'POST':
			form = SurgeForm(request.POST)
			if form.is_valid():
				chracter.MomentofWeakness_passed_stat += 1
				if chracter.Momentofstrength_stat < chracter.Max_MomentofStrength_stat:
					chracter.Momentofstrength_stat += 1
				chracter.save()
		return HttpResponseRedirect(reverse('SurgePage',  kwargs={'GIDin': GIDin}))
	else:
		return HttpResponseRedirect(reverse('index'))

def SurgePageIncrementWeaknessFailed(request, GIDin, CIDin):
	if isGameCommander(request,GIDin):
		chracter = get_object_or_404(Character, CID = CIDin)
			
		if request.method == 'POST':
			form = SurgeForm(request.POST)
			if form.is_valid():
				chracter.MomentofWeakness_failed_stat += 1
				chracter.save()
		return HttpResponseRedirect(reverse('SurgePage',  kwargs={'GIDin': GIDin}))
	else:
		return HttpResponseRedirect(reverse('index'))
	
def SurgePageSpendStrength(request, GIDin, CIDin):
	if isGameCommander(request,GIDin):
		chracter = get_object_or_404(Character, CID = CIDin)
			
		if request.method == 'POST':
			form = SurgeForm(request.POST)
			if form.is_valid():
				if chracter.Momentofstrength_stat > 4:
					chracter.Momentofstrength_stat -= 5
				chracter.save()
		return HttpResponseRedirect(reverse('SurgePage',  kwargs={'GIDin': GIDin}))
	else:
		return HttpResponseRedirect(reverse('index'))