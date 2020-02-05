import random

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import response, JsonResponse, request
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.views.generic.base import RedirectView

from app.forms import CharacterForm
from app.models import CharacterClass, Character, Inventory, Party, Minion, BossAlain, Consumable, Head, Chest, Leg, \
    Weapon, InventoryConsumable, Enemy, PartyEnemy


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        result['characterClasses'] = CharacterClass.objects.all()
        # le - dans le order_by pour demander un ordre décroissant
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


class GenerateCharacterView(LoginRequiredMixin, CreateView):
    login_url = 'logIn'
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
        self.request.session[
            'Strength'] = currentCharacterClass.generateStrength()
        self.request.session[
            'Agility'] = currentCharacterClass.generateAgility()
        self.request.session[
            'Intelligence'] = currentCharacterClass.generateIntelligence()
        self.request.session[
            'PhysicalResistance'] = currentCharacterClass.generatePR()
        self.request.session[
            'MagicalResistance'] = currentCharacterClass.generateMR()
        return super().get(self)

    def form_valid(self, form):
        # Création de l'objet sans enregistrement en base
        self.object = form.save(commit=False)
        # Création d'un inventaire vide unique au personnage avec affectation et récupéraction de la classe du personnage
        currentCharacterClass = get_object_or_404(CharacterClass,
                                                  pk=self.request.session[
                                                      'characterClass'])
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
        self.object.physicalResistance = self.request.session[
            'PhysicalResistance']
        self.object.magicalResistance = self.request.session[
            'MagicalResistance']
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


class LogoutView(LogoutView):
    next_page = 'home'


class PlayGameView(LoginRequiredMixin, TemplateView):
    login_url = 'logIn'
    template_name = 'playGame.html'

    def get(self, request, *args, **kwargs):
        party = get_object_or_404(Party, pk=self.kwargs['pk'])
        print(request.user.pk)
        if request.user.pk != party.user.pk:
            return redirect(reverse('home'))
        elif party.isEnded:
            return redirect(reverse('home'))
        return super().get(self)

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        result['title'] = 'Play Game'
        party = get_object_or_404(Party, pk=self.kwargs['pk'])
        result['party'] = party
        result['currentCharacter'] = party.character.reload()
        print(party.enemies.all().last())
        print(party.enemies.all().count())
        if party.enemies.all().count() > 0:
            enemy = party.enemies.all().last()
            p_e = get_object_or_404(PartyEnemy, party=party, enemy=enemy)
            result['enemy'] = {
                'partyStage': party.stage,
                'enemyPk': enemy.pk,
                'enemyName': enemy.name,
                'enemyHp': p_e.hp,
                'enemyHpMax': enemy.hpMax,
                'enemyStrength': enemy.strength,
                'enemyAgility': enemy.agility,
                'enemyIntelligence': enemy.intelligence,
                'enemyPhysicalResistance': enemy.physical_resistance,
                'enemyMagicalResistance': enemy.magical_resistance,
                'partyIsEnded': party.isEnded
            }
        else:
            result['enemy'] = NextEnemy(pkParty=party.pk)
        return result


class PlayRound(generic.View):
    http_method_names = ['get']

    def get(self, request, **kwargs):
        """

        :param kwargs:
        :mandatory pkParty, pkEnemy:
        :optional:
        :return:
        """
        party = get_object_or_404(Party, pk=kwargs['pkParty'])
        adventurer = party.character
        enemy = get_object_or_404(Enemy, pk=kwargs['pkEnemy'])
        p_e = PartyEnemy.objects.get(party=party,
                                     enemy=enemy)
        if p_e.hp <= 0:
            return JsonResponse({
                'nothing': 'You know nothing John Snow'
            })
        if random.randint(0, 1):
            atkEnemy = enemy.strength
            resAdventurer = adventurer.getPhysicalResistance()
            defEnemy = enemy.physical_resistance
        else:
            atkEnemy = enemy.intelligence
            resAdventurer = adventurer.getMagicalResistance()
            defEnemy = enemy.magical_resistance

        if adventurer.characterClass.name == 'Warrior':
            atkAdventurer = adventurer.getStrength()
            defAdventurer = adventurer.getPhysicalResistance()
            resEnemy = enemy.physical_resistance
        else:
            atkAdventurer = adventurer.getIntelligence()
            resEnemy = enemy.magical_resistance
            defAdventurer = adventurer.getMagicalResistance()

        if adventurer.agility > enemy.agility:
            hpTab = fight(atkAdventurer, defAdventurer, adventurer.name, resEnemy, enemy.name)
            adventurer.setHp(-hpTab[0])
            p_e.hp -= hpTab[1]
            battleReport = {'0': hpTab[2]}
            adventurer.save()
            p_e.save()
            if p_e.hp > 0 and adventurer.hp > 0:
                battleReport['0']['6'] = " l'ennemie si tien toujour devant pret a en d'acoudre !"
                hpTab = fight(atkEnemy, defEnemy, enemy.name, resAdventurer, adventurer.name)
                p_e.hp -= hpTab[0]
                adventurer.setHp(-hpTab[1])
                battleReport['1'] = hpTab[2]
                p_e.save()
                adventurer.save()
        else:
            hpTab = fight(atkEnemy, defEnemy, enemy.name, resAdventurer, adventurer.name)
            p_e.hp -= hpTab[0]
            adventurer.setHp(-hpTab[1])
            battleReport = {'0': hpTab[2]}
            p_e.save()
            adventurer.save()
            if p_e.hp > 0 and adventurer.hp > 0:
                battleReport['0']['6'] = " notre Héros est toujour debout mais pour encore combien de temps ?!"
                hpTab = fight(atkAdventurer, defAdventurer, adventurer.name, resEnemy, enemy.name)
                adventurer.setHp(-hpTab[0])
                p_e.hp -= hpTab[1]
                battleReport['1'] = hpTab[2]
                adventurer.save()
                p_e.save()
        if adventurer.hp <= 0:
            battleReport['end'] = 'Cet énemie était bien superieur a ce héors malheurement, SOUILLEEEEEED'
            party.isEnded = True
            party.save()
            return JsonResponse({'isEnded': party.isEnded,
                                 'enemy': {
                                     'hp': p_e.hp
                                 },
                                 'character': ReloadCharacter(currentCharacter=adventurer),
                                 'battleReport': battleReport
                                 })
        elif p_e.hp <= 0:
            battleReport['end'] = "L'énemie s'est fait écraser sur ce dernier coup incompris de la population !"
            GettingXp(character=adventurer)
            return JsonResponse({'dropItem': DropItem(adventurer=adventurer),
                                 'isEnded': party.isEnded,

                                 'enemy': {
                                     'hp': p_e.hp
                                 },
                                 'character': ReloadCharacter(currentCharacter=adventurer),
                                 'battleReport': battleReport
                                 })
        else:
            return JsonResponse({
                'isEnded': party.isEnded,
                'enemy': {
                    'hp': p_e.hp
                },
                'character': ReloadCharacter(currentCharacter=adventurer),
                'battleReport': battleReport
            })


def fight(atk, atkDef, atkName, res, defName):
    aD20 = random.randint(0, 20)
    dD20 = random.randint(0, 20)
    assault = atk + aD20
    protection = res + dD20
    hpAtk = 0
    hpDef = 0

    battleReport = {'0': 'Voila que ' + atkName + ' attaque',
                    '1': "Que les dés vous dessine un destin favorable !",
                    '2':  atkName + " lance un D20 d'attaque et fait " + str(aD20),
                    '3': 'et ' + defName + ' lance un D20 de défense et fait ' + str(dD20)}
    if aD20 == 1:
        damage = assault - atkDef
        battleReport['4'] = atkName + ' WTF il se rate lamentablement et fait un echec critque !!!!!'
        if damage >= 0:
            hpAtk = damage
            battleReport['5'] = 'LE HABAKIRIIIIIII de ' + str(hpAtk) + ' damageeeees'
        else:
            battleReport['5'] =  "Heuresement que son armure est plus épaisse que ses muscle et ne s'inflige aucun damages !"
    else:
        damage = assault - protection
        if aD20 == 20:
            battleReport['4'] = 'et... au mon dieu ?! ' + atkName + ' !!! il transperce ' + defName + ' en faisant une réussite critque'
            damage *= 2
        if damage > 0:
            hpDef = damage
            battleReport['5'] = 'le coup part !!!! et lui fait ' + str(hpDef) + ' de damageeeeessss !!!!'
        else:
            battleReport['5'] = 'malheuresement il va falloir y mettre un du sien pour le fumé !!'
    return hpAtk, hpDef, battleReport


def DropItem(**kwargs):
    if random.randint(1, 2) == 1:
        stuffRarity = random.randint(1, 100)
        if 1 <= stuffRarity <= 50:
            stuffRarity = 'Common'
        elif 51 <= stuffRarity <= 89:
            stuffRarity = 'Rare'
        elif 90 <= stuffRarity <= 99:
            stuffRarity = 'Epic'
        else:
            stuffRarity = 'Legendary'
        stuffClass = random.randint(1, 5)
        if stuffClass == 1:
            stuffClassName = 'Consumable'
            stuffPull = Consumable.objects.filter(rarity=stuffRarity)
            stuffCount = stuffPull.count()
            ItemDropped = stuffPull[random.randint(0, stuffCount - 1)]
        elif stuffClass == 2:
            stuffClassName = 'Head'
            stuffPull = Head.objects.filter(rarity=stuffRarity, characterClass=kwargs['adventurer'].characterClass)
            stuffCount = stuffPull.count()
            ItemDropped = stuffPull[random.randint(0, stuffCount - 1)]
        elif stuffClass == 3:
            stuffClassName = 'Chest'
            stuffPull = Chest.objects.filter(rarity=stuffRarity, characterClass=kwargs['adventurer'].characterClass)
            stuffCount = stuffPull.count()
            ItemDropped = stuffPull[random.randint(0, stuffCount - 1)]
        elif stuffClass == 4:
            stuffClassName = 'Leg'
            stuffPull = Leg.objects.filter(rarity=stuffRarity, characterClass=kwargs['adventurer'].characterClass)
            stuffCount = stuffPull.count()
            ItemDropped = stuffPull[random.randint(0, stuffCount - 1)]
        else:
            stuffClassName = 'Weapon'
            stuffPull = Weapon.objects.filter(rarity=stuffRarity, characterClass=kwargs['adventurer'].characterClass)
            stuffCount = stuffPull.count()
            ItemDropped = stuffPull[random.randint(0, stuffCount - 1)]
        if stuffClassName == 'Consumable':
            data = {
                'isItemDropped': True,
                'stuffClassName': stuffClassName,
                'stuffRarity': stuffRarity,
                'stuffCount': stuffCount,
                'pk': ItemDropped.pk,
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
                'pk': ItemDropped.pk,
                'ItemDropped': {
                    'name': ItemDropped.name,
                    'requiredLevel': ItemDropped.requiredLevel,
                    'requiredClass': ItemDropped.characterClass.name,
                    'rarity': ItemDropped.rarity,
                    'hpMax': ItemDropped.hpMax,
                    'physicalResistence': ItemDropped.physicalResistance,
                    'magicalResistence': ItemDropped.magicalResistance,
                    'strength': ItemDropped.strength,
                    'intelligence': ItemDropped.intelligence,
                    'agility': ItemDropped.agility
                }
            }
    else:
        data = {'isItemDropped': False}
    return data


def ChangeStuff(*args, **kwargs):
    oldStuff = ''
    newStuff = ''
    for prop, cls in {'head': Head,
                      'chest': Chest,
                      'leg': Leg,
                      'weapon': Weapon}.items():
        if kwargs['stuffClassName'] == prop.capitalize():
            try:
                obj = getattr(kwargs['inventory'], prop)
                if obj:
                    oldStuff = obj.name
                    kwargs['inventory'].character.setHpMax(-obj.hpMax)
                else:
                    oldStuff = 'None'
                setattr(kwargs['inventory'],
                        prop,
                        get_object_or_404(cls, pk=kwargs['stuffPk']))
                kwargs['inventory'].save()
                newStuff = getattr(kwargs['inventory'], prop)
                kwargs['inventory'].character.setHpMax(newStuff.hpMax)
                kwargs['inventory'].character.save()
            except:
                pass
    return JsonResponse({
        'stuffClassName': kwargs['stuffClassName'],
        'oldStuff': oldStuff,
        'newStuff': newStuff.name,
        'newStuffRarity': newStuff.rarity,
        'newStuffHpMax': newStuff.hpMax,
        'newStuffStrength': newStuff.strength,
        'newStuffIntelligence': newStuff.intelligence,
        'newStuffAgility': newStuff.agility,
        'newStuffPhysicalResistance': newStuff.physicalResistance,
        'newStuffMagicalResistance': newStuff.magicalResistance,
        'character': ReloadCharacter(currentCharacter=kwargs['inventory'].character)
    })


def AddConsumable(*args, **kwargs):
    kwargs['inventory'].consumables.add(kwargs['consumable'])

    i_c = InventoryConsumable.objects.get(inventory=kwargs['inventory'],
                                          consumable=kwargs['consumable'])
    i_c.quantity += 1
    i_c.save()
    return JsonResponse({
        'stuffClassName': kwargs['stuffClassName'],
        'stuffPk': kwargs['consumable'].pk,
        'newStuff': kwargs['consumable'].name,
        'newStuffHpMax': kwargs['consumable'].hp,
        'newStuffStrength': kwargs['consumable'].strength,
        'newStuffIntelligence': kwargs['consumable'].intelligence,
        'newStuffAgility': kwargs['consumable'].agility,
        'newStuffQuantity': i_c.quantity
    })


def ChangeItem(*args, **kwargs):
    currentParty = get_object_or_404(Party, pk=kwargs['partyPk'])
    currentCharacter = currentParty.character
    characterInventory = currentCharacter.inventory
    if kwargs['stuffClassName'] == 'Consumable':
        return AddConsumable(inventory=characterInventory,
                             consumable=get_object_or_404(Consumable,
                                                          pk=kwargs['stuffPk']),
                             stuffClassName=kwargs['stuffClassName'])
    else:
        return ChangeStuff(inventory=characterInventory,
                           stuffClassName=kwargs['stuffClassName'],
                           stuffPk=kwargs['stuffPk'])


def NextEnemy(**kwargs):
    """

    :param kwargs:
    :mandatory pkParty:
    :optional pkEnemy:
    :return Json of the next Enemy:
    """
    party = get_object_or_404(Party, pk=kwargs['pkParty'])
    adventurer = party.character
    if kwargs.get('pkEnemy') is None:
        if Enemy.objects.count() == 0:
            GenerateEnemy(adventurer=adventurer, stage=party.stage)
        next_enemy = Enemy.objects.first()
    else:
        l_enemy = get_object_or_404(Enemy, pk=kwargs['pkEnemy'])
        if l_enemy.next is None:
            GenerateEnemy(adventurer=adventurer, stage=party.stage, last=l_enemy)
        next_enemy = l_enemy.next
    PartyEnemy.objects.create(party=party,
                              enemy=next_enemy,
                              hp=next_enemy.hp)
    party.stage += 1
    party.save()
    return {
        'partyStage': party.stage,
        'enemyPk': next_enemy.pk,
        'enemyName': next_enemy.name,
        'enemyHpMax': next_enemy.hpMax,
        'enemyHp': next_enemy.hpMax,
        'enemyStrength': next_enemy.strength,
        'enemyAgility': next_enemy.agility,
        'enemyIntelligence': next_enemy.intelligence,
        'enemyPhysicalResistance': next_enemy.physical_resistance,
        'enemyMagicalResistance': next_enemy.magical_resistance
    }


class NextEnemyView(generic.View):
    http_method_names = ['get']

    def get(self, request, **kwargs):
        if kwargs.get('pkEnemy'):
            p_e = get_object_or_404(PartyEnemy, party=kwargs['pkParty'], enemy=kwargs['pkEnemy'])
            if p_e.hp > 0:
                return JsonResponse({'nothingDude': 'You know Nothing John Snow'})
        return JsonResponse(NextEnemy(**kwargs), safe=False)


def GenerateEnemy(**kwargs):
    """

    :param kwargs:
    :mandatory adventurer, stage:
    :optional last:
    :return:
    """
    adventurer = kwargs['adventurer']
    minions = []
    for i in range(9):
        minion = Minion.create(adventurer, i)
        minion.save()
        minions.append(minion)
    if kwargs.get('last'):
        last = kwargs['last']
        last.next = minions[0]
        last.save()
    minion_prev = None
    for minion in minions[::-1]:
        if minion_prev is None:
            minion_prev = minion
        else:
            minion.next = minion_prev
            minion.save()
            minion_prev = minion
        # PartyEnemy.objects.create(party=party, enemy=minion)
    stage = kwargs['stage'] + 10
    new_boss = BossAlain.create(stage, adventurer)
    print(stage)
    print(new_boss)
    new_boss.save()
    minions[8].next = new_boss
    minions[8].save()


def UseItem(*args, **kwargs):
    currentParty = get_object_or_404(Party, pk=kwargs['partyPk'])
    currentConsumable = get_object_or_404(Consumable, pk=kwargs['consumablePk'])

    i_c = InventoryConsumable.objects.get(inventory=currentParty.character.inventory,
                                          consumable=currentConsumable)
    consumableName = i_c.consumable.name
    consumableOldQuantity = i_c.quantity
    i_c.quantity -= 1
    i_c.save()
    if i_c.quantity == 0:
        i_c.delete()
    consumableNewQuantity = i_c.quantity

    currentParty.character.modifyCarac(currentConsumable)
    currentParty.character.save()
    return JsonResponse({'consumableName': consumableName,
                         'consumableOldQuantity': consumableOldQuantity,
                         'consumableNewQuantity': consumableNewQuantity,
                         'character': ReloadCharacter(
                             currentCharacter=currentParty.character)
                         })


class EnemyList(ListView):
    template_name = 'listEnemy.html'
    model = Minion
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['minions'] = Minion.objects.all()
        return context


def ReloadCharacter(*args, **kwargs):
    currentCharacter = kwargs['currentCharacter']
    return currentCharacter.reload()


def GettingXp(*args, **kwargs):
    currentCharacter = kwargs['character']
    currentStage = currentCharacter.party.stage
    for (stage, min_xp, max_xp) in [(100, 40, 50),
                                    (50, 30, 40),
                                    (10, 20, 30)]:
        if (currentStage % stage) == 0:
            xpGet = random.randint(min_xp, max_xp)
            break
        else:
            xpGet = random.randint(10, 20)
    currentCharacter.xp += xpGet
    currentCharacter.save()
    return currentCharacter.xp


def LevelUp(*args, **kwargs):
    pass