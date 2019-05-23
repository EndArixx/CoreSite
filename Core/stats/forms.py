from django import forms

class SurgeForm(forms.Form):
	Max_ActionSurges_f = forms.IntegerField(label='Max Action',required=False)
	Total_ActionSurges_f = forms.IntegerField(label='Total Action',required=False)
	ActionSurges_f = forms.IntegerField(label='Current Action',required=False)
	Max_MomentofStrength_f = forms.IntegerField(label='Max Strength',required=False)
	Momentofstrength_f = forms.IntegerField(label='Current Strength',required=False)
	MomentofWeakness_failed_f = forms.IntegerField(label='Total Failed',required=False)
	MomentofWeakness_passed_f = forms.IntegerField(label='Total Passed',required=False) 

AddorO=[('Add_f','Add'),
	('Override_f','Override')]
	
class HPAllForm(forms.Form):
	OverHeal_f = forms.BooleanField(label='Temporary HP?',required=False) 
	AddorO_f = forms.ChoiceField(label='',choices=AddorO, widget=forms.RadioSelect, initial= "Add_f")
	HeadHP_f = forms.IntegerField(label='Head', initial=0,required=False) 
	ArmLeftHP_f = forms.IntegerField(label='Left Arm', initial=0,required=False) 
	CoreHP_f = forms.IntegerField(label='Core', initial=0,required=False) 
	ArmRightHP_f = forms.IntegerField(label='Right Arm', initial=0,required=False) 
	LegLeftHP_f = forms.IntegerField(label='Left Leg', initial=0,required=False) 
	LegRightHP_f = forms.IntegerField(label='Right Leg', initial=0,required=False) 

class ArmorAllForm(forms.Form):
	AddorO_f = forms.ChoiceField(label='',choices=AddorO, widget=forms.RadioSelect, initial= "Add_f")
	HeadArmor_f = forms.IntegerField(label='Head', initial=0,required=False) 
	ArmLeftArmor_f = forms.IntegerField(label='Left Arm', initial=0,required=False) 
	CoreArmor_f = forms.IntegerField(label='Core', initial=0,required=False) 
	ArmRightArmor_f = forms.IntegerField(label='Right Arm', initial=0,required=False) 
	LegLeftArmor_f = forms.IntegerField(label='Left Leg', initial=0,required=False) 	
	LegRightArmor_f = forms.IntegerField(label='Right Leg', initial=0,required=False) 
	
class HPFormDamage(forms.Form):
	skipArmor_f = forms.BooleanField(label='Ignore Armor?',required=False) 
	Value_f = forms.IntegerField(label='Amount',min_value=0, initial=0,required=True) 
	
class HPFormHeal(forms.Form):
	OverHeal_f = forms.BooleanField(label='Temporary HP?',required=False) 
	Value_f = forms.IntegerField(label='Amount',min_value=0, initial=0,required=True) 
	