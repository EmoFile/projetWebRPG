from django.contrib import admin

# Register your models here.
from app.models import Character, Weapon, Head, Chest, Leg, Consumable, \
    CharacterClass, Inventory, InventoryConsumable, Party, Minion, BossAlain, Enemy, PartyEnemy


class CharacterAdmin(admin.ModelAdmin):
    def className(self, obj):
        return f'{obj.characterClass.name}'
    
    list_display = ('name',
                    'level',
                    'className',
                    'hpMax',
                    'strength',
                    'agility',
                    'intelligence',
                    'physicalResistance',
                    'magicalResistance')
    list_display_links = list_display


class WeaponAdmin(admin.ModelAdmin):
    def className(self, obj):
        return f'{obj.characterClass.name}'
    
    list_display = ('name',
                    'requiredLevel',
                    'className',
                    'rarity',
                    'diceNumber',
                    'damage',
                    'strength',
                    'agility',
                    'intelligence')
    list_display_links = list_display


class HeadAdmin(admin.ModelAdmin):
    def className(self, obj):
        return f'{obj.characterClass.name}'
    
    list_display = ('name',
                    'requiredLevel',
                    'className',
                    'rarity',
                    'hpMax',
                    'strength',
                    'agility',
                    'intelligence',
                    'physicalResistance',
                    'magicalResistance')
    list_display_links = list_display


class ChestAdmin(admin.ModelAdmin):
    def className(self, obj):
        return f'{obj.characterClass.name}'
    
    list_display = ('name',
                    'requiredLevel',
                    'className',
                    'rarity',
                    'hpMax',
                    'strength',
                    'agility',
                    'intelligence',
                    'physicalResistance',
                    'magicalResistance')
    list_display_links = list_display


class LegAdmin(admin.ModelAdmin):
    def className(self, obj):
        return f'{obj.characterClass.name}'
    
    list_display = ('name',
                    'requiredLevel',
                    'className',
                    'rarity',
                    'hpMax',
                    'strength',
                    'agility',
                    'intelligence',
                    'physicalResistance',
                    'magicalResistance')
    list_display_links = list_display


class ConsumableAdmin(admin.ModelAdmin):
    def className(self, obj):
        return f'{obj.characterClass.name}'
    
    list_display = ('name',
                    'rarity',
                    'hp',
                    'strength',
                    'agility',
                    'intelligence')
    list_display_links = list_display


class ConsumableIlineAdmin(admin.TabularInline):
    model = InventoryConsumable
    extra = 0


class InventoryAdmin(admin.ModelAdmin):
    inlines = (ConsumableIlineAdmin,)


class GenerateMinionAdmin(admin.ModelAdmin):
    def className(self, obj):
        return f'{obj.Minion.name}'


class GenerateBossAlain(admin.ModelAdmin):
    def className(self, obj):
        return f'{obj.BossAlain.name}'


class PartyAdmin(admin.ModelAdmin):
    def className(self, obj):
        return f'{obj.character.characterClass.name}'
    
    def characterName(self, obj):
        return f'{obj.character.name}'
    
    def characterLvl(self, obj):
        return f'{obj.character.level}'
    
    def characterHpMax(self, obj):
        return f'{obj.character.hpMax}'
    
    def characterStrength(self, obj):
        return f'{obj.character.strength}'
    
    def characterAgility(self, obj):
        return f'{obj.character.agility}'
    
    def characterInt(self, obj):
        return f'{obj.character.intelligence}'
    
    def characterPR(self, obj):
        return f'{obj.character.physicalResistance}'
    
    def characterMR(self, obj):
        return f'{obj.character.magicalResistance}'
    
    list_display = ('user',
                    'stage',
                    'characterName',
                    'className',
                    'characterLvl',
                    'characterHpMax',
                    'characterStrength',
                    'characterAgility',
                    'characterInt',
                    'characterPR',
                    'characterMR')
    list_display_links = list_display


admin.site.register(CharacterClass)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Weapon, WeaponAdmin)
admin.site.register(Head, HeadAdmin)
admin.site.register(Chest, ChestAdmin)
admin.site.register(Leg, LegAdmin)
admin.site.register(Consumable, ConsumableAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Party, PartyAdmin)
admin.site.register(Minion)
admin.site.register(BossAlain, GenerateBossAlain)
admin.site.register(Enemy)
admin.site.register(PartyEnemy)
