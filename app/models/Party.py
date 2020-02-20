import datetime

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from app.models import Character, Enemy


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
    
    def game_over(self):
        self.isEnded = True
        adventurer = self.character
        adventurer.strength = adventurer.getStrength()
        adventurer.agility = adventurer.getAgility()
        adventurer.intelligence = adventurer.getIntelligence()
        adventurer.magicalResistance = adventurer.getMagicalResistance()
        adventurer.physicalResistance = adventurer.getPhysicalResistance()
        adventurer.save()
        PartyEnemy.objects.filter(party=self).delete()
        self.character.inventory.delete()
        self.save()


class PartyEnemy(models.Model):
    party = models.ForeignKey(Party,
                              on_delete=models.CASCADE)
    enemy = models.ForeignKey(Enemy,
                              on_delete=models.CASCADE)
    hp = models.IntegerField(default=0,
                             blank=False,
                             null=False)

    def __str__(self):
        return f'{self.id}: {self.party.character.name} | {self.enemy.name} | {self.hp}'