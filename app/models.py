import random

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
	                                       validators=[MinValueValidator(10)],
	                                       blank=False,
	                                       null=False)
	minStrength = models.IntegerField(default=1,
	                                  validators=[MinValueValidator(0)],
	                                  blank=False,
	                                  null=False)
	minAgility = models.IntegerField(default=1,
	                                 validators=[MinValueValidator(0)],
	                                 blank=False,
	                                 null=False)
	minInt = models.IntegerField(default=1,
	                             validators=[MinValueValidator(0)],
	                             blank=False,
	                             null=False)
	minPhysResis = models.IntegerField(default=0,
	                                   validators=[MinValueValidator(0)],
	                                   blank=False,
	                                   null=False)
	minMagRes = models.IntegerField(default=0,
	                                validators=[MinValueValidator(0)],
	                                blank=False,
	                                null=False)
	
	def __str__(self):
		return f'{self.id}: {self.name}'
	
	def generateHpMax(self):
		return random.randint(self.minHpMax, self.minHpMax + 20)
	
	def generateStrength(self):
		return random.randint(self.minStrength, self.minStrength + 10)
	
	def generateAgility(self):
		return random.randint(self.minAgility, self.minAgility + 10)
	
	def generateIntelligence(self):
		return random.randint(self.minInt, self.minInt + 10)
	
	def generatePR(self):
		return random.randint(self.minPhysResis, self.minPhysResis + 10)
	
	def generateMR(self):
		return random.randint(self.minMagRes, self.minMagRes + 10)


# USELESS CAR PBR DE TROP NOMBREUX CALL LES UN DANS LES AUTRES MAIS C4EST
# CHELOU DONC A MONTRER A PONS
# def getRadomCarac(self):
# 	return {'hpMax': self.generateHpMax(),
# 	        'strength': self.generateStrength(),
# 	        'agility': self.generateAgility(),
# 	        'intelligence': self.generateIntelligence(),
# 	        'physicalResistance': self.generatePR(),
# 	        'magicalResistance': self.getRadomCarac()}


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
	physicalResistance = models.IntegerField(default=0,
	                                         validators=[
		                                         MinValueValidator(0)],
	                                         blank=False,
	                                         null=False)
	magicalResistance = models.IntegerField(default=0,
	                                        validators=[
		                                        MinValueValidator(0)],
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
	
	# Page de redirection après création d'un user => pour le passage en prod
	# mettre la page début de la partie du coup
	def get_absolute_url(self):
		return reverse('characterDetail', kwargs={'pk': self.pk})


class Item(models.Model):
	class Meta:
		abstract = True
	
	name = models.CharField(max_length=40,
	                        default='New Item',
	                        blank=False,
	                        null=False)
	strength = models.IntegerField(default=0,
	                               validators=[MinValueValidator(0)],
	                               blank=False,
	                               null=False)
	agility = models.IntegerField(default=0,
	                              validators=[MinValueValidator(0)],
	                              blank=False,
	                              null=False)
	intelligence = models.IntegerField(default=0,
	                                   validators=[MinValueValidator(0)],
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
	                            validators=[MinValueValidator(0)],
	                            blank=False,
	                            null=False)
	physicalResistance = models.IntegerField(default=0,
	                                         validators=[
		                                         MinValueValidator(0)],
	                                         blank=False,
	                                         null=False)
	magicalResistance = models.IntegerField(default=0,
	                                        validators=[
		                                        MinValueValidator(0)],
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
	hp = models.IntegerField(default=1,
	                         validators=[MinValueValidator(1)],
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
	character = models.ForeignKey(Character,
	                              on_delete=models.PROTECT)
	level = models.PositiveIntegerField(default=1,
	                                    validators=[MinValueValidator(1)],
	                                    blank=False,
	                                    null=False)
	
	def __str__(self):
		return f'{self.id}: {self.user.first_name} ' \
		       f'{self.character} ' \
		       f'{self.level}'
