$(() => {
    let $url = document.location.pathname;
    console.log($url);
    console.log($url.lastIndexOf("/"));
    console.log($url.length);
    
    let $pkParty = '';
    for ($i = $url.lastIndexOf("/") + 1; $i < $url.length; $i++) {
        $pkParty += $url[$i];
    }
    console.log($pkParty);
    
    $('#dropButton').click(function () {
        $.ajax({
            url: '/dropItem',
            type: 'get',
            dataType: 'json',
        }).done(function (result) {
            console.log(result);
            
            
            let $modalTitle = document.getElementById('itemModalLabel');
            let $stuffClassName = document.getElementById('stuffClassName');
            let $stuffPk = document.getElementById('stuffPk');
            let $levelRequired = document.getElementById('levelRequired');
            let $classRequired = document.getElementById('classRequired');
            let $rarity = document.getElementById('rarity');
            let $hpMax = document.getElementById('hpMax');
            let $hp = document.getElementById('hp');
            let $physicalResistence = document.getElementById('physicalResistence');
            let $magicalResistence = document.getElementById('magicalResistence');
            let $strength = document.getElementById('strength');
            let $intelligence = document.getElementById('intelligence');
            let $agility = document.getElementById('agility');
            
            if (result['isItemDropped'] !== false) {
                $modalTitle.textContent = result['ItemDropped']['name'];
                $rarity.textContent = 'Rarity: ' + result['ItemDropped']['rarity'] + '\n';
                $stuffClassName.textContent = result['stuffClassName'];
                $stuffPk.textContent = result['pk'];
                
                if (result['stuffClassName'] === 'Consumable') {
                    $hp.textContent = 'Hp: ' + result['ItemDropped']['hp'] + '\n';
                } else {
                    $levelRequired.textContent = 'Level required: ' + result['ItemDropped']['requiredLevel'] + '\n';
                    $classRequired.textContent = 'Class: ' + result['ItemDropped']['requiredClass'] + '\n';
                    $hpMax.textContent = 'Hp max: ' + result['ItemDropped']['hpMax'] + '\n';
                    $physicalResistence.textContent = 'Physical resistence: ' + result['ItemDropped']['physicalResistence'] + '\n';
                    $magicalResistence.textContent = 'Magical resistence: ' + result['ItemDropped']['magicalResistence'] + '\n';
                }
                $strength.textContent = 'Strength: ' + result['ItemDropped']['strength'] + '\n';
                $intelligence.textContent = 'Intelligence: ' + result['ItemDropped']['intelligence'] + '\n';
                $agility.textContent = 'Agility: ' + result['ItemDropped']['agility'] + '\n';
            } else {
                $modalTitle.textContent = 'No loot here !';
            }
            $('#itemModal').on('shown.bs.modal', function () {
                
                $('#dropButton').trigger('focus')
            });
            
        });
        
    });
    
    $('#changeItem').click(function () {
        $.ajax({
            url: '/changeItem/' + $pkParty + '/' + document.getElementById('stuffClassName').textContent
                + '/' + document.getElementById('stuffPk').textContent,
            type: 'get',
            dataType: 'json',
        }).done(function (result) {
            console.log(result);

        });
    });
    
    $('#closeModal').click(function () {
        let $modalTitle = document.getElementById('itemModalLabel');
        let $levelRequired = document.getElementById('levelRequired');
        let $classRequired = document.getElementById('classRequired');
        let $rarity = document.getElementById('rarity');
        let $hpMax = document.getElementById('hpMax');
        let $hp = document.getElementById('hp');
        let $physicalResistence = document.getElementById('physicalResistence');
        let $magicalResistence = document.getElementById('magicalResistence');
        let $strength = document.getElementById('strength');
        let $intelligence = document.getElementById('intelligence');
        let $agility = document.getElementById('agility');
        $modalTitle.textContent = '';
        $rarity.textContent = '';
        $hp.textContent = '';
        $levelRequired.textContent = '';
        $classRequired.textContent = '';
        $hpMax.textContent = '';
        $physicalResistence.textContent = '';
        $magicalResistence.textContent = '';
        $strength.textContent = '';
        $intelligence.textContent = '';
        $agility.textContent = '';
    });
    
    $(".useItem").click(function () {
        let $urlUseItem = $(this).attr('urlUseItem');
        let $coupleCharacterConsumable = $(this).attr('coupleCharacterConsumable');
        console.log($urlUseItem);
        console.log($coupleCharacterConsumable);
        $.ajax({
            url: '/' + $urlUseItem,
            type: 'get',
            dataType: 'json',
        }).done(function (result) {
            console.log(result);
            let $quantity = document.getElementById('quantity/' + $coupleCharacterConsumable);
            let $hp = document.getElementById('characterHp');
            let $physicalResistence = document.getElementById('characterPhysicalResistence');
            let $magicalResistence = document.getElementById('characterMagicalResistence');
            let $strength = document.getElementById('characterStrength');
            let $intelligence = document.getElementById('characterIntelligence');
            let $agility = document.getElementById('characterAgility');
            if (result['consumableNewQuantity'] > 0) {
                $quantity.textContent = result['consumableNewQuantity'];
            } else {
                $quantity.parentElement.hidden = true;
            }
            $hp.textContent = result['character']['hp'] + '/' + result['character']['hpMax'];
            $physicalResistence.textContent = result['character']['physicalResistance'];
            $magicalResistence.textContent = result['character']['magicalResistance'];
            $strength.textContent = result['character']['strength'];
            $intelligence.textContent = result['character']['intelligence'];
            $agility.textContent = result['character']['agility'];
        });
    });
});