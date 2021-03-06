import random
from django.db import models


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
    diceNumber = models.PositiveIntegerField(default=1,
                                             blank=False,
                                             null=False)
    damage = models.PositiveIntegerField(default=4,
                                         blank=False,
                                         null=False)

    def is_minion(self):
        return hasattr(self, 'minion')

    @classmethod
    def create(cls, adventurer, min_percent, max_percent, min_percent_def,
               max_percent_def, name, stage, *args, **kwargs):
        """
        :param adventurer: Character Adventurer
        :param min_percent:
        :param max_percent:
        :param min_percent_def:
        :param max_percent_def:
        :param name:
        :return: Enemy
        """
        ratio = (0.5*stage+49)/99
        min_ratio_damage = (0.1*adventurer.inventory.weapon.damage+36.65)/49
        max_ratio_damage = 1.10
        if min_ratio_damage > 0.90:
            min_ratio_damage = 0.90
        if ratio > 1.25:
            ratio = 1.25
        damage = random.uniform(
            min_ratio_damage*adventurer.inventory.weapon.damage,
            max_ratio_damage*adventurer.inventory.weapon.damage
        )
        damage = 4 if damage < 4 else damage
        diceNumber = random.uniform(
            adventurer.inventory.weapon.diceNumber - 1,
            adventurer.inventory.weapon.diceNumber + 1
        )
        if diceNumber > 4:
            diceNumber = 4
        elif diceNumber < 1:
            diceNumber = 1
        hpMax = round(ratio*(random.uniform(
            adventurer.hpMax + (adventurer.hpMax * min_percent) / 100,
            adventurer.hpMax + (adventurer.hpMax * max_percent) / 100)))
        strength = round(ratio*(random.uniform(
            adventurer.getPhysicalResistance() - (
                    adventurer.getPhysicalResistance() * min_percent_def) / 100,
            adventurer.getPhysicalResistance() - (
                    adventurer.getPhysicalResistance() * max_percent_def) / 100)))
        intelligence = round(ratio*(random.uniform(
            adventurer.getMagicalResistance() - (
                    adventurer.getMagicalResistance() * min_percent_def) / 100,
            adventurer.getMagicalResistance() - (
                    adventurer.getMagicalResistance() * max_percent_def) / 100)))
        physical_resistance = round(ratio*(random.uniform(
            adventurer.getStrength() + (
                    adventurer.getStrength() * min_percent_def) / 100,
            adventurer.getStrength() + (
                    adventurer.getStrength() * max_percent_def) / 100)))
        magical_resistance = round(ratio*(random.uniform(
            adventurer.getIntelligence() + (
                    adventurer.getIntelligence() * min_percent_def) / 100,
            adventurer.getIntelligence() + (
                    adventurer.getIntelligence() * max_percent_def) / 100)))
        agility = round(ratio*(random.uniform(adventurer.getAgility() - 10,
                                       adventurer.getAgility() + 10)))
        hp = hpMax
        return cls(hpMax=hpMax, strength=strength, intelligence=intelligence,
                   physical_resistance=physical_resistance,
                   magical_resistance=magical_resistance,
                   agility=agility, hp=hp, name=name, damage=damage, diceNumber=diceNumber, *args, **kwargs)

    def getDamage(self):
        damage = 0
        for i in range(0, self.diceNumber):
            damage += random.randint(1, self.damage)
        return damage


class Minion(Enemy):
    def __str__(self):
        return f'{self.id}: {self.name} ' \
               f'|HpM: {self.hpMax}' \
               f'|hp: {self.hp}' \
               f'|Str: {self.strength}' \
               f'|Ag: {self.agility}' \
               f'|Int: {self.intelligence}' \
               f'|Next: {str(self.next) if self.next is not None else None}]'

    @classmethod
    def create(cls, adventurer, i, stage, **kwargs):
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
        name = "Minions of Alain"
        return super().create(adventurer, min_percent, max_percent,
                              min_percent_def, max_percent_def, name, stage)


class BossAlain(Enemy):
    def __str__(self):
        return f'{self.id}: {self.name} ' \
               f'|HpM: {self.hpMax}' \
               f'|hp: {self.hp}' \
               f'|Str: {self.strength}' \
               f'|Ag: {self.agility}' \
               f'|Int: {self.intelligence}' \
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
                              min_percent_def, max_percent_def, name, stage)

