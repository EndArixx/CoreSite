from django.shortcuts import get_object_or_404,render
from django.contrib.auth.decorators import permission_required
from django.http import Http404, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.staticfiles import finders

#models
from .models import  *

#forms
from .forms import CharacterForm


#utilities-------------------------------------------------------------------
def CanViewGroup(request,GIDin):
	userHasGroup = False
	publicGroups = public_Group.objects.filter(GID = GIDin).first()
	if publicGroups != None:
		userHasGroup = publicGroups.IsPublic
	if not userHasGroup and request.user.is_authenticated:
			uname = request.user.get_username()
			#Get player Name
			playA = Player.objects.get(Name = uname)
			PIDin = playA.PID
			accessstats = Group_Access.objects.filter(PID = PIDin, GID = GIDin).first()
			if accessstats != None:
				userHasGroup = accessstats.IsPlayer
	return userHasGroup
	
def CanViewCharacter(request,CIDin):
	userHasCharacter = False
	character = get_object_or_404(Character,CID = CIDin)
	userHasCharacter = CanViewGroup(request, character.GID)
	if not userHasCharacter and request.user.is_authenticated:
		uname = request.user.get_username()
		playA = Player.objects.get(Name = uname)
		PIDin = playA.PID
		accessstats = character_Access.objects.filter(PID = PIDin, CID = CIDin).first()
		if accessstats != None:
			userHasCharacter = accessstats.HasAccess
	return userHasCharacter
	
	
	
#Views-----------------------------------------------------------------------

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
			playA = Player.objects.get(Name = uname)
			PIDin = playA.PID
			accessstats = Group_Access.objects.filter(PID = PIDin, IsPlayer = True)
				
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
		except Character.DoesNotExist:
			raise Http404("group does not exist")
		NPC_dis = NPC_Disposition.objects.filter(GID = GIDin).order_by('-Disposition')
		#NPClist = NPC.object.filter(NID = NPC_dis.NID)
		return render(request, 'stats/NPCList.html', {'Group':theGroup,'NPCList':NPC_dis})
	else:
		raise Http404()
	
def NPCpage(request, GIDin,NIDin):
	if CanViewGroup(request,GIDin):
		return HttpResponse("You're looking at the characters of " + str(GIDin) + " " + str(NIDin))
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
	
	if not Access:
		raise Http404()
	
	character = get_object_or_404(Character,CID = CIDin)
		
	try:
		#getHP/Armour Data		
		characterHP = get_object_or_404(Character_HP,CID = CIDin)	
		#john this is dirty
		characterArmor = Character_Equipped_Armor_Value.objects.filter(CID = CIDin).first()
		characterStatus = Character_Status.objects.filter(CID = CIDin, Hidden = False)
		
		#team members
		groupMembers = Character.objects.filter(GID = character.GID)
	
		#stats
		characterStat = Character_Stat.objects.filter(CID = CIDin)	
		characterSkill = Character_Skill.objects.filter(CID = CIDin)	
		characterPower = Character_Power.objects.filter(CID = CIDin, Hidden = False)	

		#Items
		characterWeapon = Character_Weapon.objects.filter(CID = CIDin, Hidden = False)	
		characterGear = Character_Item.objects.filter(CID = CIDin, Equipable = True, Hidden = False)	
		characterItem = Character_Item.objects.filter(CID = CIDin, Equipable = False, Hidden = False)	
		
		characterDetails = Character_Details.objects.filter(CID = CIDin, Hidden = False)	
		
		if not character.Image:		
			character.Image = 'default.png'
		else:
			image = finders.find('stats/character/'+character.Image)
			if not image:
				character.Image = 'invalid.png'
			
		
	except Exception as e:
		print(str(e))
		raise Http404("Error loading character: " + str(character.Name))

	return render(request, 'stats/CharacterNewLim.html', {
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
	
	
#JOHN USED FOR TESTING YOU MAY REMOVE AFTER NEW SHEETS ARE COMPLETED
#player characters
def Character_Old(request, CIDin):
	uname = 'NotLoggedIn'
	Access = False
	
	#check access rights of user.
	if request.user.is_authenticated:
		uname = request.user.get_username()
		try:
			#Get player Name
			playA = Player.objects.get(Name = uname)
			PIDin = playA.PID
			accessstats = character_Access.objects.get(PID = PIDin, CID = CIDin)
			if accessstats != None:
				Access = accessstats.HasAccess
				uname  = uname + ' - ' + str(Access)
			else:
				uname = uname +  ' - [not in table]' 
		except Character.DoesNotExist:
			raise Http404("Character does not exist")
		except Exception as e:
			uname = uname + '[Access Error]' + str(e)
		
	try:
		chractersInGroup = Character.objects.get(CID = CIDin)
	except  Character.DoesNotExist:
		raise Http404("character does not exist")
		
	if Access:
		#getHP Data		
		characterHP = get_object_or_404(Character_HP,CID = CIDin)
		#JOHN: this should have a new method
		if request.method == 'POST':
			form = CharacterForm(request.POST)
			#user is updating?
			if form.is_valid():
				if form.cleaned_data['MIND_stat_f'] != None:
					chractersInGroup.MIND_stat = form.cleaned_data['MIND_stat_f']
					
				if form.cleaned_data['FIST_stat_f'] != None:
					chractersInGroup.FIST_stat = form.cleaned_data['FIST_stat_f']
					
				if form.cleaned_data['EYES_stat_f'] != None:
					chractersInGroup.EYES_stat = form.cleaned_data['EYES_stat_f']
					
				if form.cleaned_data['FACE_stat_f'] != None:
					chractersInGroup.FACE_stat = form.cleaned_data['FACE_stat_f']
					
				if form.cleaned_data['HEART_stat_f'] != None:
					chractersInGroup.HEART_stat = form.cleaned_data['HEART_stat_f']
				chractersInGroup.save()
				
		else:
			form = CharacterForm()
		#Send Access
		return render(request, 'stats/characterCon.html', {'chractersInGroup': chractersInGroup,'characterHP': characterHP, 'userNamePass': uname, 'form': form})
	else:
		#send Non Access
		return render(request, 'stats/characterLim.html', {'chractersInGroup': chractersInGroup, 'userNamePass': uname})
		
		
