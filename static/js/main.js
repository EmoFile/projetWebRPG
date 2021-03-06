function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function isEnded($pkParty){
    $.ajax({
            url: '/end/' + $pkParty,
            type: 'get',
            dataType: 'json'
        }).done(function (result){
            console.log(result);
            $('.useItem').off().attr('class', 'useItem btn btn-secondary');
            $('#playRound').off().attr('class', 'btn btn-secondary');
            $('#nextStage').attr('class', 'btn btn-secondary').off();
            $('#endRankPersonal').append(result['personalRank']);
            $('#endRank').append(result['rank']);
            $('#endUserName').append(result['username']);
            $('#endCharacterName').append(result['characterName']);
            $('#endStage').append(result['stage']);
            $('#endHpMax').append(result['hpMax']);
            $('#endStrength').append(result['strength']);
            $('#endIntelligence').append(result['intelligence']);
            $('#endAgility').append(result['agility']);
            $('#endPhysicalResistance').append(result['physicalResistance']);
            $('#endMagicalResistance').append(result['magicalResistance']);
            $('#isEndedModal').modal('handleUpdate').modal('show')
        })
}

function afterRollDice(result, $pkParty) {
    document.getElementById('enemyHp').innerText = result['enemy']['hp'];
    document.getElementById('characterHp').innerText = result['character']['hp'];
    document.getElementById('characterHpMax').innerText = result['character']['hpMax'];
    document.getElementById('characterLevel').innerText = result['character']['level'];
    document.getElementById('characterXp').innerText = result['character']['xp'];
    document.getElementById('characterXpRequired').innerText = result['character']['xpRequired'];
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
        let $damage = document.getElementById('damage');

        if (result['dropItem']['isItemDropped'] !== false) {
            $('#changeItem').show();
            $modalTitle.textContent = result['dropItem']['ItemDropped']['name'];
            $rarity.textContent = 'Rarity: ' + result['dropItem']['ItemDropped']['rarity'] + '\n';
            $stuffClassName.textContent = result['dropItem']['stuffClassName'];
            $stuffKindName.textContent = 'Type: ' + result['dropItem']['stuffClassName'];
            $stuffPk.textContent = result['dropItem']['pk'];

            if (result['dropItem']['stuffClassName'] === 'Consumable') {
                $hp.textContent = 'Hp: ' + result['dropItem']['ItemDropped']['hp'] + '\n';
            } else {
                if (result['dropItem']['stuffClassName'] === 'Weapon') {
                    $damage.textContent ='Damage: ' + result['dropItem']['ItemDropped']['diceNumber'] + 'D' + result['dropItem']['ItemDropped']['damage'];
                }
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
    if (result['isEnded']){
        isEnded($pkParty)
    }
    else if (result['enemy']['hp'] <= 0) {
        ITEM.bindItem($pkParty);
        bindNextStage($pkParty);
    } else if (!result['isEnded']) {
        bindPlayRound($pkParty);
        ITEM.bindItem($pkParty)
    }
}

function bindNextStage($pkParty) {
    $('#nextStage').attr('class', 'btn btn-success').click(function () {
        let $pkEnemy = document.getElementById('pkEnemy').innerText;
        $('#nextStage').attr('class', 'btn btn-secondary').off();
        $.ajax({
            url: '/nextEnemy/' + $pkParty + '/' + $pkEnemy,
            type: 'get',
            dataType: 'json',
        }).done(function (result) {
            if (!(result['nothingDude'])) {
                document.getElementById('pkEnemy').innerText = result['enemyPk'];
                document.getElementById('stage').innerText = result['partyStage'];
                document.getElementById('enemyHp').innerText = document.getElementById('enemyHpMax').innerText = result['enemyHpMax'];
                document.getElementById('enemyPhysicalResistance').innerText = result['enemyPhysicalResistance'];
                document.getElementById('enemyStrength').innerText = result['enemyStrength'];
                document.getElementById('enemyAgility').innerText = result['enemyAgility'];
                document.getElementById('enemyIntelligence').innerText = result['enemyIntelligence'];
                document.getElementById('enemyMagicalResistance').innerText = result['enemyMagicalResistance'];
                document.getElementById('enemyName').innerText = result['enemyName'];
                bindPlayRound($pkParty);
            }
        });
    });
}

function bindPlayRound($pkParty) {
    $('#playRound').attr('class', 'btn btn-warning').click(function () {
        let $pkEnemy = document.getElementById('pkEnemy').innerText;
        $('#playRound').off().attr('class', 'btn btn-secondary');
        $('.useItem').off().attr('class', 'useItem btn btn-secondary');
        $.ajax({
            url: '/playRound/' + $pkParty + '/' + $pkEnemy,
            type: 'get',
            dataType: 'json',
        }).done(function (result) {
            if (!(result['nothing'])) {
                addBattleReport(result, $pkParty)
            } else {
                console.log(result['nothing'])
            }
        });
    });
}

function bindRollDice() {

}

function closeModal() {
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
    let $damage = document.getElementById('damage');

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
    $damage.textContent = '';
}

const ITEM = {
    bindItem($pkParty) {
        $(".useItem").attr('class', 'useItem btn btn-success').click(function () {
            let $urlUseItem = $(this).attr('urlUseItem');
            let $coupleCharacterConsumable = $(this).attr('coupleCharacterConsumable');
            $.ajax({
                url: '/' + $urlUseItem,
                type: 'get',
                dataType: 'json',
            }).done(function (result) {
                if(result['isEnded']){
                    console.log(result)
                    isEnded($pkParty)
                }
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

async function Battle(battle, result, party) {
    let thisBattle = battle[Object.keys(battle)[0]];
    let $dockElement = $('<p></p>');
    await sleep(500);
    $dockElement.append(document.createTextNode(thisBattle['0'])).append('</br>');
    $('.battleReport').append($dockElement).animate({scrollTop: $('.battleReport').prop("scrollHeight")}, 0);
    await sleep(500);
    $dockElement.append(document.createTextNode(thisBattle['1'])).append('</br>')
    $('.battleReport').append($dockElement).animate({scrollTop: $('.battleReport').prop("scrollHeight")}, 0);
    $('.battleReport').append($dockElement);
    delete thisBattle['0'];
    delete thisBattle['1'];
    $('#rollDice').show().attr('class', 'btn btn-primary').one("click", async function () {
        $('#rollDice').off().attr('class', 'btn btn-secondary');
        for (let i in thisBattle) {
            $dockElement.append(document.createTextNode(thisBattle[i])).append('</br>');
            $('.battleReport').append($dockElement).animate({scrollTop: $('.battleReport').prop("scrollHeight")}, 0);
            await sleep(200)
        }
        delete battle[Object.keys(battle)[0]];
        if (Object.keys(battle).length === 0) {
            if (result['end'] !== undefined) {
                let fin = result['end'];
                $dockElement.append('<p>').append(document.createTextNode(fin)).append('</p>');
                $('.battleReport').append($dockElement).animate({scrollTop: $('.battleReport').prop("scrollHeight")}, 0);
            }
            afterRollDice(result, party);
        } else {
            await sleep(200)
            Battle(battle, result, party);
        }
        /* peut etre faire une fonction qi teste si il reste des chose a afficher pour le battle report (et donc supprimer au fur et a mesure*/
    });
}

async function addBattleReport(report, party) {
    let battle = report['battleReport'];
    let $dockElement = $('<p></p>');
    await Battle(battle, report, party)

}

$(() => {
    let $url = document.location.pathname;
    let $pkParty = '';

    for ($i = $url.lastIndexOf("/") + 1; $i < $url.length; $i++) {

        $pkParty += $url[$i];
    }
    ITEM.bindItem($pkParty);

    let $buttonNextStage = $('<button></button>')
        .attr('type', 'button')
        .attr('id', 'nextStage')
        .attr('class', 'btn btn-secondary')
        .html("Next Stage")
        .off();

    let $buttonPlayRound = $('<button></button>')
        .attr('type', 'button')
        .attr('id', 'playRound')
        .attr('class', 'btn btn-secondary')
        .html("Play round")
        .off();

    let $buttonRollDice = $('<button></button>')
        .attr('type', 'button')
        .attr('id', 'rollDice')
        .attr('class', 'btn btn-secondary')
        .html('Roll The Dice')
        .off();

    let $spanRollDice = $('#buttonRollDice');
    let $spanNextStage = $('#buttonNextStage');
    let $spanPlayRound = $('#buttonPlayRound');

    $spanRollDice.append($buttonRollDice);
    $spanNextStage.append($buttonNextStage);
    $spanPlayRound.append($buttonPlayRound);

    let $hpEnemy = document.getElementById('enemyHp');
    $buttonRollDice.click(false);
    if ($hpEnemy.textContent <= 0) {
        $buttonNextStage.show();
        bindNextStage($pkParty);
        $buttonPlayRound.click(false)
    } else {
        $buttonPlayRound.show();
        bindPlayRound($pkParty);
        $buttonNextStage.click(false)
    }

    $('#changeItem').hide();

    $('#changeItem').click(function () {
        $.ajax({
            url: '/changeItem/' + $pkParty + '/' + document.getElementById('stuffClassName').textContent
                + '/' + document.getElementById('stuffPk').textContent,
            type: 'get',
            dataType: 'json',
        }).done(function (result) {
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
                    break;
                case 'Epic':
                    var $color = 'color: blueviolet';
                    break;
                case 'Legendary':
                    var $color = 'color: gold';
                    break;
                default:
                    var $color = 'color: limegreen';
            }
            if (result['stuffClassName'] === 'Head') {
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
                let $weaponName = document.getElementById('weaponName');
                let $weaponKind = document.getElementById('weaponKind');
                let $weaponHpMax = document.getElementById('weaponHpMax');
                let $weaponStrength = document.getElementById('weaponStrength');
                let $weaponIntelligence = document.getElementById('weaponIntelligence');
                let $weaponAgility = document.getElementById('weaponAgility');
                let $weaponPhysicalResistance = document.getElementById('weaponPhysicalResistance');
                let $weaponMagicalResistance = document.getElementById('weaponMagicalResistance');
                let $weaponDiceNumber = document.getElementById('weaponDiceNumber');
                let $weaponDamage = document.getElementById('weaponDamage');

                $weaponName.innerText = result['newStuff'];
                $weaponKind.innerText = 'Weapon';
                $weaponName.setAttribute('style', $color);
                $weaponHpMax.innerText = result['newStuffHpMax'];
                $weaponStrength.innerText = result['newStuffStrength'];
                $weaponIntelligence.innerText = result['newStuffIntelligence'];
                $weaponAgility.innerText = result['newStuffAgility'];
                $weaponPhysicalResistance.innerText = result['newStuffPhysicalResistance'];
                $weaponMagicalResistance.innerText = result['newStuffMagicalResistance'];
                $weaponDiceNumber.innerText = result['newStuffDiceNumber'];
                $weaponDamage.innerText = result['newStuffDamage'];
            } else {
                // MODIFIE LE CONSUMABLE OU L'ATTRIBUER
                if (document.getElementById('quantity/' + $pkParty + '/' + result['stuffPk']) === null) {
                    let $div = document.getElementById('consumablesPanel');
                    let $table = document.createElement('table');
                    let $tr = document.createElement('tr');
                    let $th = document.createElement('th');
                    let $tdqunatity = document.createElement('td');
                    let $tdusebutton = document.createElement('td');
                    let $pqunatity = document.createElement('p');
                    let $usebutton = document.createElement('button');
                    let $tdtablecarac = document.createElement('td');
                    let $tablecarac = document.createElement('table');
                    let $trtablecarac = document.createElement('tr');
                    let $thhp = document.createElement('th');
                    let $spanhp = document.createElement('span');
                    let $thstrength = document.createElement('th');
                    let $spanstrength = document.createElement('span');
                    let $thintelligence = document.createElement('th');
                    let $spanintelligence = document.createElement('span');
                    let $thagility = document.createElement('th');
                    let $spanagility = document.createElement('span');

                    $table.setAttribute('class', 'table table-borderless');
                    $table.setAttribute('id', result['newStuff']);
                    $th.setAttribute('scope', 'row');
                    $th.setAttribute('style',$color);
                    $tr.setAttribute('class', 'small');
                    $th.innerText = result['newStuff'];
                    $pqunatity.setAttribute('id', 'quantity/' + $pkParty + '/' + result['stuffPk']);
                    $pqunatity.innerText = result['newStuffQuantity'];
                    $usebutton.setAttribute('urlUseItem', 'quantity/' + $pkParty + '/' + result['stuffPk']);
                    $usebutton.setAttribute('coupleCharacterConsumable', $pkParty + '/' + result['stuffPk']);
                    $usebutton.setAttribute('type', 'button');
                    $usebutton.setAttribute('class', 'useItem btn btn-success useItem');
                    $usebutton.innerText = 'Use';
                    $spanhp.setAttribute('id', 'hp/' + $pkParty + '/' + result['stuffPk']);
                    $spanstrength.setAttribute('id', 'strength/' + $pkParty + '/' + result['stuffPk']);
                    $spanintelligence.setAttribute('id', 'intelligence/' + $pkParty + '/' + result['stuffPk']);
                    $spanagility.setAttribute('id', 'agility/' + $pkParty + '/' + result['stuffPk']);
                    $spanhp.setAttribute('class', 'col-3 text-success');
                    $spanstrength.setAttribute('class', 'col-3 text-danger');
                    $spanintelligence.setAttribute('class', 'col-3 text-info');
                    $spanagility.setAttribute('class', 'col-3 text-warning');
                    $spanhp.innerText = result['newStuffHp'];
                    $spanstrength.innerText = result['newStuffStrength'];
                    $spanintelligence.innerText = result['newStuffIntelligence'];
                    $spanagility.innerText = result['newStuffAgility'];


                    $tdqunatity.append($pqunatity);
                    $tdusebutton.append($usebutton);
                    $tr.append($th);
                    $tr.append($tdqunatity);
                    $tr.append($tdusebutton);
                    $thhp.append($spanhp);
                    $thstrength.append($spanstrength);
                    $thintelligence.append($spanintelligence);
                    $thagility.append($spanagility);
                    $trtablecarac.append($thhp);
                    $trtablecarac.append($thstrength);
                    $trtablecarac.append($thintelligence);
                    $trtablecarac.append($thagility);
                    $tablecarac.append($trtablecarac);
                    $tdtablecarac.append($tablecarac);
                    $tr.append($tdtablecarac);
                    $table.append($tr);
                    $div.append($table);
                    ITEM.bindItem($pkParty);

                } else {
                    let $quantity = document.getElementById('quantity/' + $pkParty + '/' + result['stuffPk']);
                    $quantity.innerText = result['newStuffQuantity']
                }
            }
            if (result['stuffClassName'] !== 'Consumable') {
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
            console.log(result);
            if(result['isEnded']){
                isEnded($pkParty)
            }
        });
    });

    $('#closeModal').click(function () {
        closeModal();
    });


});

