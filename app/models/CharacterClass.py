import random
from django.core.validators import MinValueValidator
from django.db import models

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

