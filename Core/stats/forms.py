from django import forms

class CharacterForm(forms.Form):
	MIND_stat_f = forms.IntegerField(label='Mind Stat',required=False)
	FIST_stat_f = forms.IntegerField(label='Fist Stat',required=False)
	EYES_stat_f = forms.IntegerField(label='Eyes Stat',required=False)
	FACE_stat_f = forms.IntegerField(label='Face Stat',required=False)
	HEART_stat_f = forms.IntegerField(label='Heart Stat',required=False)