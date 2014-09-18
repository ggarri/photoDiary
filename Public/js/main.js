function init(){
	var updateListFriends = function(){
		http_request('get_friends','GET',{}, function(data){
			$('.friends').html(data);
		});	
	};

	var updateListRequests = function(){
		http_request('get_requests','GET',{}, function(data){
			$('.requests').html(data);
		});	
	};

	var update = function(){
		updateListFriends();
    	updateListRequests();
	}

	// Adding a searching input field to locate places in the map
	$('.userName').selfAutocomplete({
		service: 'search_by_name',
		accesor : [],
		label: ['fields','name'],
		key: ['pk'],
		pathLabel: 'input.userName',
		pathKey: 'input.userId',
		callback: function(){
		}
    });

	$('.reject').die().live('click', function(){
    	var requestId = $(this).parent().attr('id');
    	http_request('reject_request','POST',{'requestId':requestId}, function(data){
    		update();
    	});
    });

    $('.accept').die().live('click', function(){
    	var requestId = $(this).parent().attr('id');
    	http_request('accept_request','POST',{'requestId':requestId}, function(data){
    		update();
    	});
    });

	$('.delete').die().live('click', function(){
    	var userId = $(this).parent().attr('id');
    	http_request('del_friend','POST',{'userId':userId}, function(data){
    		update();
    	});
    });

    $('.add').die().live('click', function(){
    	var userId = $('.userId').val();
    	http_request('add_friend','POST',{'userId':userId}, function(data){
    		update();
    	});
    });
    update();
}