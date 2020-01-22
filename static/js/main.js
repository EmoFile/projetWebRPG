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
    
    $('#changeItem').click(function () {
        $.ajax({
            url: '/changeItem/' + $pkParty + '/' + document.getElementById('stuffClassName').textContent
                + '/' + document.getElementById('stuffPk').textContent,
            type: 'get',
            dataType: 'json',
        }).done(function (result) {
            console.log(result);
            if(result['stuffClassName'] === 'Head'){
                console.log('Head')
                
            } else if(result['stuffClassName'] === 'Chest'){
            // MODIFIE LE CHEST OU L'ATTRIBUER
                console.log('Head')

            } else if(result['stuffClassName'] === 'Leg'){
            // MODIFIE LE LEG OU L'ATTRIBUER
                console.log('Head')
            } else if(result['stuffClassName'] === 'Weapon'){
            // MODIFIE LE WEAPON OU L'ATTRIBUER
                console.log('Head')
            } else {
            // MODIFIE LE CONSUMABLE OU L'ATTRIBUER
                console.log('Consum')

            }
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
    $('#playRound').click(function () {
        let $pkEnemy = document.getElementById('pkEnemy').innerText;
        $.ajax({
            url: '/playRound/' + $pkParty + '/' + $pkEnemy,
            type: 'get',
            dataType: 'json',
        }).done(function (result) {
            console.log('Hp ennemy: ' + result['enemy']['hp']);
            console.log('Hp character: ' + result['character']['hp']);
            if (result['dropItem']) {
                console.log('Y a un drop un drop mec !!!');
                console.log(result['dropItem']);
                
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
                
                if (result['dropItem']['isItemDropped'] !== false) {
                    $modalTitle.textContent = result['dropItem']['ItemDropped']['name'];
                    $rarity.textContent = 'Rarity: ' + result['dropItem']['ItemDropped']['rarity'] + '\n';
                    $stuffClassName.textContent = result['dropItem']['stuffClassName'];
                    $stuffPk.textContent = result['dropItem']['pk'];
                    
                    if (result['dropItem']['stuffClassName'] === 'Consumable') {
                        $hp.textContent = 'Hp: ' + result['dropItem']['ItemDropped']['hp'] + '\n';
                    } else {
                        $levelRequired.textContent = 'Level required: ' + result['dropItem']['ItemDropped']['requiredLevel'] + '\n';
                        $classRequired.textContent = 'Class: ' + result['dropItem']['ItemDropped']['requiredClass'] + '\n';
                        $hpMax.textContent = 'Hp max: ' + result['dropItem']['ItemDropped']['hpMax'] + '\n';
                        $physicalResistence.textContent = 'Physical resistence: ' + result['dropItem']['ItemDropped']['physicalResistence'] + '\n';
                        $magicalResistence.textContent = 'Magical resistence: ' + result['dropItem']['ItemDropped']['magicalResistence'] + '\n';
                    }
                    $strength.textContent = 'Strength: ' + result['dropItem']['ItemDropped']['strength'] + '\n';
                    $intelligence.textContent = 'Intelligence: ' + result['dropItem']['ItemDropped']['intelligence'] + '\n';
                    $agility.textContent = 'Agility: ' + result['dropItem']['ItemDropped']['agility'] + '\n';
                } else {
                    $modalTitle.textContent = 'No loot here !';
                }
                // $('#itemModal').show();
                $('#itemModal').modal('show')
                
            }
        });
    })
    ;
    $('#nextStage').click(function () {
        let $pkEnemy = document.getElementById('pkEnemy').innerText;
        $.ajax({
            url: '/nextEnemy/' + $pkParty + '/' + $pkEnemy,
            type: 'get',
            dataType: 'json',
        }).done(function (result) {
            console.log(result);
            document.getElementById('pkEnemy').innerText = result['enemyPk'];
        });
    });
})
;