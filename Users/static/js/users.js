function init(){
	var context = '#main-area'
	main_menu('.main-menu', '.signIn');

	// Initial message widget content
	$('#messages').messages();

	// Render register form on the view, using service outcome 
	http_request('getRegisterForm', 'GET', {}, function(data) {
		$('.register_form .fields', $(context)).html(data);
		$('input[name=password]', $('.fields')).prop('type', 'password'); // Hide the password field in register form.
	});

	// Create a new user
	$('.register_form .register', $(context)).unbind('click').click(function(){
		userData = composeData('.register_form');
		http_request('setNewUser', 'POST', userData, function(data) {
			$('#messages').messages('show', data);
		});
	});

	// Remove every input fields at register form
	$('.register_form .clear', $(context)).unbind('click').click(function(){
		$.each($('input', $('.register_form')), function(key, item){
			$(item).val('');
		});
	});

	// Loggin statements
	$('.login_form button[type=submit]', $(context)).unbind('click').click(function(){
		userData = composeData('.login_form');
		http_request('login', 'POST', userData, function(data) {
			$('#messages').messages('show', data);
			if(data['type'] == true){
				window.location.reload();
			}
		});
	});
}