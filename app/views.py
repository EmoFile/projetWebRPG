import random

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import response, JsonResponse, request
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, DetailView

from app.forms import CharacterForm
from app.models import CharacterClass, Character, Inventory, Party, Consumable, Head, Chest, Leg, Weapon


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        result['characterClasses'] = CharacterClass.objects.all()
        # le - dans le order_by pour demander un ordre décroissant
        # result['characters'] = Character.objects.all().order_by('-level', '-hpMax', '-strength', '-intelligence',
        #                                                         '-agility',
        #                                                         '-physicalResistance', '-magicalResistance')

        result['partys'] = Party.objects.all().order_by('-stage')
        result['title'] = 'B.T.A - II'
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

    def get_success_url(self):
        party = get_object_or_404(Party, character=self.object)
        return reverse('playGame', kwargs={'pk': party.pk})

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        result['title'] = 'Create Character'
        return result

    def get(self, *args, **kwargs):
        currentCharacterClass = get_object_or_404(CharacterClass,
                                                  pk=self.kwargs['pk'])

        self.request.session['characterClassName'] = currentCharacterClass.name
        self.request.session['characterClass'] = self.kwargs['pk']
        self.request.session['HpMax'] = currentCharacterClass.generateHpMax()
        self.request.session['Strength'] = currentCharacterClass.generateStrength()
        self.request.session['Agility'] = currentCharacterClass.generateAgility()
        self.request.session['Intelligence'] = currentCharacterClass.generateIntelligence()
        self.request.session['PhysicalResistance'] = currentCharacterClass.generatePR()
        self.request.session['MagicalResistance'] = currentCharacterClass.generateMR()
        return super().get(self)

    def form_valid(self, form):
        # Création de l'objet sans enregistrement en base
        self.object = form.save(commit=False)

        # Création d'un inventaire vide unique au personnage avec affectation et récupéraction de la classe du personnage
        currentCharacterClass = get_object_or_404(CharacterClass,
                                                  pk=self.request.session['characterClass'])
        inventory = Inventory()
        inventory.save()

        # Constitution du personnage
        self.object.inventory = inventory
        self.object.characterClass = currentCharacterClass
        self.object.hpMax = self.request.session['HpMax']
        self.object.hp = self.request.session['HpMax']
        self.object.strength = self.request.session['Strength']
        self.object.agility = self.request.session['Agility']
        self.object.intelligence = self.request.session['Intelligence']
        self.object.physicalResistance = self.request.session['PhysicalResistance']
        self.object.magicalResistance = self.request.session['MagicalResistance']

        # Création en BDD du personnage
        self.object.save()
        party = Party(user=self.request.user, character=self.object)
        party.save()
        return super().form_valid(form)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('logIn')
    template_name = 'signUp.html'


class LogInView(LoginView):
    form_class = AuthenticationForm
    template_name = 'logIn.html'

    def get_success_url(self):
        return reverse('home')


class PlayGameView(TemplateView):
    template_name = 'playGame.html'

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        result['title'] = 'Play Game'
        party = get_object_or_404(Party, pk=self.kwargs['pk'])
        result['party'] = party
        return result


def dropItem(request):
    if random.randint(1, 2) == 1:
        stuffRarity = random.randint(1, 10)
        if 1 <= stuffRarity <= 4:
            stuffRarity = 'Common'
        elif 5 <= stuffRarity <= 7:
            stuffRarity = 'Rare'
        elif 8 <= stuffRarity <= 9:
            stuffRarity = 'Epic'
        else:
            stuffRarity = 'Legendary'

        stuffClass = random.randint(1, 5)
        if stuffClass == 1:
            stuffClassName = 'Consumable'
            stuffPull = Consumable.objects.filter(rarity=stuffRarity)
            stuffCount = stuffPull.count()
            ItemDropped = stuffPull[random.randint(0, stuffCount-1)]
            # ItemDropped = get_object_or_404(Consumable, pk=random.randint(1, Consumable.objects.count()))
        elif stuffClass == 2:
            stuffClassName = 'Head'
            stuffPull = Head.objects.filter(rarity=stuffRarity)
            stuffCount = stuffPull.count()
            ItemDropped = stuffPull[random.randint(0, stuffCount-1)]
            # ItemDropped = get_object_or_404(Head, pk=random.randint(1, Head.objects.count()))
        elif stuffClass == 3:
            stuffClassName = 'Chest'
            stuffPull = Chest.objects.filter(rarity=stuffRarity)
            stuffCount = stuffPull.count()
            ItemDropped = stuffPull[random.randint(0, stuffCount-1)]
            #ItemDropped = get_object_or_404(Chest, pk=random.randint(1, Chest.objects.count()))
        elif stuffClass == 4:
            stuffClassName = 'Leg'
            stuffPull = Leg.objects.filter(rarity=stuffRarity)
            stuffCount = stuffPull.count()
            ItemDropped = stuffPull[random.randint(0, stuffCount-1)]
            # ItemDropped = get_object_or_404(Leg, pk=random.randint(1, Leg.objects.count()))
        else:
            stuffClassName = 'Weapon'
            stuffPull = Weapon.objects.filter(rarity=stuffRarity)
            stuffCount = stuffPull.count()
            ItemDropped = stuffPull[random.randint(0, stuffCount-1)]
            # ItemDropped = get_object_or_404(Weapon, pk=random.randint(1, Weapon.objects.count()))

        if stuffClassName == 'Consumable':
            data = {
                'isItemDropped': True,
                'stuffClassName': stuffClassName,
                'stuffRarity': stuffRarity,
                'stuffCount': stuffCount,
                'ItemDropped': {
                    'name': ItemDropped.name,
                    'rarity': ItemDropped.rarity,
                    'hp': ItemDropped.hp,
                    'strength': ItemDropped.strength,
                    'intelligence': ItemDropped.intelligence,
                    'agility': ItemDropped.agility
                }
            }
        else:
            data = {
                'isItemDropped': True,
                'stuffClassName': stuffClassName,
                'stuffRarity': stuffRarity,
                'stuffCount': stuffCount,
                'ItemDropped': {
                    'name': ItemDropped.name,
                    'requiredLevel': ItemDropped.requiredLevel,
                    'requiredClass': ItemDropped.characterClass.name,
                    'rarity': ItemDropped.rarity,
                    'hpMax': ItemDropped.hpMax,
                    'physicalResistance': ItemDropped.physicalResistance,
                    'magicalResistance': ItemDropped.magicalResistance,
                    'strength': ItemDropped.strength,
                    'intelligence': ItemDropped.intelligence,
                    'agility': ItemDropped.agility
                }
            }
    else:
        data = {'isItemDropped': False}
    return JsonResponse(data)
