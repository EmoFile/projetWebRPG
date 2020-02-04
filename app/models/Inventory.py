from django.db import models

from .Item import Head, Chest, Leg, Weapon, Consumable


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