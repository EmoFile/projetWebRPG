import random

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
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

        commonWeaponPull = Weapon.objects.filter(rarity="Common", characterClass=self.object.characterClass)
        pullCount = commonWeaponPull.count()
        randomCommonWeapon = commonWeaponPull[random.randint(0, pullCount - 1)]

        self.object.inventory.weapon = randomCommonWeapon
        self.object.inventory.save()

        commonConsumablePull = Consumable.objects.filter(Q(rarity="Common") | Q(rarity="Rare"))
        pullCount = commonConsumablePull.count()
        randomPotion = commonConsumablePull[random.randint(0, pullCount - 1)]
        AddConsumable(stuffClassName="Consumable", inventory=self.object.inventory, consumable=randomPotion)

        commonHealingConsumablePull = Consumable.objects.filter(rarity="Common", hp__gt=0)
        pullCount = commonHealingConsumablePull.count()
        randomHealingCommonPotion = commonHealingConsumablePull[random.randint(0, pullCount - 1)]
        AddConsumable(stuffClassName="Consumable", inventory=self.object.inventory,
                      consumable=randomHealingCommonPotion)

        rareHealingConsumablePull = Consumable.objects.filter(rarity="Rare", hp__gt=0)
        pullCount = rareHealingConsumablePull.count()
        randomHealingRarePotion = rareHealingConsumablePull[random.randint(0, pullCount - 1)]
        AddConsumable(stuffClassName="Consumable", inventory=self.object.inventory, consumable=randomHealingRarePotion)

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
            hpTab = fight(atkAdventurer, defAdventurer, adventurer, resEnemy, enemy.name)
            adventurer.setHp(-hpTab[0])
            p_e.hp -= hpTab[1]
            battleReport = {'0': hpTab[2]}
            adventurer.save()
            p_e.save()
            if p_e.hp > 0 and adventurer.hp > 0:
                hpTab = fight(atkEnemy, defEnemy, enemy, resAdventurer, adventurer.name)
                p_e.hp -= hpTab[0]
                adventurer.setHp(-hpTab[1])
                battleReport['1'] = hpTab[2]
                p_e.save()
                adventurer.save()
        else:
            hpTab = fight(atkEnemy, defEnemy, enemy, resAdventurer, adventurer.name)
            p_e.hp -= hpTab[0]
            adventurer.setHp(-hpTab[1])
            battleReport = {'0': hpTab[2]}
            p_e.save()
            adventurer.save()
            if p_e.hp > 0 and adventurer.hp > 0:
                hpTab = fight(atkAdventurer, defAdventurer, adventurer, resEnemy, enemy.name)
                adventurer.setHp(-hpTab[0])
                p_e.hp -= hpTab[1]
                battleReport['1'] = hpTab[2]
                adventurer.save()
                p_e.save()
        if adventurer.hp <= 0:
            end = {
                "This enemy was far superior to this hero, unfortunately..., SOUILLED",
                "It could have gone well... but it didn't."
            }
            party.isEnded = True
            party.save()
            return JsonResponse({'isEnded': party.isEnded,
                                 'enemy': {
                                     'hp': p_e.hp
                                 },
                                 'character': ReloadCharacter(currentCharacter=adventurer),
                                 'battleReport': battleReport,
                                 'end': random.choice(list(end))
                                 })
        elif p_e.hp <= 0:
            end = {
                "The Enemy has been crushed on this latest misunderstood coup by the population!",
                "You're doing well so far, Hero... but what will you do when your enemies measure up to you?"
            }
            GettingXp(character=adventurer)
            return JsonResponse({'dropItem': DropItem(adventurer=adventurer),
                                 'isEnded': party.isEnded,

                                 'enemy': {
                                     'hp': p_e.hp
                                 },
                                 'character': ReloadCharacter(currentCharacter=adventurer),
                                 'battleReport': battleReport,
                                 'end': random.choice(list(end))
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


def getDamage(*args, **kwargs):
    currantAtk = kwargs['atk']
    if currantAtk.__class__.__name__ == "Character":
        if currantAtk.inventory.weapon:
            return currantAtk.inventory.weapon.getDamage()
        else:
            damage = 0
            for i in range(0, 2):
                damage += random.randint(1, round(currantAtk.strength / 4))
            return damage
    else:
        return currantAtk.getDamage()


def fight(atk, atkDef, atkObj, res, defName):
    announce = {
        atkObj.name + " is getting ready to attack.",
        atkObj.name + " is getting closer!",
        atkObj.name + " gives a black look to his enemy...",
    }
    dice_announce = {
        "It's time to roll the dice.",
        "May the dice guide you to a favourable destiny.",
        "Fortune favors you, my friend!"
    }
    aD20 = random.randint(0, 20)
    dD20 = random.randint(0, 20)
    attack_dice = {
        atkObj.name + " throws a D20 for attack and goes " + aD20.__str__(),
        "The dice we choose! And it will be " + aD20.__str__() + " on the D20 attack from " + atkObj.name
    }
    defence_dice = {
        defName + "doesn't let up and throws a D20 in his defense and goes... " + dD20.__str__(),
        defName + " says a prayer before throwing his d20 and does " + dD20.__str__()
    }
    assault = atk + aD20
    protection = res + dD20
    hit = assault - protection
    hpAtk = 0
    hpDef = 0
    battleReport = {'0': random.choice(list(announce)),
                    '1': random.choice(list(dice_announce)),
                    '2': random.choice(list(attack_dice)),
                    '3': random.choice(list(defence_dice))
                    }
    if aD20 == 1:
        damage = getDamage(atk=atkObj)
        critical_failure = {
            "OMG why" + atkObj.name + " is so dumb dude ??? He wants to kill himself ???",
            "Well, let him keep this up and he'll never be remembered.",
            "How?! He must really suck at dice?!"
        }
        battleReport['4'] = random.choice(list(critical_failure))
        if damage >= 0:
            hpAtk = damage
            critical_failure_damages = {
                "THE HABAKIRIIIIIIII, " + atkObj.name + " takes " + damage.__str__() + " of damages",
                "He stumbled and put his finger in his eye unfortunately he did " + damage.__str__() + " damages"
            }
            battleReport['5'] = random.choice(list(critical_failure_damages))
        else:
            critical_failure_nothing = {
                atkObj.name + " even manages to miss his suicide... The population is disappointed",
                "fortunately his clothes are thicker than his muscles..."
            }
            battleReport['5'] = random.choice(list(critical_failure_nothing))
    else:
        damage = getDamage(atk=atkObj)
        if aD20 == 20:
            success_critcal = {
                atkObj.name + " does his most murderous and darkSasuke look.",
                "All his muscles are contracting ! Are those veins in his forehead ? Or a tumor ?",
                atkObj.name + " brandished his weapon! The dice were with him now his mind and strength are one!"
            }
            battleReport['4'] = random.choice(list(success_critcal))
            damage *= 2
        if hit > 0:
            hpDef = damage
            success_damage = {
                atkObj.name + "attacks and does" + damage.__str__() + " damages to his opponent!",
                atkObj.name + "is not at his peak but still does " + damage.__str__() + " damages."
            }
            success_critcal_damage = {
                "Oh, my God! It wasn't all for nothing, that murderous atmosphere! " + atkObj.name + " inflicts " + damage.__str__() + " damages to his opponent !",
                "so much power !!!! he does " + damage.__str__() + " damages"
            }
            if aD20 == 20:
                battleReport['5'] = random.choice(list(success_critcal_damage))
            else:
                battleReport['5'] = random.choice(list(success_damage))
        else:
            failure_damage = {
                "all for this...",
                "I didn't expect anything, but I'm still disappointed.",
                "A lot of muscle for a big thing, this " + atkObj.name
            }
            battleReport['5'] = random.choice(list(failure_damage))
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
        minion = Minion.create(adventurer, i, kwargs['stage'] + i)
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
