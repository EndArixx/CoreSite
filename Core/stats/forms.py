from django import forms

class SurgeForm(forms.Form):
	Max_ActionSurges_f = forms.IntegerField(label='Max Action',required=False)
	Total_ActionSurges_f = forms.IntegerField(label='Total Action',required=False)
	ActionSurges_f = forms.IntegerField(label='Current Action',required=False)
	Max_MomentofStrength_f = forms.IntegerField(label='Max Strength',required=False)
	Momentofstrength_f = forms.IntegerField(label='Current Strength',required=False)
	MomentofWeakness_failed_f = forms.IntegerField(label='Total Failed',required=False)
	MomentofWeakness_passed_f = forms.IntegerField(label='Total Passed',required=False) 