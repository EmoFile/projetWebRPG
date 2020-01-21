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
            url: 'dropItem',
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
    // $('#dropButton').click(function () {
    //     console.log($('#dropButton').val());
    //     $.ajax({
    //         url: 'dropItem',
    //         type: 'get',
    //         dataType: 'json',
    //     }).done(function (result) {
    //         console.log(result);
    //         console.log(result['ItemDropped']['name']);
    //         let $body = $('#page-body');
    //
    //         let $modal = document.createElement('div');
    //         // <div class="modal" tabindex="-1" role="dialog">
    //
    //         let $modalDialog = document.createElement('div');
    //         // <div class="modal-dialog" role="document">
    //
    //         let $modalContent = document.createElement('div');
    //         // <div class="modal-content">
    //
    //         let $modalHeader = document.createElement('div');
    //         // <div class="modal-header">
    //
    //         let $modalTitle = document.createElement('h5');
    //         $modalTitle.textContent = result['ItemDropped']['name'];
    //         // <h5 class="modal-title">' + result['ItemDropped']['name'] + '</h5>
    //
    //         let $modalBody = document.createElement('div');
    //         // <div class="modal-body">
    //
    //         let $modalBodyContent = document.createElement('p');
    //         $modalBodyContent.textContent = result['ItemDropped']['requiredLevel'] + result['ItemDropped']['requiredClass'] + result['ItemDropped']['rarity'];
    //         // <p>' + result['ItemDropped']['requiredLevel'] + result['ItemDropped']['requiredClass'] + result['ItemDropped']['rarity'] + '</p>
    //
    //         let $modalFooter = document.createElement('div');
    //         // <div class="modal-footer">
    //
    //         let $modalEquipButton = document.createElement('button');
    //         $modalEquipButton.textContent = 'Equiper';
    //         // <button type="button" class="btn btn-primary">Save changes</button>
    //
    //         let $modalCloseButton = document.createElement('button');
    //         $modalCloseButton.textContent = 'Close';
    //         // <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
    //
    //         $modalFooter.append($modalEquipButton);
    //         $modalFooter.append($modalCloseButton);
    //         $modalBody.append($modalBodyContent);
    //         $modalHeader.append($modalTitle);
    //
    //         $modalContent.append($modalHeader);
    //         $modalContent.append($modalBody);
    //         $modalContent.append($modalFooter);
    //
    //         $modalDialog.append($modalContent);
    //
    //         $modal.append($modalDialog);
    //
    //         $body.append($modal);
    // });
    //     });
    //     return false;
    // });

});