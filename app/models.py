import random

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.

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
	                                         validators=[MinValueValidator(0)],
	                                         blank=False,
	                                         null=False)
	magicalResistance = models.IntegerField(default=0,
	                                        validators=[MinValueValidator(0)],
	                                        blank=False,
	                                        null=False)
	inventory = models.OneToOneField('Inventory',
	                                 on_delete=models.PROTECT)
	
	def generateRandomCharacter(self, name, characterClass):
		self.name = name
		self.characterClass = characterClass
		self.hpMax = self.generateHpMax(characterClass)
		self.hp = self.hpMax
		self.strength = self.generateStrength(characterClass)
		self.agility = self.generateAgility(characterClass)
		self.intelligence = self.generateIntelligence(characterClass)
		self.PR = self.generatePR(characterClass)
		self.MR = self.generateMR(characterClass)
	
	def __str__(self):
		return f'{self.id}: {self.name} ' \
		       f'[Lvl: {self.level}' \
		       f'|Class: {self.characterClass.name}' \
		       f'|HpM: {self.hpMax}' \
		       f'|hp: {self.hp}' \
		       f'|Str: {self.strength}' \
		       f'|Ag: {self.agility}' \
		       f'|Int: {self.intelligence}' \
		       f'|Pr: {self.physicalResistance}' \
		       f'|Mr: {self.magicalResistance}]'
	
	def generateStrength(self, characterclass):
		return random.randint(characterclass.minStrength, characterclass.minStrength + 5)
	
	def generateHpMax(self, characterclass):
		return random.randint(characterclass.minHpMax, characterclass.minHpMax + 5)
	
	def generateAgility(self, characterclass):
		return random.randint(characterclass.minAgility, characterclass.minAgility + 5)
	
	def generateIntelligence(self, characterclass):
		return random.randint(characterclass.minInt, characterclass.minInt + 5)
	
	def generatePR(self, characterclass):
		return random.randint(characterclass.minPhysResis,
		             characterclass.minPhysResis + 5)
	
	def generateMR(self, characterclass):
		return random.randint(characterclass.minMagRes, characterclass.minMagRes + 5)


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
	                                         validators=[MinValueValidator(0)],
	                                         blank=False,
	                                         null=False)
	magicalResistance = models.IntegerField(default=0,
	                                        validators=[MinValueValidator(0)],
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
	                         related_name='headInventory')
	chest = models.ForeignKey(Chest,
	                          on_delete=models.CASCADE,
	                          related_name='chestInventory')
	leg = models.ForeignKey(Leg,
	                        on_delete=models.CASCADE,
	                        related_name='legInventory')
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


class Enemy(models.Model):
	class Meta:
		abstract = True

	name = models.CharField(max_length=20,
							default='un sbire de Alain',
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


class Minion(Enemy):
	def __init__(self, adventurer, i, *args, **kwargs):
		'''
		:param adventurer: Object from class carachter
		:param i: iteration of ennemy from place
		:param args:
		:param kwargs:
		'''
		super().__init__(*args, **kwargs)
		min_percent = (i - 1) * 3
		max_percent = (i + 2) * 3
		min_percent_def = (30 * i - 330) / 11
		max_percent_def = (7 * i - 69) / 3
		self.hpMax = random.randrange(round(adventurer.hpMax + (adventurer.hpMax * min_percent)/100),
									  round(adventurer.hpMax + (adventurer.hpMax * max_percent)/100))
		self.strength = random.randrange(round(adventurer.physicalResistance - (adventurer.physicalResistance * min_percent_def)/100),
									  	 round(adventurer.physicalResistance - (adventurer.physicalResistance * max_percent_def)/100))
		self.intelligence = random.randrange(round(adventurer.magicalResistance - (adventurer.magicalResistance * min_percent_def)/100),
									  		 round(adventurer.magicalResistance - (adventurer.magicalResistance * max_percent_def)/100))
		self.physical_resistance = random.randrange(round(adventurer.strength + (adventurer.strength * min_percent_def)/100),
									  				round(adventurer.strength + (adventurer.strength * max_percent_def)/100))
		self.magical_resistance = random.randrange(round(adventurer.intelligence + (adventurer.intelligence * min_percent_def)/100),
									  			   round(adventurer.intelligence + (adventurer.intelligence * max_percent_def)/100))
		self.agility = random.randrange(adventurer.agility - 10, adventurer.agility + 10)
		self.hp = self.hpMax


class BossAlain(Enemy):
	def __init__(self, stage, adventurer, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if(stage % 100)  == 0:
			print("KingAlain is comming for you")
		elif (stage % 50) == 0:
			print("GeneralAlain is comming for you")
		elif (stage % 10) == 0:
			print("SoldierAlain is comming for you")
		else:
			print("t'es pas censé être la mec t'a lancer une fonction au mauvais stage")

