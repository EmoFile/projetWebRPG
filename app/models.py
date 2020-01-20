import random, datetime

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
from django.urls import reverse


class CharacterClass(models.Model):
    name = models.CharField(max_length=20,
                            blank=True,
                            null=True)
    minHpMax = models.PositiveIntegerField(default=10,
                                           validators=[MinValueValidator(5)],
                                           blank=False,
                                           null=False)
    maxHpMax = models.PositiveIntegerField(default=20,
                                           validators=[MinValueValidator(10)],
                                           blank=False,
                                           null=False)
    minStrength = models.IntegerField(default=-10,
                                      blank=False,
                                      null=False)
    maxStrength = models.IntegerField(default=10,
                                      blank=False,
                                      null=False)
    minAgility = models.IntegerField(default=-10,
                                     blank=False,
                                     null=False)
    maxAgility = models.IntegerField(default=10,
                                     blank=False,
                                     null=False)
    minInt = models.IntegerField(default=-10,
                                 blank=False,
                                 null=False)
    maxInt = models.IntegerField(default=10,
                                 blank=False,
                                 null=False)
    minPhysRes = models.IntegerField(default=-10,
                                     blank=False,
                                     null=False)
    maxPhysRes = models.IntegerField(default=10,
                                     blank=False,
                                     null=False)
    minMagRes = models.IntegerField(default=-10,
                                    blank=False,
                                    null=False)
    maxMagRes = models.IntegerField(default=10,
                                    blank=False,
                                    null=False)
    
    def __str__(self):
        return f'{self.id}: {self.name}'
    
    def generateHpMax(self):
        return random.randint(self.minHpMax, self.maxHpMax)
    
    def generateStrength(self):
        return random.randint(self.minStrength, self.maxStrength)
    
    def generateAgility(self):
        return random.randint(self.minAgility, self.maxAgility)
    
    def generateIntelligence(self):
        return random.randint(self.minInt, self.maxInt)
    
    def generatePR(self):
        return random.randint(self.minPhysRes, self.maxPhysRes)
    
    def generateMR(self):
        return random.randint(self.minMagRes, self.maxMagRes)


# USELESS CAR PBR DE TROP NOMBREUX CALL LES UN DANS LES AUTRES MAIS C4EST
# CHELOU DONC A MONTRER A PONS
# def getRadomCarac(self):
#     return {'hpMax': self.generateHpMax(),
#             'strength': self.generateStrength(),
#             'agility': self.generateAgility(),
#             'intelligence': self.generateIntelligence(),
#             'physicalResistance': self.generatePR(),
#             'magicalResistance': self.getRadomCarac()}


class Character(models.Model):
    name = models.CharField(max_length=20,
                            default='Jon Doe',
                            blank=False,
                            null=False)
    characterClass = models.ForeignKey(CharacterClass,
                                       on_delete=models.CASCADE,
                                       related_name='characterClass')
    level = models.PositiveIntegerField(default=1,
                                        validators=[MinValueValidator(1)],
                                        blank=False,
                                        null=False)
    hpMax = models.PositiveIntegerField(default=10,
                                        validators=[MinValueValidator(0)],
                                        blank=False,
                                        null=False)
    hp = models.PositiveIntegerField(default=10,
                                     validators=[MinValueValidator(0)],
                                     blank=False,
                                     null=False)
    strength = models.IntegerField(default=1,
                                   blank=False,
                                   null=False)
    agility = models.IntegerField(default=1,
                                  blank=False,
                                  null=False)
    intelligence = models.IntegerField(default=1,
                                       blank=False,
                                       null=False)
    physicalResistance = models.IntegerField(default=0,
                                             blank=False,
                                             null=False)
    magicalResistance = models.IntegerField(default=0,
                                            blank=False,
                                            null=False)
    inventory = models.OneToOneField('Inventory',
                                     on_delete=models.PROTECT)
    
    def __str__(self):
        return f'{self.id}: {self.name} ' \
               f'[Lvl: {self.level}' \
               f'|Class: {self.characterClass}' \
               f'|HpM: {self.hpMax}' \
               f'|hp: {self.hp}' \
               f'|Str: {self.strength}' \
               f'|Ag: {self.agility}' \
               f'|Int: {self.intelligence}' \
               f'|Pr: {self.physicalResistance}' \
               f'|Mr: {self.magicalResistance}]'


class Item(models.Model):
    class Meta:
        abstract = True
    
    COMMON = 'Common'
    RARE = 'Rare'
    EPIC = 'Epic'
    LEGENDARY = 'Legendary'
    RARITY_CHOICES = [
        (COMMON, 'Common'),
        (RARE, 'Rare'),
        (EPIC, 'Epic'),
        (LEGENDARY, 'Legendary'),
    ]
    name = models.CharField(max_length=40,
                            default='New Item',
                            blank=False,
                            null=False)
    rarity = models.CharField(max_length=10,
                              choices=RARITY_CHOICES,
                              default=COMMON
                              )
    strength = models.IntegerField(default=0,
                                   blank=False,
                                   null=False)
    agility = models.IntegerField(default=0,
                                  blank=False,
                                  null=False)
    intelligence = models.IntegerField(default=0,
                                       blank=False,
                                       null=False)


class Stuff(Item):
    class Meta:
        abstract = True
    
    requiredLevel = models.PositiveIntegerField(default=1,
                                                validators=[
                                                    MinValueValidator(1)],
                                                blank=False,
                                                null=False)
    hpMax = models.IntegerField(default=0,
                                blank=False,
                                null=False)
    physicalResistance = models.IntegerField(default=0,
                                             blank=False,
                                             null=False)
    magicalResistance = models.IntegerField(default=0,
                                            blank=False,
                                            null=False)


class Weapon(Stuff):
    oneHanded = models.BooleanField(default=True)
    characterClass = models.ForeignKey(CharacterClass,
                                       on_delete=models.CASCADE,
                                       related_name='weaponCharacterClass')
    
    def __str__(self):
        return f'{self.id}: {self.name} ' \
               f'[Lvl: {self.requiredLevel}' \
               f'|Class: {self.characterClass.name}' \
               f'|1H: {self.oneHanded}' \
               f'|Str: {self.strength}' \
               f'|Ag:{self.agility}' \
               f'|Int: {self.intelligence}]'


class Head(Stuff):
    characterClass = models.ForeignKey(CharacterClass,
                                       on_delete=models.CASCADE,
                                       related_name='headCharacterClass')
    
    def __str__(self):
        return f'{self.id}: {self.name} ' \
               f'[Lvl: {self.requiredLevel}' \
               f'|Class: {self.characterClass.name}' \
               f'|HpM: {self.hpMax}' \
               f'|Str: {self.strength}' \
               f'|Ag:{self.agility}' \
               f'|Int: {self.intelligence}' \
               f'|Pr: {self.physicalResistance}' \
               f'|Mr: {self.magicalResistance}]'


class Chest(Stuff):
    characterClass = models.ForeignKey(CharacterClass,
                                       on_delete=models.CASCADE,
                                       related_name='chestCharacterClass')
    
    def __str__(self):
        return f'{self.id}: {self.name} ' \
               f'[Lvl: {self.requiredLevel}' \
               f'|Class : {self.characterClass.name}' \
               f'|HpM: {self.hpMax}' \
               f'|Str: {self.strength}' \
               f'|Ag:{self.agility}' \
               f'|Int: {self.intelligence}' \
               f'|Pr: {self.physicalResistance}' \
               f'|Mr: {self.magicalResistance}]'


class Leg(Stuff):
    characterClass = models.ForeignKey(CharacterClass,
                                       on_delete=models.CASCADE,
                                       related_name='legCharacterClass')
    
    def __str__(self):
        return f'{self.id}: {self.name} ' \
               f'[Lvl: {self.requiredLevel}' \
               f'|Class: {self.characterClass.name}' \
               f'|HpM: {self.hpMax}' \
               f'|Str: {self.strength}' \
               f'|Ag:{self.agility}' \
               f'|Int: {self.intelligence}' \
               f'|Pr: {self.physicalResistance}' \
               f'|Mr: {self.magicalResistance}]'


class Consumable(Item):
    hp = models.IntegerField(default=0,
                             validators=[MinValueValidator(0)],
                             blank=False,
                             null=False)
    
    def __str__(self):
        return f'{self.id}: {self.name} ' \
               f'[Hp: {self.hp}' \
               f'|Str: {self.strength}' \
               f'|Ag:{self.agility}' \
               f'|Int: {self.intelligence}]'


class Inventory(models.Model):
    head = models.ForeignKey(Head,
                             on_delete=models.CASCADE,
                             related_name='headInventory',
                             blank=True,
                             null=True)
    chest = models.ForeignKey(Chest,
                              on_delete=models.CASCADE,
                              related_name='chestInventory',
                              blank=True,
                              null=True)
    leg = models.ForeignKey(Leg,
                            on_delete=models.CASCADE,
                            related_name='legInventory',
                            blank=True,
                            null=True)
    weapon = models.ForeignKey(Weapon,
                               on_delete=models.CASCADE,
                               related_name='weaponInventory',
                               blank=True,
                               null=True)
    consumables = models.ManyToManyField('Consumable',
                                         through='InventoryConsumable')


class InventoryConsumable(models.Model):
    inventory = models.ForeignKey(Inventory,
                                  on_delete=models.PROTECT)
    consumable = models.ForeignKey(Consumable,
                                   on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0,
                                           blank=False,
                                           null=False)
    
    def __str__(self):
        return f'{self.id}: {self.consumable.name} {self.quantity}'


class Party(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT)
    character = models.OneToOneField(Character,
                                     on_delete=models.PROTECT)
    stage = models.PositiveIntegerField(default=1,
                                        validators=[MinValueValidator(1)],
                                        blank=False,
                                        null=False)
    date = models.DateField("Date", default=datetime.date.today)
    
    class Meta:
        unique_together = ['character']
    
    def __str__(self):
        return f'{self.id}: {self.user.username} ' \
               f'{self.character} ' \
               f'{self.stage}'


class Enemy(models.Model):
    class Meta:
        abstract = True
    
    name = models.CharField(max_length=20,
                            default='un mec',
                            blank=False,
                            null=False)
    hpMax = models.PositiveIntegerField(default=10,
                                        validators=[MinValueValidator(0)],
                                        blank=False,
                                        null=False)
    hp = models.PositiveIntegerField(default=10,
                                     validators=[MinValueValidator(0)],
                                     blank=False,
                                     null=False)
    strength = models.IntegerField(default=1,
                                   validators=[MinValueValidator(0)],
                                   blank=False,
                                   null=False)
    agility = models.IntegerField(default=1,
                                  validators=[MinValueValidator(0)],
                                  blank=False,
                                  null=False)
    intelligence = models.IntegerField(default=1,
                                       validators=[MinValueValidator(0)],
                                       blank=False,
                                       null=False)
    physical_resistance = models.IntegerField(default=0,
                                              validators=[MinValueValidator(0)],
                                              blank=False,
                                              null=False)
    magical_resistance = models.IntegerField(default=0,
                                             validators=[MinValueValidator(0)],
                                             blank=False,
                                             null=False)
    
    @classmethod
    def create(cls, adventurer, min_percent, max_percent, min_percent_def,
               max_percent_def, name):
        '''
        :param adventurer: Charactere Adventurer
        :param min_percent:
        :param max_percent:
        :param min_percent_def:
        :param max_percent_def:
        :param name:
        :return: Enemy
        '''
        hpMax = random.uniform(
            round(adventurer.hpMax + (adventurer.hpMax * min_percent) / 100),
            round(adventurer.hpMax + (adventurer.hpMax * max_percent) / 100))
        strength = random.uniform(
            round(adventurer.physicalResistance - (
                adventurer.physicalResistance * min_percent_def) / 100),
            round(adventurer.physicalResistance - (
                adventurer.physicalResistance * max_percent_def) / 100))
        intelligence = random.uniform(
            round(adventurer.magicalResistance - (
                adventurer.magicalResistance * min_percent_def) / 100),
            round(adventurer.magicalResistance - (
                adventurer.magicalResistance * max_percent_def) / 100))
        physical_resistance = random.uniform(
            round(adventurer.strength + (
                adventurer.strength * min_percent_def) / 100),
            round(adventurer.strength + (
                adventurer.strength * max_percent_def) / 100))
        magical_resistance = random.uniform(
            round(adventurer.intelligence + (
                adventurer.intelligence * min_percent_def) / 100),
            round(adventurer.intelligence + (
                adventurer.intelligence * max_percent_def) / 100))
        agility = random.uniform(adventurer.agility - 10,
                                 adventurer.agility + 10)
        hp = hpMax
        return cls(hpMax=hpMax, strength=strength, intelligence=intelligence,
                   physical_resistance=physical_resistance,
                   magical_resistance=magical_resistance,
                   agility=agility, hp=hp, name=name)


class Minion(Enemy):
    def __str__(self):
        return f'{self.id}: {self.name} ' \
               f'|HpM: {self.hpMax}' \
               f'|hp: {self.hp}' \
               f'|Str: {self.strength}' \
               f'|Ag: {self.agility}' \
               f'|Int: {self.intelligence}]'
    
    @classmethod
    def create(cls, adventurer, i, **kwargs):
        """
        :param adventurer: Charactere Adventurer
        :param i: placement number of Minion (itération)
        :param kwargs:
        :return: Minion
        """
        min_percent = (i - 1) * 3
        max_percent = (i + 2) * 3
        min_percent_def = (30 * i - 330) / 11
        max_percent_def = (7 * i - 69) / 3
        name = "un sbire d'Alain"
        return super(Minion, cls).create(adventurer, min_percent, max_percent,
                                         min_percent_def, max_percent_def, name)


class BossAlain(Enemy):
    def __str__(self):
        return f'{self.id}: {self.name} ' \
               f'|HpM: {self.hpMax}' \
               f'|hp: {self.hp}' \
               f'|Str: {self.strength}' \
               f'|Ag: {self.agility}' \
               f'|Int: {self.intelligence}]'
    
    @classmethod
    def create(cls, stage, adventurer, **kwargs):
        """
        :param stage: level stage
        :param adventurer: Charactere Adventurer
        :param kwargs:
        :return: BossAlain
        """
        k = random.randint(7, 9)
        min_percent_def = (30 * k - 330) / 11
        max_percent_def = (7 * k - 69) / 3
        if (stage % 100) == 0:
            print("KingAlain is comming for you")
            min_percent = 70
            max_percent = 100
            name = 'KingAlain'
        elif (stage % 50) == 0:
            print("GeneralAlain is comming for you")
            min_percent = 60
            max_percent = 70
            name = 'GeneralAlain'
        elif (stage % 10) == 0:
            print("SoldierAlain is comming for you")
            min_percent = 50
            max_percent = 60
            name = 'SoldierAlain'
        else:
            print(
                "t'es pas censé être la mec t'a lancer une fonction au mauvais stage")
        return super(BossAlain, cls).create(adventurer, min_percent,
                                            max_percent, min_percent_def,
                                            max_percent_def, name)
