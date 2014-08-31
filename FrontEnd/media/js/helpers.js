
function composeData(context){
	var data = {};
	$('input, select, textarea', $(context)).each( function(key, item) {
		var name = $(item).attr('name');
		var value = $(item).val();
		data[name] = value;
	});	
	return data;
}

function main_menu(context, option){
	$('li', $(context)).removeClass('active');
	$(option, $(context)).addClass('active');
}
