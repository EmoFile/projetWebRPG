from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import response, JsonResponse, request
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.views.generic.base import View, RedirectView

from app.forms import CharacterForm
from app.models import CharacterClass, Character, Inventory, Party, Enemy, Minion, BossAlain


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


# class GenerateMinionTest(View):
#     def get_success_url(self):
#         return reverse('home')
#
#     def get(self):
#         adventurer = Character.objects.filter(pk=['adventurerId'])
#         for i in range(9):
#             minion_temp = Minion(adventurer, i)
#             minion_temp.save()


class GenerateMinionTest(RedirectView):
    permanent = False
    query_string = False
    pattern_name = 'playGame'

    def get_redirect_url(self, *args, **kwargs):
        adventurer = get_object_or_404(Character, pk=kwargs['pk'])
        for i in range(9):
            minion_temp = Minion.create(adventurer, i)
            minion_temp.save()
        return super().get_redirect_url(*args, **kwargs)


class GenerateBoss(RedirectView):
    permanent = False
    query_string = False
    pattern_name = 'playGame'

    def get_redirect_url(self, *args, **kwargs):
        adventurer = get_object_or_404(Character, pk=kwargs['pk'])
        boss_temp = BossAlain.create(100, adventurer)
        boss_temp.save()
        return super().get_redirect_url(*args, **kwargs)


class EnemyList(ListView):
    template_name = 'listEnemy.html'
    model = Minion
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['minions'] = Minion.objects.all()
        return context
