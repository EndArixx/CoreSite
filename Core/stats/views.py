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
from .forms import SurgeForm


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
	
def CanViewCharacter(request,CIDin):
	userHasCharacter = False
	character = get_object_or_404(Character,CID = CIDin)
	userHasCharacter = CanViewGroup(request, character.GID)
	if not userHasCharacter and request.user.is_authenticated:
		accessstats = character_Access.objects.filter(PID = getPid(request), CID = CIDin).first()
		if accessstats != None:
			userHasCharacter = accessstats.HasAccess
	return userHasCharacter
	
def CanEditCharacter(request,CIDin):
	userCanEditCharacter = False
	character = get_object_or_404(Character,CID = CIDin)
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
def PlayerHandbook(request):
	return render(request, 'stats/playerHB.html')

#Index----------------------------------------
#---------------------------------------------
def index(request):
	publicGroups = public_Group.objects.filter(IsPublic = True)
	if request.user.is_authenticated:
		uname = request.user.get_username()
		try:
			#Get player Name
			playA = Player.objects.get(User = request.user)
			PIDin = playA.PID
			accessstats = Group_Access.objects.filter(Q(PID = PIDin) & (Q(IsPlayer = True) | Q(IsGC = True)))
				
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
		try:
			chractersInGroup = Character.objects.filter(GID = GIDin)
			#theGroup = Group.objects.filter(GID = GIDin)
			theGroup = get_object_or_404(Group,GID = GIDin)
		except Character.DoesNotExist:
			raise Http404("group does not exist")
		return render(request, 'stats/group.html', {'chractersInGroup': chractersInGroup, 'Group':theGroup})
	else:
		raise Http404()

#NPC stuff------------------------------------
#---------------------------------------------
def NPClist(request, GIDin):
	if CanViewGroup(request,GIDin):
		try:
			theGroup = get_object_or_404(Group,GID = GIDin)
		except theGroup.DoesNotExist:
			raise Http404("group does not exist")
		NPC_dis = NPC_Disposition.objects.filter(GID = GIDin).order_by('NID__FID__Name','NID__Name')
		NPC_fac = Faction.objects.filter(FID__in = set(NPC_dis.values_list('NID__FID', flat=True))).order_by('Name')
		return render(request, 'stats/NPCList.html', {'Group':theGroup,'NPCList':NPC_dis, 'NPCFaction':NPC_fac})
	else:
		raise Http404()
	
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
		raise Http404()

#GameCommander Control-------------------------
#----------------------------------------------		
def SurgePage(request, GIDin):
	if isGameCommander(request,GIDin):
		try:
			theGroup = get_object_or_404(Group,GID = GIDin)
			chractersInGroup = Character.objects.filter(GID = GIDin)
		except Character.DoesNotExist:
			raise Http404("group does not exist")
		return render(request, 'stats/surgeControl.html', {'chractersInGroup': chractersInGroup, 'Group':theGroup})
	else:
		raise Http404()
		
def SurgePageCharacterSave(request, GIDin, CIDin):
	if isGameCommander(request,GIDin):
		try:
			theGroup = get_object_or_404(Group,GID = GIDin)
			chracter = get_object_or_404(Character, CID = CIDin)
		except Character.DoesNotExist:
			raise Http404("group does not exist")
			
		if request.method == 'POST':
			form = SurgeForm(request.POST)
			if form.is_valid():
				if form.cleaned_data['ActionSurges_f'] != None:
					chracter.ActionSurges_stat = form.cleaned_data['ActionSurges_f']
				chracter.save()
		return HttpResponseRedirect(reverse('SurgePage',  kwargs={'GIDin': GIDin}))
	else:
		raise Http404()
		

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
		raise Http404()
	
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
		raise Http404()	
		
		
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
		raise Http404()	

	
		
#Player---------------------------------------
#---------------------------------------------
def player(request, PID):
	#John Validate player.
	return HttpResponse("You're looking at the characters of %s." % PID)
	
#Character------------------------------------
#---------------------------------------------
def Character_Sheet(request, CIDin):
	Access = CanViewCharacter(request, CIDin)
	htmlpage = 'stats/{0}.html'
	if not Access:
		raise Http404()
	
	character = get_object_or_404(Character,CID = CIDin)
	try:
		#Some Things may be hidden from everyone but the player owner and the DB.
		if isGameCommander(request, character.GID) or CanEditCharacter(request, CIDin):
			characterStatus = Character_Status.objects.filter(CID = CIDin)
			characterPower = Character_Power.objects.filter(CID = CIDin)	
			characterWeapon = Character_Weapon.objects.filter(CID = CIDin)	
			characterGear = Character_Item.objects.filter(CID = CIDin, Equipable = True)	
			characterItem = Character_Item.objects.filter(CID = CIDin, Equipable = False)	
			characterDetails = Character_Details.objects.filter(CID = CIDin)	
			htmlpage  = htmlpage.format('CharacterNewCon')
		else:
			characterStatus = Character_Status.objects.filter(CID = CIDin, Hidden = False)
			characterPower = Character_Power.objects.filter(CID = CIDin, Hidden = False)	
			characterWeapon = Character_Weapon.objects.filter(CID = CIDin, Hidden = False)	
			characterGear = Character_Item.objects.filter(CID = CIDin, Equipable = True, Hidden = False)	
			characterItem = Character_Item.objects.filter(CID = CIDin, Equipable = False, Hidden = False)	
			characterDetails = Character_Details.objects.filter(CID = CIDin, Hidden = False)
			htmlpage = htmlpage.format('CharacterNewLim')
			
		#These tables do not have a hidden column. 
		characterHP = get_object_or_404(Character_HP,CID = CIDin)	
			#john this is dirty
		characterArmor = Character_Equipped_Armor_Value.objects.filter(CID = CIDin).first()
		groupMembers = Character.objects.filter(GID = character.GID)
		characterStat = Character_Stat.objects.filter(CID = CIDin)	
		characterSkill = Character_Skill.objects.filter(CID = CIDin)	
		
		if not character.Image:		
			character.Image = 'default.png'
		else:
			image = finders.find('stats/character/'+character.Image)
			if not image:
				character.Image = 'invalid.png'
				
			
	except Exception as e:
		print(str(e))
		raise Http404("Error loading character: " + str(character.Name))

	return render(request, htmlpage, {
	'character': character,
	'characterHP': characterHP,
	'characterArmor': characterArmor,
	'groupMembers': groupMembers,
	'characterStat': characterStat,
	'characterSkill': characterSkill,
	'characterPower': characterPower,
	'characterWeapon': characterWeapon,
	'characterGear': characterGear,
	'characterItem': characterItem,
	'characterDetails': characterDetails,
	'characterStatus': characterStatus})	
