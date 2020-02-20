import math

from django.core.validators import MinValueValidator
from django.db import models

from app.models import CharacterClass


class Character(models.Model):
    name = models.CharField(max_length=20,
                            default='Jon Doe',
                            blank=False,
                            null=False)
    characterClass = models.ForeignKey(CharacterClass,
                                       default=1,
                                       on_delete=models.CASCADE,
                                       related_name='characterClass')
    level = models.PositiveIntegerField(default=1,
                                        validators=[MinValueValidator(1)],
                                        blank=False,
                                        null=False)
    xp = models.PositiveIntegerField(default=0,
                                     blank=False,
                                     null=False)
    hpMax = models.IntegerField(default=10,
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
                                     default=1,
                                     blank=True,
                                     null=True,
                                     on_delete=models.SET_NULL)

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
            self.setHp(item.hp)
            self.strength += item.strength
            self.agility += item.agility
            self.intelligence += item.intelligence
        else:
            self.setHpMax(item.hpMax)
            self.setHp(item.hp)
            self.strength += item.strength
            self.agility += item.agility
            self.intelligence += item.intelligence
            self.physicalResistance += item.physicalResistance
            self.magicalResistance += item.magicalResistance

    def getHpMax(self):
        return self.hpMax

    def getStrength(self):
        strength = self.strength
        if self.inventory is not None:
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
        if self.inventory is not None:
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
        if self.inventory is not None:
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
        if self.inventory is not None:
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
        if self.inventory is not None:
            if self.inventory.head is not None:
                magicalResistance += self.inventory.head.magicalResistance
            if self.inventory.chest is not None:
                magicalResistance += self.inventory.chest.magicalResistance
            if self.inventory.leg is not None:
                magicalResistance += self.inventory.leg.magicalResistance
            if self.inventory.weapon is not None:
                magicalResistance += self.inventory.weapon.magicalResistance
        return magicalResistance

    def setHp(self, hp):
        hp_temp = self.hp + hp
        if hp_temp > self.hpMax:
            self.hp = self.hpMax
        else:
            self.hp = hp_temp
        return None

    def setHpMax(self, hp):
        hp_max = self.hpMax + hp
        self.hp = math.ceil((self.hp * hp_max) / self.hpMax)
        self.hpMax = hp_max
        self.save()

    def xpRequired(self):
        return 100 + 10 * (self.level - 1)

    def reload(self):
        if self.xp >= self.xpRequired():
            self.xp -= 100 + 10 * (self.level - 1)
            self.level += 1
            self.hpMax += 5
            self.save()
            self.strength += 2
            self.intelligence += 2
            self.agility += 2
            self.physicalResistance += 2
            self.magicalResistance += 2
            self.hp = self.getHpMax()
            self.save()
        return {
            'level': self.level,
            'xp': self.xp,
            'xpRequired': 100 + 10 * (self.level - 1),
            'hpMax': self.getHpMax(),
            'hp': self.hp,
            'strength': self.getStrength(),
            'agility': self.getAgility(),
            'intelligence': self.getIntelligence(),
            'physicalResistance': self.getPhysicalResistance(),
            'magicalResistance': self.getMagicalResistance(),
            'basic': {
                'strength': self.strength,
                'agility': self.agility,
                'intelligence': self.intelligence,
                'physicalResistance': self.physicalResistance,
                'magicalResistance': self.magicalResistance
            }
        }
