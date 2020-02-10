import math
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

        commonWeaponPull = Weapon.objects.filter(rarity="Common", requiredLevel=1,
                                                 characterClass=self.object.characterClass)
        pullCount = commonWeaponPull.count()
        if pullCount == 0 or random.randint(1, 100) <= 20:
            generateItem(stuffClassName='Weapon', stuffRarity='Common', adventurer=self.object)
            commonWeaponPull = Weapon.objects.filter(rarity="Common", requiredLevel=1,
                                                     characterClass=self.object.characterClass)
            pullCount = commonWeaponPull.count()
        randomCommonWeapon = commonWeaponPull[random.randint(0, pullCount - 1)]
        self.object.inventory.weapon = randomCommonWeapon
        self.object.inventory.save()

        commonConsumablePull = Consumable.objects.filter(Q(rarity="Common") | Q(rarity="Rare"))
        pullCount = commonConsumablePull.count()
        if pullCount == 0 or random.randint(1, 100) <= 20:
            generateItem(stuffClassName='Consumable', stuffRarity='Common' if random.randint(1, 2) == 1 else 'Rare',
                         adventurer=self.object)
            commonConsumablePull = Consumable.objects.filter(Q(rarity="Common") | Q(rarity="Rare"))
            pullCount = commonConsumablePull.count()
        randomPotion = commonConsumablePull[random.randint(0, pullCount - 1)]
        AddConsumable(stuffClassName="Consumable", inventory=self.object.inventory, consumable=randomPotion)

        commonHealingConsumablePull = Consumable.objects.filter(rarity="Common", hp__gt=0)
        pullCount = commonHealingConsumablePull.count()
        if pullCount == 0 or random.randint(1, 100) <= 20:
            generateItem(stuffClassName='Consumable', stuffRarity='Common', adventurer=self.object)
            commonHealingConsumablePull = Consumable.objects.filter(rarity="Common", hp__gt=0)
            pullCount = commonHealingConsumablePull.count()
        randomHealingCommonPotion = commonHealingConsumablePull[random.randint(0, pullCount - 1)]
        AddConsumable(stuffClassName="Consumable", inventory=self.object.inventory,
                      consumable=randomHealingCommonPotion)

        rareHealingConsumablePull = Consumable.objects.filter(rarity="Rare", hp__gt=0)
        pullCount = rareHealingConsumablePull.count()
        if pullCount == 0 or random.randint(1, 100) <= 20:
            generateItem(stuffClassName='Consumable', stuffRarity='Rare', adventurer=self.object)
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
                battleReport['0']['6'] = " l'ennemie si tien toujour devant pret a en d'acoudre !"
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
                battleReport['0']['6'] = " notre Héros est toujour debout mais pour encore combien de temps ?!"
                adventurer.setHp(-hpTab[0])
                p_e.hp -= hpTab[1]
                battleReport['1'] = hpTab[2]
                adventurer.save()
                p_e.save()
        if adventurer.hp <= 0:
            end = 'Cet énemie était bien superieur a ce héors malheurement, SOUILLEEEEEED'
            party.isEnded = True
            party.save()
            return JsonResponse({'isEnded': party.isEnded,
                                 'enemy': {
                                     'hp': p_e.hp
                                 },
                                 'character': ReloadCharacter(currentCharacter=adventurer),
                                 'battleReport': battleReport,
                                 'end': end
                                 })
        elif p_e.hp <= 0:
            end = "L'énemie s'est fait écraser sur ce dernier coup incompris de la population !"
            GettingXp(character=adventurer)
            return JsonResponse({'dropItem': DropItem(adventurer=adventurer),
                                 'isEnded': party.isEnded,

                                 'enemy': {
                                     'hp': p_e.hp
                                 },
                                 'character': ReloadCharacter(currentCharacter=adventurer),
                                 'battleReport': battleReport,
                                 'end': end
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
    aD20 = random.randint(0, 20)
    dD20 = random.randint(0, 20)
    assault = atk + aD20
    protection = res + dD20
    hit = assault - protection
    hpAtk = 0
    hpDef = 0
    battleReport = {'0': 'Voila que ' + atkObj.name + ' attaque',
                    '1': "Que les dés vous dessine un destin favorable !",
                    '2': atkObj.name + " 1D20 + atk = " + aD20.__str__() + ' + ' + atk.__str__() + ' = ' + assault.__str__(),
                    '3': 'et ' + defName + ' fait 1D20 + res = ' + dD20.__str__() + ' + ' + res.__str__() + ' = ' + protection.__str__()}
    if aD20 == 1:
        damage = getDamage(atk=atkObj)
        battleReport['4'] = atkObj.name + ' WTF il se rate lamentablement et fait un echec critque !!!!!'
        if damage >= 0:
            hpAtk = damage
            battleReport['5'] = 'LE HABAKIRIIIIIII de ' + damage.__str__() + ' damageeeees'
        else:
            battleReport[
                '5'] = "Heuresement que son armure est plus épaisse que ses muscle et ne s'inflige aucun damages !"
    else:
        damage = getDamage(atk=atkObj)
        if aD20 == 20:
            battleReport[
                '4'] = 'et... au mon dieu ?! ' + atkObj.name + ' !!! il transperce ' + defName + ' en faisant une réussite critque'
            damage *= 2
        if hit > 0:
            hpDef = damage
            battleReport['5'] = 'le coup part !!!! et lui fait ' + damage.__str__() + ' de damageeeeessss !!!!'
        else:
            battleReport['5'] = 'malheuresement il va falloir y mettre un du sien pour le fumé !!'
    return hpAtk, hpDef, battleReport


def dispactForStuff(*args, **kwargs):
    strengthPoints = 0
    agilityPoints = 0
    intelligencePoints = 0
    hpMaxPoints = 0
    physResPoints = 0
    MagResPoints = 0

    return [0, strengthPoints, agilityPoints, intelligencePoints, hpMaxPoints, physResPoints, MagResPoints,
            0, 0]


def dispatchForWeapon(*args, **kwargs):
    strengthPoints = 0
    agilityPoints = 0
    intelligencePoints = 0
    diceNumber = 0
    damage = 0

    return [0, strengthPoints, agilityPoints, intelligencePoints, 0, 0, 0,
            diceNumber, damage]


def dispatchForConsumable(*args, **kwargs):
    while True:
        isUpHP = False
        isUpStrength = False
        isUpAgility = False
        isUpIntellignece = False
        while not (isUpHP or isUpStrength or isUpAgility or isUpIntellignece):
            if random.randint(0, 1) == 1:
                isUpHP = True
            else:
                isUpHP = False
            if random.randint(0, 1) == 1:
                isUpStrength = True
            else:
                isUpStrength = False
            if random.randint(0, 1) == 1:
                isUpAgility = True
            else:
                isUpAgility = False
            if random.randint(0, 1) == 1:
                isUpIntellignece = True
            else:
                isUpIntellignece = False

        stuffPoint = kwargs['stuffPoint']
        print(f'Création d\'une potion avec {stuffPoint} points')
        hpPoints = 0
        strengthPoints = 0
        agilityPoints = 0
        intelligencePoints = 0
        while stuffPoint != 0 and (hpPoints + strengthPoints + agilityPoints + intelligencePoints) != kwargs['stuffPoint']:
            if isUpHP == True:
                hpPoints = random.randint(0, stuffPoint)
                stuffPoint -= hpPoints
            else:
                hpPoints = -random.randint(0, stuffPoint)
                stuffPoint -= hpPoints
            if isUpStrength == True:
                strengthPoints = random.randint(0, stuffPoint)
                stuffPoint -= strengthPoints
            else:
                strengthPoints = -random.randint(0, stuffPoint)
                stuffPoint -= strengthPoints
            if isUpAgility == True:
                agilityPoints = random.randint(0, stuffPoint)
                stuffPoint -= agilityPoints
            else:
                agilityPoints = -random.randint(0, stuffPoint)
                stuffPoint -= agilityPoints
            if isUpIntellignece == True:
                intelligencePoints = random.randint(0, stuffPoint)
                stuffPoint -= intelligencePoints
            else:
                intelligencePoints = -random.randint(0, stuffPoint)
                stuffPoint -= intelligencePoints
            print(
                f' Il reste {stuffPoint} points : {hpPoints} HP, {strengthPoints} FOR, {agilityPoints} AGI, {intelligencePoints} INT somme {hpPoints + strengthPoints + agilityPoints + intelligencePoints}')
        print(Consumable.objects.filter(hp=hpPoints*5,strength=strengthPoints,agility=agilityPoints,intelligence=intelligencePoints).count())
        if Consumable.objects.filter(hp=hpPoints*5,strength=strengthPoints,agility=agilityPoints,intelligence=intelligencePoints).count() == 0:
            break
    return [hpPoints * 5, strengthPoints, agilityPoints, intelligencePoints, 0, 0, 0,
            0, 0]


def dispacthPoints(*args, **kwargs):
    stuffPoint = kwargs['stuffPoint']
    stuffClassName = kwargs['stuffClassName']
    itemCharacterClassRequired = kwargs['itemCharacterClassRequired']
    ## spéaration en 3 partie dispatchForConsumable, dispatchForWeapon, dispatchForBasicStuff
    if stuffClassName == 'Consumable':
        dispacthPoints = dispatchForConsumable(stuffPoint=stuffPoint)
    elif stuffClassName == 'Weapon':
        dispacthPoints = dispatchForWeapon(stuffPoint=stuffPoint, itemCharacterClassRequired=itemCharacterClassRequired)
    else:
        dispacthPoints = dispactForStuff(stuffPoint=stuffPoint, itemCharacterClassRequired=itemCharacterClassRequired)
    hpPoints = dispacthPoints[0]
    strengthPoints = dispacthPoints[1]
    agilityPoints = dispacthPoints[2]
    intelligencePoints = dispacthPoints[3]
    physResPoints = dispacthPoints[4]
    MagResPoints = dispacthPoints[5]
    hpMaxPoints = dispacthPoints[6]
    diceNumber = dispacthPoints[7]
    damage = dispacthPoints[8]
    return [hpPoints, strengthPoints, agilityPoints, intelligencePoints, hpMaxPoints, physResPoints, MagResPoints,
            diceNumber, damage]


def calculPoints(*args, **kwargs):
    if kwargs['stuffClassName'] == 'Consumable':
        basicStuffPointByRarity = [1, 2, 3, 6]
    else:
        basicStuffPointByRarity = [2, 4, 6, 12]
    for (rarity, index) in [('Common', 0),
                            ('Rare', 1),
                            ('Epic', 2),
                            ('Legendary', 3)]:
        if kwargs['stuffRarity'] == rarity:
            return math.ceil(basicStuffPointByRarity[index] * (1 + 0.25 * (kwargs['itemLvlRequired'] - 1)))


def generateItem(*args, **kwargs):
    stuffClassName = kwargs['stuffClassName']
    stuffRarity = kwargs['stuffRarity']
    adventurer = kwargs['adventurer']
    itemCharacterClassRequired = adventurer.characterClass
    itemLvlRequired = random.randint(1, adventurer.level)
    stuffPointDispatch = dispacthPoints(
        stuffPoint=calculPoints(stuffRarity=stuffRarity, itemLvlRequired=itemLvlRequired,
                                stuffClassName=stuffClassName),
        stuffClassName=stuffClassName,
        itemCharacterClassRequired=itemCharacterClassRequired)
    if stuffClassName == 'Consumable':
        ItemDropped = Consumable(name='Poiton n°' + str(random.randint(0, 999999999)),
                                 rarity=stuffRarity,
                                 hp=stuffPointDispatch[0],
                                 strength=stuffPointDispatch[1],
                                 agility=stuffPointDispatch[2],
                                 intelligence=stuffPointDispatch[3])
    elif stuffClassName == 'Weapon':
        ItemDropped = Weapon(rarity=stuffRarity, requiredLevel=itemLvlRequired,
                             characterClass=itemCharacterClassRequired,
                             strength=stuffPointDispatch[1],
                             agility=stuffPointDispatch[2],
                             intelligence=stuffPointDispatch[3],
                             diceNumber=stuffPointDispatch[7],
                             damage=stuffPointDispatch[8])
    elif stuffClassName == 'Head':
        ItemDropped = Head(rarity=stuffRarity, requiredLevel=itemLvlRequired, characterClass=itemCharacterClassRequired,
                           hpMax=stuffPointDispatch[4],
                           physicalResistance=stuffPointDispatch[5],
                           magicalResistance=stuffPointDispatch[6],
                           strength=stuffPointDispatch[1],
                           agility=stuffPointDispatch[2],
                           intelligence=stuffPointDispatch[3])
    elif stuffClassName == 'Chest':
        ItemDropped = Chest(rarity=stuffRarity, requiredLevel=itemLvlRequired,
                            characterClass=itemCharacterClassRequired,
                            hpMax=stuffPointDispatch[4],
                            physicalResistance=stuffPointDispatch[5],
                            magicalResistance=stuffPointDispatch[6],
                            strength=stuffPointDispatch[1],
                            agility=stuffPointDispatch[2],
                            intelligence=stuffPointDispatch[3])
    else:
        ItemDropped = Leg(rarity=stuffRarity, requiredLevel=itemLvlRequired,
                          characterClass=itemCharacterClassRequired,
                          hpMax=stuffPointDispatch[4],
                          physicalResistance=stuffPointDispatch[5],
                          magicalResistance=stuffPointDispatch[6],
                          strength=stuffPointDispatch[1],
                          agility=stuffPointDispatch[2],
                          intelligence=stuffPointDispatch[3])
    ItemDropped.save()
    if stuffClassName == 'Consumable':
        data = {
            'isItemDropped': True,
            'stuffClassName': stuffClassName,
            'stuffRarity': stuffRarity,
            'stuffCount': 'generated object',
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
            'stuffCount': 'generated object',
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
    return data


def DropItem(**kwargs):
    ItemLevelRequired = random.randint(0, kwargs['adventurer'].level)
    if random.randint(1, 2) <= 2:
        stuffRarity = random.randint(1, 100)
        if 1 <= stuffRarity <= 50:
            stuffRarity = 'Common'
        elif 51 <= stuffRarity <= 89:
            stuffRarity = 'Rare'
        elif 90 <= stuffRarity <= 99:
            stuffRarity = 'Epic'
        else:
            stuffRarity = 'Legendary'
        stuffClass = random.randint(1, 6)
        if stuffClass <= 2:
            stuffClassName = 'Consumable'
            stuffPull = Consumable.objects.filter(rarity=stuffRarity)
            stuffCount = stuffPull.count()
            if stuffCount == 0 or random.randint(1, 100) <= 99:
                return generateItem(adventurer=kwargs['adventurer'], stuffClassName=stuffClassName,
                                    stuffRarity=stuffRarity)
            stuffCount = stuffPull.count()
            ItemDropped = stuffPull[random.randint(0, stuffCount - 1)]
        elif stuffClass == 3:
            stuffClassName = 'Head'
            stuffPull = Head.objects.filter(rarity=stuffRarity, characterClass=kwargs['adventurer'].characterClass,
                                            requiredLevel__lte=ItemLevelRequired)
            stuffCount = stuffPull.count()
            if stuffCount == 0 or random.randint(1, 100) <= 20:
                return generateItem(adventurer=kwargs['adventurer'], stuffClassName=stuffClassName,
                                    stuffRarity=stuffRarity)
            stuffCount = stuffPull.count()
            ItemDropped = stuffPull[random.randint(0, stuffCount - 1)]
        elif stuffClass == 4:
            stuffClassName = 'Chest'
            stuffPull = Chest.objects.filter(rarity=stuffRarity, characterClass=kwargs['adventurer'].characterClass,
                                             requiredLevel__lte=ItemLevelRequired)
            stuffCount = stuffPull.count()
            if stuffCount == 0 or random.randint(1, 100) <= 20:
                return generateItem(adventurer=kwargs['adventurer'], stuffClassName=stuffClassName,
                                    stuffRarity=stuffRarity)
            stuffCount = stuffPull.count()
            ItemDropped = stuffPull[random.randint(0, stuffCount - 1)]
        elif stuffClass == 5:
            stuffClassName = 'Leg'
            stuffPull = Leg.objects.filter(rarity=stuffRarity, characterClass=kwargs['adventurer'].characterClass,
                                           requiredLevel__lte=ItemLevelRequired)
            stuffCount = stuffPull.count()
            if stuffCount == 0 or random.randint(1, 100) <= 20:
                return generateItem(adventurer=kwargs['adventurer'], stuffClassName=stuffClassName,
                                    stuffRarity=stuffRarity)
            stuffCount = stuffPull.count()
            ItemDropped = stuffPull[random.randint(0, stuffCount - 1)]
        else:
            stuffClassName = 'Weapon'
            stuffPull = Weapon.objects.filter(rarity=stuffRarity,
                                              characterClass=kwargs['adventurer'].characterClass,
                                              requiredLevel__lte=ItemLevelRequired)
            stuffCount = stuffPull.count()
            if stuffCount == 0 or random.randint(1, 100) <= 20:
                return generateItem(adventurer=kwargs['adventurer'], stuffClassName=stuffClassName,
                                    stuffRarity=stuffRarity)
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
