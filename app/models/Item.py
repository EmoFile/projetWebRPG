import random

from django.core.validators import MinValueValidator
from django.db import models

from app.models import CharacterClass


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
    name = models.CharField(max_length=250,
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
                                       default=1,
                                       on_delete=models.CASCADE,
                                       related_name='weaponCharacterClass')
    diceNumber = models.PositiveIntegerField(default=1,
                                             blank=False,
                                             null=False)
    damage = models.PositiveIntegerField(default=4,
                                         blank=False,
                                         null=False)

    def __str__(self):
        return f'{self.id}: {self.name} ' \
               f'[Lvl: {self.requiredLevel}' \
               f'|Class: {self.characterClass.name}' \
               f'|1H: {self.oneHanded}' \
               f'|Str: {self.strength}' \
               f'|Ag:{self.agility}' \
               f'|Int: {self.intelligence}]'

    def getDamage(self):
        damage = 0
        for i in range(0, self.diceNumber):
            damage += random.randint(1,self.damage)
        return damage


class Head(Stuff):
    characterClass = models.ForeignKey(CharacterClass,
                                       default=1,
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
                                       default=1,
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
                                       default=1,
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
