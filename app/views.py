from django.http import response, JsonResponse, request
from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.views.generic import TemplateView

from app.models import CharacterClass, Character


class IndexView(TemplateView):
	template_name = 'index.html'
	
	def get_context_data(self, **kwargs):
		result = super().get_context_data(**kwargs)
		result['characterClasses'] = CharacterClass.objects.all()
		return result


class GenerateCharacterView(generic.View):
	def post(self):
		
		var = Character.generateRandomCharacter(request['characterClass'])
		return JsonResponse(var)
