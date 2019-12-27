$(() => {
	$('#play').click(function () {
		console.log($('#characterClass').val());
		$.ajax({
			url: 'generateCharacter',
			type: 'post',
			dataType: 'json',
			data:
				{
					'characterClass': $('#characterClass').val()
				}
		}).done(function (result) {
			console.log(result)
		});
		return false;
	});
});