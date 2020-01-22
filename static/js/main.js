const BUTTON = {
    init($pkParty, $buttonNextStage, $buttonPlayRound, $spanPlayRound, $spanNextStage){
        this.pkParty =  $pkParty;
        this.buttonNextStage = $buttonNextStage;
        this.buttonPlayRound = $buttonPlayRound;
        this.spanPlayRound = $spanPlayRound;
        this.spanNexStage = $spanNextStage;
        console.log("init")
    },
    addRound(){
        this.spanPlayRound.append(this.buttonPlayRound);
        this.onBindRound();
    },
    addNextStage(){
        this.spanNexStage.append(this.buttonNextStage);
        this.onBindNextStage();
    },
    onBindRound(){
        console.log(this);
        this.pkEnemy = document.getElementById('pkEnemy').innerText;
        let $this = this;
        $('#playRound').click(function () {
            console.log($this)
        $.ajax({
            url: '/playRound/' + $this.pkParty + '/' + $this.pkEnemy,
            type: 'get',
            dataType: 'json',
        }).done(function (result) {
            console.log(result);
            document.getElementById('enemyHp').innerText = result['enemy']['hp'];
            document.getElementById('characterHp').innerText = result['character']['hp'];
            $this.onDelete(result['isEnded'], result['enemy']['hp']);
        });
        });
    },
    onBindNextStage() {
        console.log("bind next stage");
        this.pkEnemy = document.getElementById('pkEnemy').innerText;
        let $this = this;
       $('#nextStage').click(function () {
        console.log($this)
        $.ajax({
            url: '/nextEnemy/' + $this.pkParty + '/' + $this.pkEnemy,
            type: 'get',
            dataType: 'json',
        }).done(function (result) {
            console.log(result);
            document.getElementById('pkEnemy').innerText = result['enemyPk'];
            console.log(result['enemyHpMax']);
            document.getElementById('enemyHp').innerText = document.getElementById('enemyHpMax').innerText = result['enemyHpMax'];
            document.getElementById('enemyPhysicalResistance').innerText = result['enemyPhysicalResistance'];
            document.getElementById('enemyStrength').innerText = result['enemyStrength'];
            document.getElementById('enemyAgility').innerText = result['enemyAgility'];
            document.getElementById('enemyIntelligence').innerText = result['enemyIntelligence'];
            document.getElementById('enemyMagicalResistance').innerText = result['enemyMagicalResistance'];
            $this.buttonNextStage.remove();
            $this.spanPlayRound.append($this.buttonPlayRound);
            $this.onBindRound();
        });
    });
    },
    onDelete(isEnded, enemyHp){
        if(isEnded)
            this.buttonPlayRound.remove();
        else if (enemyHp <= 0 ){
            this.buttonPlayRound.remove();
            this.spanNexStage.append(this.buttonNextStage);
            this.onBindNextStage();
        }
    },

};


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

    let $buttonNextStage = document.createElement('button');
    $buttonNextStage.setAttribute('type', 'button');
    $buttonNextStage.setAttribute('id', 'nextStage');
    $buttonNextStage.setAttribute('class', 'btn btn-danger');
    $buttonNextStage.textContent = "NextStage";

    let $buttonPlayRound = document.createElement('button');
    $buttonPlayRound.setAttribute('type', 'button');
    $buttonPlayRound.setAttribute('id', 'playRound');
    $buttonPlayRound.setAttribute('class', 'btn btn-secondary');
    $buttonPlayRound.textContent = "Play round";

    let $spanNextStage = document.getElementById('buttonNextStage');
    let $spanPlayRound = document.getElementById('buttonPlayRound');

    let $hpEnemy = document.getElementById('enemyHp');
    console.log($hpEnemy.textContent);
    BUTTON.init($pkParty, $buttonNextStage, $buttonPlayRound, $spanPlayRound, $spanNextStage);
    console.log("ici")
    console.log("notre play button : ")
    if ($hpEnemy.textContent <= 0){
        BUTTON.addNextStage()
    }
    else{
        BUTTON.addRound()
    }
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
            let $hpMax = document.getElementById('characterHpMax');
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
            $hp.textContent = result['character']['hp'];
            $hpMax.textContent = result['character']['hpMax'];
            $physicalResistence.textContent = result['character']['physicalResistance'];
            $magicalResistence.textContent = result['character']['magicalResistance'];
            $strength.textContent = result['character']['strength'];
            $intelligence.textContent = result['character']['intelligence'];
            $agility.textContent = result['character']['agility'];
        });
    });


});