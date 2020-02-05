function closeModal() {
    console.log('Vidage de la modale');
    let $modalTitle = document.getElementById('itemModalLabel');
    let $levelRequired = document.getElementById('levelRequired');
    let $classRequired = document.getElementById('classRequired');
    let $stuffClassName = document.getElementById('stuffClassName');
    let $stuffKindName = document.getElementById('stuffKindName');
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
    $stuffKindName.textContent = '';
    $stuffClassName.textContent = '';
    $hpMax.textContent = '';
    $physicalResistence.textContent = '';
    $magicalResistence.textContent = '';
    $strength.textContent = '';
    $intelligence.textContent = '';
    $agility.textContent = '';
}

const ITEM = {
    bindItem() {
        $(".useItem").click(function () {
            console.log("click");
            let $urlUseItem = $(this).attr('urlUseItem');
            let $coupleCharacterConsumable = $(this).attr('coupleCharacterConsumable');
            console.log($urlUseItem);
            console.log($coupleCharacterConsumable);
            $.ajax({
                url: '/' + $urlUseItem,
                type: 'get',
                dataType: 'json',
            }).done(function (result) {
                console.log("done");
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
                    document.getElementById(result['consumableName']).remove();
                    // $quantity.parentElement.hidden = true;
                }
                $hp.textContent = result['character']['hp'];
                $physicalResistence.textContent = result['character']['physicalResistance'];
                $magicalResistence.textContent = result['character']['magicalResistance'];
                $strength.textContent = result['character']['strength'];
                $intelligence.textContent = result['character']['intelligence'];
                $agility.textContent = result['character']['agility'];

                document.getElementById('characterBasicPhysicalResistence').innerText = '(' + result['character']['basic']['physicalResistance'] + ')';
                document.getElementById('characterBasicMagicalResistence').innerText = '(' + result['character']['basic']['magicalResistance'] + ')';
                document.getElementById('characterBasicStrength').innerText = '(' + result['character']['basic']['strength'] + ')';
                document.getElementById('characterBasicAgility').innerText = '(' + result['character']['basic']['agility'] + ')';
                document.getElementById('characterBasicIntelligence').innerText = '(' + result['character']['basic']['intelligence'] + ')';
            });
        });
    }
};

function addBattleReport(report){
    let $dockElement = $('<p></p>');
    console.log(report);
    for(let i in report){
        if(i !== 'end'){
            for(let j in report[i]){
                console.log(report[i][j])
                $dockElement.append(document.createTextNode(report[i][j])).append('</br>') ;
            }
        }
    }

    if(report['end'] !== undefined){
        let  fin = report['end']
        $dockElement.append(document.createTextNode( fin)) ;
    }
    $('.battleReport').append($dockElement)
     $('.battleReport').animate({ scrollTop: $('.battleReport').prop("scrollHeight")}, 0);
}

$(() => {
    ITEM.bindItem();
    let $url = document.location.pathname;
    console.log($url);
    console.log($url.lastIndexOf("/"));
    console.log($url.length);

    let $pkParty = '';

    for ($i = $url.lastIndexOf("/") + 1; $i < $url.length; $i++) {
        $pkParty += $url[$i];
    }
    console.log($pkParty);

    let $buttonNextStage = $('<button></button>')
        .attr('type', 'button')
        .attr('id', 'nextStage')
        .attr('class', 'btn btn-danger')
        .html("Next Stage")
        .hide();

    let $buttonPlayRound = $('<button></button>')
        .attr('type', 'button')
        .attr('id', 'playRound')
        .attr('class', 'btn btn-secondary')
        .html("Play round")
        .hide();

    let $spanNextStage = $('#buttonNextStage');
    let $spanPlayRound = $('#buttonPlayRound');

    $spanNextStage.append($buttonNextStage);
    $spanPlayRound.append($buttonPlayRound);

    let $hpEnemy = document.getElementById('enemyHp');
    console.log($hpEnemy.textContent);
    console.log("ici")
    console.log("notre play button : ")
    if ($hpEnemy.textContent <= 0) {
        $buttonNextStage.show()
    } else {
        $buttonPlayRound.show()
    }

    $('#changeItem').hide();

    $('#changeItem').click(function () {
        $.ajax({
            url: '/changeItem/' + $pkParty + '/' + document.getElementById('stuffClassName').textContent
                + '/' + document.getElementById('stuffPk').textContent,
            type: 'get',
            dataType: 'json',
        }).done(function (result) {
            console.log(result);
            let $hpMax = document.getElementById('characterHpMax');
            let $hp = document.getElementById('characterHp');
            let $physicalResistence = document.getElementById('characterPhysicalResistence');
            let $magicalResistence = document.getElementById('characterMagicalResistence');
            let $strength = document.getElementById('characterStrength');
            let $intelligence = document.getElementById('characterIntelligence');
            let $agility = document.getElementById('characterAgility');
            switch (result['newStuffRarity']) {
                case 'Rare':
                    var $color = 'color: dodgerblue';
                    console.log('Rare');
                    break;
                case 'Epic':
                    var $color = 'color: blueviolet';
                    console.log('Epic');
                    break;
                case 'Legendary':
                    var $color = 'color: gold';
                    console.log('Legendary');
                    break;
                default:
                    var $color = 'color: limegreen';
                    console.log('Common');
            }
            if (result['stuffClassName'] === 'Head') {
                console.log('Head');
                let $headName = document.getElementById('headName');
                let $headKind = document.getElementById('headKind');
                let $headHpMax = document.getElementById('headHpMax');
                let $headStrength = document.getElementById('headStrength');
                let $headIntelligence = document.getElementById('headIntelligence');
                let $headAgility = document.getElementById('headAgility');
                let $headPhysicalResistance = document.getElementById('headPhysicalResistance');
                let $headMagicalResistance = document.getElementById('headMagicalResistance');

                $headName.innerText = result['newStuff'];
                $headKind.innerText = 'Head';
                $headName.setAttribute('style', $color);
                $headHpMax.innerText = result['newStuffHpMax'];
                $headStrength.innerText = result['newStuffStrength'];
                $headIntelligence.innerText = result['newStuffIntelligence'];
                $headAgility.innerText = result['newStuffAgility'];
                $headPhysicalResistance.innerText = result['newStuffPhysicalResistance'];
                $headMagicalResistance.innerText = result['newStuffMagicalResistance'];

            } else if (result['stuffClassName'] === 'Chest') {
                // MODIFIE LE CHEST OU L'ATTRIBUER
                console.log('Chest');
                let $chestName = document.getElementById('chestName');
                let $chestKind = document.getElementById('chestKind');
                let $chestHpMax = document.getElementById('chestHpMax');
                let $chestStrength = document.getElementById('chestStrength');
                let $chestIntelligence = document.getElementById('chestIntelligence');
                let $chestAgility = document.getElementById('chestAgility');
                let $chestPhysicalResistance = document.getElementById('chestPhysicalResistance');
                let $chestMagicalResistance = document.getElementById('chestMagicalResistance');

                $chestName.innerText = result['newStuff'];
                $chestKind.innerText = 'Chest';
                $chestName.setAttribute('style', $color);
                $chestHpMax.innerText = result['newStuffHpMax'];
                $chestStrength.innerText = result['newStuffStrength'];
                $chestIntelligence.innerText = result['newStuffIntelligence'];
                $chestAgility.innerText = result['newStuffAgility'];
                $chestPhysicalResistance.innerText = result['newStuffPhysicalResistance'];
                $chestMagicalResistance.innerText = result['newStuffMagicalResistance'];

            } else if (result['stuffClassName'] === 'Leg') {
                // MODIFIE LE LEG OU L'ATTRIBUER
                console.log('Leg');
                let $legName = document.getElementById('legName');
                let $legKind = document.getElementById('legKind');
                let $legHpMax = document.getElementById('legHpMax');
                let $legStrength = document.getElementById('legStrength');
                let $legIntelligence = document.getElementById('legIntelligence');
                let $legAgility = document.getElementById('legAgility');
                let $legPhysicalResistance = document.getElementById('legPhysicalResistance');
                let $legMagicalResistance = document.getElementById('legMagicalResistance');

                $legName.innerText = result['newStuff'];
                $legKind.innerText = 'Leg';
                $legName.setAttribute('style', $color);
                $legHpMax.innerText = result['newStuffHpMax'];
                $legStrength.innerText = result['newStuffStrength'];
                $legIntelligence.innerText = result['newStuffIntelligence'];
                $legAgility.innerText = result['newStuffAgility'];
                $legPhysicalResistance.innerText = result['newStuffPhysicalResistance'];
                $legMagicalResistance.innerText = result['newStuffMagicalResistance'];
            } else if (result['stuffClassName'] === 'Weapon') {
                // MODIFIE LE WEAPON OU L'ATTRIBUER
                console.log('Weapon');
                let $weaponName = document.getElementById('weaponName');
                let $weaponKind = document.getElementById('weaponKind');
                let $weaponHpMax = document.getElementById('weaponHpMax');
                let $weaponStrength = document.getElementById('weaponStrength');
                let $weaponIntelligence = document.getElementById('weaponIntelligence');
                let $weaponAgility = document.getElementById('weaponAgility');
                let $weaponPhysicalResistance = document.getElementById('weaponPhysicalResistance');
                let $weaponMagicalResistance = document.getElementById('weaponMagicalResistance');

                $weaponName.innerText = result['newStuff'];
                $weaponKind.innerText = 'Weapon';
                $weaponName.setAttribute('style', $color);
                $weaponHpMax.innerText = result['newStuffHpMax'];
                $weaponStrength.innerText = result['newStuffStrength'];
                $weaponIntelligence.innerText = result['newStuffIntelligence'];
                $weaponAgility.innerText = result['newStuffAgility'];
                $weaponPhysicalResistance.innerText = result['newStuffPhysicalResistance'];
                $weaponMagicalResistance.innerText = result['newStuffMagicalResistance'];
            } else {
                // MODIFIE LE CONSUMABLE OU L'ATTRIBUER
                console.log('Consumable');
                console.log('useItem/' + $pkParty + '/' + result['stuffPk']);
                console.log(document.getElementById('quantity/' + $pkParty + '/' + result['stuffPk']));
                if (document.getElementById('quantity/' + $pkParty + '/' + result['stuffPk']) === null) {
                    let $div = document.getElementById('consumablesPanel');
                    let $table = document.createElement('table');
                    let $tr = document.createElement('tr');
                    let $th = document.createElement('th');
                    let $tdqunatity = document.createElement('td');
                    let $tdusebutton = document.createElement('td');
                    let $pqunatity = document.createElement('p');
                    let $usebutton = document.createElement('button');
                    $table.setAttribute('class', 'table table-borderless');
                    $table.setAttribute('id', result['newStuff']);
                    $th.setAttribute('scope', 'row');
                    $th.innerText = result['newStuff'];
                    $pqunatity.setAttribute('id', 'quantity/' + $pkParty + '/' + result['stuffPk']);
                    $pqunatity.innerText = result['newStuffQuantity'];
                    $usebutton.setAttribute('urlUseItem', 'quantity/' + $pkParty + '/' + result['stuffPk']);
                    $usebutton.setAttribute('coupleCharacterConsumable', $pkParty + '/' + result['stuffPk']);
                    $usebutton.setAttribute('type', 'button');
                    $usebutton.setAttribute('class', 'useItem btn btn-success useItem');
                    $usebutton.innerText = 'Use';

                    $tdqunatity.append($pqunatity);
                    $tdusebutton.append($usebutton);
                    $tr.append($th);
                    $tr.append($tdqunatity);
                    $tr.append($tdusebutton);
                    $table.append($tr);
                    $div.append($table);
                    ITEM.bindItem();

                } else {
                    let $quantity = document.getElementById('quantity/' + $pkParty + '/' + result['stuffPk']);
                    $quantity.innerText = result['newStuffQuantity']
                }
            }
            console.log("avant le result.character");
            console.log(result);
            if (result['stuffClassName'] !== 'Consumable') {
                console.log(result['character'])
                $hpMax.innerText = result['character']['hpMax'];
                $hp.innerText = result['character']['hp'];
                $physicalResistence.innerText = result['character']['physicalResistance'];
                $magicalResistence.innerText = result['character']['magicalResistance'];
                $strength.innerText = result['character']['strength'];
                $intelligence.innerText = result['character']['intelligence'];
                $agility.innerText = result['character']['agility'];
            }
            $('#itemModal').modal('hide');
            closeModal();
        });
    });

    $('#closeModal').click(function () {
        closeModal();
    });
    $('#playRound').click(function () {
        let $pkEnemy = document.getElementById('pkEnemy').innerText;
        $.ajax({
            url: '/playRound/' + $pkParty + '/' + $pkEnemy,
            type: 'get',
            dataType: 'json',
        }).done(function (result) {
            if (!(result['nothing'])){
                console.log(result);
                addBattleReport(result['battleReport']);
                document.getElementById('enemyHp').innerText = result['enemy']['hp'];
                document.getElementById('characterHp').innerText = result['character']['hp'];
                document.getElementById('characterHpMax').innerText = result['character']['hpMax'];
                document.getElementById('characterLevel').innerText = result['character']['level'];
                document.getElementById('characterXp').innerText = result['character']['xp'];
                document.getElementById('characterXpRequired').innerText = result['character']['xpRequired'];
                console.log(document.getElementById('characterXpRequired'));
                console.log(document.getElementById('characterXpRequired').innerText);
                console.log(result['character']['xpRequired']);
                document.getElementById('characterPhysicalResistence').innerText = result['character']['physicalResistance'];
                document.getElementById('characterMagicalResistence').innerText = result['character']['magicalResistance'];
                document.getElementById('characterStrength').innerText = result['character']['strength'];
                document.getElementById('characterAgility').innerText = result['character']['agility'];
                document.getElementById('characterIntelligence').innerText = result['character']['intelligence'];
                document.getElementById('characterBasicPhysicalResistence').innerText = '(' + result['character']['basic']['physicalResistance'] + ')';
                document.getElementById('characterBasicMagicalResistence').innerText = '(' + result['character']['basic']['magicalResistance'] + ')';
                document.getElementById('characterBasicStrength').innerText = '(' + result['character']['basic']['strength'] + ')';
                document.getElementById('characterBasicAgility').innerText = '(' + result['character']['basic']['agility'] + ')';
                document.getElementById('characterBasicIntelligence').innerText = '(' + result['character']['basic']['intelligence'] + ')';
                if (result['dropItem']) {
                    console.log('Y a un drop un drop mec !!!');
                    console.log(result['dropItem']);

                    let $modalTitle = document.getElementById('itemModalLabel');
                    let $stuffClassName = document.getElementById('stuffClassName');
                    let $stuffKindName = document.getElementById('stuffKindName');
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
                        $('#changeItem').show();
                        $modalTitle.textContent = result['dropItem']['ItemDropped']['name'];
                        $rarity.textContent = 'Rarity: ' + result['dropItem']['ItemDropped']['rarity'] + '\n';
                        $stuffClassName.textContent = result['dropItem']['stuffClassName'];
                        $stuffKindName.textContent ='Type: ' + result['dropItem']['stuffClassName'];
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
                        $('#changeItem').hide()
                    }
                    // $('#itemModal').show();
                    $('#itemModal').modal('show');
                }
                console.log(result['isEnded']);
                if (result['isEnded'])
                    $buttonPlayRound.hide();
                else if (result['enemy']['hp'] <= 0) {
                    $buttonPlayRound.hide();
                    $buttonNextStage.show();
                }
            }
            else{
                console.log(result['nothing'])
            }
        });
    });

    $('#nextStage').click(function () {
        let $pkEnemy = document.getElementById('pkEnemy').innerText;
        $buttonNextStage.hide();
        $.ajax({
            url: '/nextEnemy/' + $pkParty + '/' + $pkEnemy,
            type: 'get',
            dataType: 'json',
        }).done(function (result) {
            console.log(result['nothingDude'])
            if (!(result['nothingDude'])){
                console.log(result);
                document.getElementById('pkEnemy').innerText = result['enemyPk'];
                document.getElementById('stage').innerText = result['partyStage'];
                console.log(result['enemyHpMax']);
                document.getElementById('enemyHp').innerText = document.getElementById('enemyHpMax').innerText = result['enemyHpMax'];
                document.getElementById('enemyPhysicalResistance').innerText = result['enemyPhysicalResistance'];
                document.getElementById('enemyStrength').innerText = result['enemyStrength'];
                document.getElementById('enemyAgility').innerText = result['enemyAgility'];
                document.getElementById('enemyIntelligence').innerText = result['enemyIntelligence'];
                document.getElementById('enemyMagicalResistance').innerText = result['enemyMagicalResistance'];
                document.getElementById('enemyName').innerText = result['enemyName'];
                $buttonPlayRound.show();
            }
        });
    });
});

