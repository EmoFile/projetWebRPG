from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from app.models import Character


class CharacterForm(forms.ModelForm):
	class Meta:
		model = Character
		# exclude = []
		fields = ['name', 'characterClass']
	
	name = forms.CharField(max_length=20, widget=widgets.TextInput(
		attrs={'placeholder': 'Enter Your Name'}
	))
