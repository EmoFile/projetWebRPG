import random, datetime

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
from django.db.models.signals import pre_save
from django.dispatch import receiver
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
        return random.randint(self.minHpMax, self.maxHpMax,1)

    def generateStrength(self):
        return random.randint(self.minStrength, self.maxStrength,1)

    def generateAgility(self):
        return random.randint(self.minAgility, self.maxAgility,1)

    def generateIntelligence(self):
        return random.randint(self.minInt, self.maxInt,1)

    def generatePR(self):
        return random.randint(self.minPhysRes, self.maxPhysRes,1)

    def generateMR(self):
        return random.randint(self.minMagRes, self.maxMagRes,1)


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
    xp =  models.PositiveIntegerField(default=0,
                                        blank=False,
                                        null=False)
    hpMax = models.PositiveIntegerField(default=10,
                                        validators=[MinValueValidator(0)],
                                        blank=False,
                                        null=False)
    hp = models.IntegerField(default=10,
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
    
    def modifyCarac(self, item):
        if item._meta.object_name == 'Consumable':
            self.hp += item.hp
            self.strength += item.strength
            self.agility += item.agility
            self.intelligence += item.intelligence
        else:
            self.hpMax += item.hpMax
            self.hp += item.hp
            self.strength += item.strength
            self.agility += item.agility
            self.intelligence += item.intelligence
            self.physicalResistance += item.physicalResistance
            self.magicalResistance += item.magicalResistance
    
    def getHpMax(self):
        hpMax = self.hpMax
        if self.inventory.head is not None:
            hpMax += self.inventory.head.hpMax
        if self.inventory.chest is not None:
            hpMax += self.inventory.chest.hpMax
        if self.inventory.leg is not None:
            hpMax += self.inventory.leg.hpMax
        if self.inventory.weapon is not None:
            hpMax += self.inventory.weapon.hpMax
        return hpMax
    
    def getStrength(self):
        strength = self.strength
        if self.inventory.head is not None:
            strength += self.inventory.head.strength
        if self.inventory.chest is not None:
            strength += self.inventory.chest.strength
        if self.inventory.leg is not None:
            strength += self.inventory.leg.strength
        if self.inventory.weapon is not None:
            strength += self.inventory.weapon.strength
        return strength
    
    def getAgility(self):
        agility = self.agility
        if self.inventory.head is not None:
            agility += self.inventory.head.agility
        if self.inventory.chest is not None:
            agility += self.inventory.chest.agility
        if self.inventory.leg is not None:
            agility += self.inventory.leg.agility
        if self.inventory.weapon is not None:
            agility += self.inventory.weapon.agility
        return agility
    
    def getIntelligence(self):
        intelligence = self.intelligence
        if self.inventory.head is not None:
            intelligence += self.inventory.head.intelligence
        if self.inventory.chest is not None:
            intelligence += self.inventory.chest.intelligence
        if self.inventory.leg is not None:
            intelligence += self.inventory.leg.intelligence
        if self.inventory.weapon is not None:
            intelligence += self.inventory.weapon.intelligence
        return intelligence
    
    def getPhysicalResistance(self):
        physicalResistance = self.physicalResistance
        if self.inventory.head is not None:
            physicalResistance += self.inventory.head.physicalResistance
        if self.inventory.chest is not None:
            physicalResistance += self.inventory.chest.physicalResistance
        if self.inventory.leg is not None:
            physicalResistance += self.inventory.leg.physicalResistance
        if self.inventory.weapon is not None:
            physicalResistance += self.inventory.weapon.physicalResistance
        return physicalResistance
    
    def getMagicalResistance(self):
        magicalResistance = self.magicalResistance
        if self.inventory.head is not None:
            magicalResistance += self.inventory.head.magicalResistance
        if self.inventory.chest is not None:
            magicalResistance += self.inventory.chest.magicalResistance
        if self.inventory.leg is not None:
            magicalResistance += self.inventory.leg.magicalResistance
        if self.inventory.weapon is not None:
            magicalResistance += self.inventory.weapon.magicalResistance
        return magicalResistance

    def reload(self):
        return {
            'hpMax': self.getHpMax(),
            'hp': self.hp,
            'strength': self.getStrength(),
            'agility': self.getAgility(),
            'intelligence': self.getIntelligence(),
            'physicalResistance': self.getPhysicalResistance(),
            'magicalResistance': self.getMagicalResistance()
        }


class Item(models.Model):
    class Meta:
        abstract = True
        unique_together = [['name']]

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
    stage = models.PositiveIntegerField(default=0,
                                        validators=[MinValueValidator(0)],
                                        blank=False,
                                        null=False)
    date = models.DateField("Date", default=datetime.date.today)
    isEnded = models.BooleanField(default=False)
    enemies = models.ManyToManyField('Enemy', through='PartyEnemy')

    class Meta:
        unique_together = ['character']

    def __str__(self):
        return f'{self.id}: {self.user.username} ' \
               f'{self.character} ' \
               f'{self.stage}'


class Enemy(models.Model):
    default = {
               'blank': False,
               'null': False}
    name = models.CharField(max_length=20,
                            default='un mec',
                            blank=False,
                            null=False)
    hpMax = models.PositiveIntegerField(default=10, **default)
    hp = models.PositiveIntegerField(default=10, **default)
    strength = models.IntegerField(default=1, **default)
    agility = models.IntegerField(default=1, **default)
    intelligence = models.IntegerField(default=1, **default)
    physical_resistance = models.IntegerField(default=0, **default)
    magical_resistance = models.IntegerField(default=0, **default)
    is_boss = models.BooleanField(default=False)
    next = models.ForeignKey('self', default=None, on_delete=models.CASCADE, blank=True, null=True)

    def is_minion(self):
        return hasattr(self, 'minion')

    @classmethod
    def create(cls, adventurer, min_percent, max_percent, min_percent_def,
               max_percent_def, name, *args, **kwargs):
        """
        :param adventurer: Character Adventurer
        :param min_percent:
        :param max_percent:
        :param min_percent_def:
        :param max_percent_def:
        :param name:
        :return: Enemy
        """
        hpMax = round(random.uniform(
            adventurer.hpMax + (adventurer.hpMax * min_percent) / 100,
            adventurer.hpMax + (adventurer.hpMax * max_percent) / 100))
        strength = round(random.uniform(
            adventurer.physicalResistance - (
                    adventurer.physicalResistance * min_percent_def) / 100,
            adventurer.physicalResistance - (
                    adventurer.physicalResistance * max_percent_def) / 100))
        intelligence = round(random.uniform(
            adventurer.magicalResistance - (
                    adventurer.magicalResistance * min_percent_def) / 100,
            adventurer.magicalResistance - (
                    adventurer.magicalResistance * max_percent_def) / 100))
        physical_resistance = round(random.uniform(
            adventurer.strength + (
                    adventurer.strength * min_percent_def) / 100,
            adventurer.strength + (
                    adventurer.strength * max_percent_def) / 100))
        magical_resistance = round(random.uniform(
            adventurer.intelligence + (
                    adventurer.intelligence * min_percent_def) / 100,
            adventurer.intelligence + (
                    adventurer.intelligence * max_percent_def) / 100))
        agility = round(random.uniform(adventurer.agility - 10,
                                 adventurer.agility + 10))
        hp = hpMax
        return cls(hpMax=hpMax, strength=strength, intelligence=intelligence,
                   physical_resistance=physical_resistance,
                   magical_resistance=magical_resistance,
                   agility=agility, hp=hp, name=name, *args, **kwargs)


class Minion(Enemy):
    def __str__(self):
        return f'{self.id}: {self.name} ' \
               f'|HpM: {self.hpMax}' \
               f'|hp: {self.hp}' \
               f'|Str: {self.strength}' \
               f'|Ag: {self.agility}' \
               f'|Int: {self.intelligence}'\
               f'|Next: {str(self.next) if self.next is not None else None}]'

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
        return super().create(adventurer, min_percent, max_percent,
                              min_percent_def, max_percent_def, name)


class BossAlain(Enemy):
    def __str__(self):
        return f'{self.id}: {self.name} ' \
               f'|HpM: {self.hpMax}' \
               f'|hp: {self.hp}' \
               f'|Str: {self.strength}' \
               f'|Ag: {self.agility}' \
               f'|Int: {self.intelligence}'\
               f'|Next {str(self.next) if self.next is not None else None}]'

    @classmethod
    def create(cls, stage, adventurer, **kwargs):
        """
        :param stage: level stage
        :param adventurer: Charactere Adventurer
        :param kwargs:
        :return: BossAlain
        """
        cls.is_boss = True
        k = random.randint(7, 9)
        min_percent_def = (30 * k - 330) / 11
        max_percent_def = (7 * k - 69) / 3

        min_percent = max_percent = name = None
        for (percent, p_min, p_max, title) in [(100, 70, 100, 'King Alain'),
                                               (50, 60, 70, 'General Alain'),
                                               (10, 50, 60, 'Soldier Alain')]:
            if (stage % percent) == 0:
                min_percent = p_min
                max_percent = p_max
                name = title
                break
        if name is None:
            print("t'es pas censé être la mec t'a lancer une fonction au mauvais stage")
            return None
        return super().create(adventurer,
                              min_percent, max_percent,
                              min_percent_def, max_percent_def, name)


class PartyEnemy(models.Model):
    party = models.ForeignKey(Party,
                              on_delete=models.PROTECT)
    enemy = models.ForeignKey(Enemy,
                              on_delete=models.PROTECT)
    hp = models.IntegerField(default=0,
                                     blank=False,
                                     null=False)

    def __str__(self):
        return f'{self.id}: {self.party.character.name} | {self.enemy.name} | {self.hp}'

# @receiver(pre_save, sender=Enemy)
# def pre_save_enemy_handle(sender, instance, created, **kwargs):
#     if created:
#         if isinstance(instance, BossAlain):
#         elif
