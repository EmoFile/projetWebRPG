$(() => {
    $('#dropButton').click(function () {
        console.log($('#dropButton').val());
        $.ajax({
            url: 'dropItem',
            type: 'get',
            dataType: 'json',
        }).done(function (result) {
            console.log(result);
            console.log(result['ItemDropped']['name']);
            let $body = $('#page-body');

            let $modal = document.createElement('div');
            // <div class="modal" tabindex="-1" role="dialog">

            let $modalDialog = document.createElement('div');
            // <div class="modal-dialog" role="document">

            let $modalContent = document.createElement('div');
            // <div class="modal-content">

            let $modalHeader = document.createElement('div');
            // <div class="modal-header">

            let $modalTitle = document.createElement('h5');
            $modalTitle.textContent = result['ItemDropped']['name'];
            // <h5 class="modal-title">' + result['ItemDropped']['name'] + '</h5>

            let $modalBody = document.createElement('div');
            // <div class="modal-body">

            let $modalBodyContent = document.createElement('p');
            $modalBodyContent.textContent = result['ItemDropped']['requiredLevel'] + result['ItemDropped']['requiredClass'] + result['ItemDropped']['rarity'];
            // <p>' + result['ItemDropped']['requiredLevel'] + result['ItemDropped']['requiredClass'] + result['ItemDropped']['rarity'] + '</p>

            let $modalFooter = document.createElement('div');
            // <div class="modal-footer">

            let $modalEquipButton = document.createElement('button');
            $modalEquipButton.textContent = 'Equiper';
            // <button type="button" class="btn btn-primary">Save changes</button>

            let $modalCloseButton = document.createElement('button');
            $modalCloseButton.textContent = 'Close';
            // <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>

            $modalFooter.append($modalEquipButton);
            $modalFooter.append($modalCloseButton);
            $modalBody.append($modalBodyContent);
            $modalHeader.append($modalTitle);

            $modalContent.append($modalHeader);
            $modalContent.append($modalBody);
            $modalContent.append($modalFooter);

            $modalDialog.append($modalContent);

            $modal.append($modalDialog);

            $body.append($modal);


        });
        return false;
    });
});