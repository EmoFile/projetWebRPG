import self
from django.core.checks import messages
from django.db import IntegrityError
from django.http import response, JsonResponse, request
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import TemplateView, CreateView, DetailView

from app.forms import CharacterForm
from app.models import CharacterClass, Character, Inventory


class IndexView(TemplateView):
	template_name = 'index.html'
	
	def get_context_data(self, **kwargs):
		result = super().get_context_data(**kwargs)
		result['characterClasses'] = CharacterClass.objects.all()
		result['title'] = 'Home'
		return result


class CharacterDetailView(DetailView):
	model = Character
	template_name = 'characterDetail.html'
	
	def get_context_data(self, **kwargs):
		result = super().get_context_data(**kwargs)
		result['title'] = 'Character Detail'
		return result


class GenerateCharacterView(CreateView):
	model = Character
	form_class = CharacterForm
	template_name = 'characterForm.html'
	
	def get_context_data(self, **kwargs):
		result = super().get_context_data(**kwargs)
		result['title'] = 'Create Character'
		return result
	
	def form_valid(self, form):
		# Création de l'objet sans enregistrement en base
		self.object = form.save(commit=False)
		
		# Création d'un inventaire vide unique au personnage avec affectation
		inventory = Inventory()
		inventory.save()
		self.object.inventory = inventory
		
		# Récupération en BDD de la characterClass de l'objet en création
		# => A passer en paramètre à l'arrivé sur la page pour la
		# génération des valeurs random et l'affichage des valeurs générées
		# aléatoirement en front avant le traitement du l'enregistrement du
		# personnage
		test = form['characterClass'].value()
		currentCharacterClass = get_object_or_404(CharacterClass,
		                                          pk=test)
		
		# En fonction des la characterClass trouvée génération aléatoire des
		# caractéristiques et affectation des valeurs dans l'objet
		generatedHpMax = currentCharacterClass.generateHpMax()
		self.object.hpMax = generatedHpMax
		self.object.hp = generatedHpMax
		
		generatedStrength = currentCharacterClass.generateStrength()
		self.object.strength = generatedStrength
		
		generatedAgility = currentCharacterClass.generateAgility()
		self.object.agility = generatedAgility
		
		generatedIntelligence = currentCharacterClass.generateIntelligence()
		self.object.intelligence = generatedIntelligence
		
		generatedPhysicalResistance = currentCharacterClass.generatePR()
		self.object.physicalResistance = generatedPhysicalResistance
		
		generatedMagicalResistance = currentCharacterClass.generateMR()
		self.object.magicalResistance = generatedMagicalResistance
		
		# Enregistrement en BDD de l'objet et appel du super form valid pour
		# renvoie de la succes url défini en Model
		self.object.save()
		return super().form_valid(form)

# def get_context_data(self, **kwargs):
# 	context = super().get_context_data(**kwargs)
# 	# classCharacter = get_object_or_404(CharacterClass,
# 	#                                    self.kwargs['characterClass'])
# 	# context['randomCarac'] = classCharacter.getRadomCarac()
# 	context['randomCarac'] = 'test'
# 	return context
